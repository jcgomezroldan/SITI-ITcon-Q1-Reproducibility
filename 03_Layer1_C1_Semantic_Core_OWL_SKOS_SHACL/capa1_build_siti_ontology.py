#!/usr/bin/env python3
"""
build_siti_ontology.py
----------------------
Script integral y determinista para transformar toda la taxonomía SITI 
(Archivos CSV A10-A50 y B10-B50 con la nomenclatura corregida del Lenguaje B)
en RDF/OWL y SKOS serializados en Turtle (.ttl) y RDF/XML (.owl).
La serialización no acredita razonamiento OWL 2 DL ni importación nativa en Protégé.

Estructura de Lenguajes SITI:
- Lenguaje A (Geométrico/Topológico):
    A10: Zonas geográficas
    A20: Infraestructuras y complejos
    A30: Áreas y espacios funcionales
    A40: Sistemas e instalaciones operativas
    A50: Componentes funcionales
- Lenguaje B (Parámetros de Gestión/Alfanumérico):
    B10: Gestión de proyectos y activos
    B20: Personal y actores
    B30: Ayudas de diseño y construcción (CAD, Materiales, Herramientas y Equipos)
    B40: Actividades, productos y servicios (Seguridad vial, Sostenibilidad, APU Distritales, APU Nacionales)
    B50: Propiedades e indicadores (Especificaciones técnicas, KPIs, Parámetros físicos, Inventario)

Autor: JC Gomez-Roldan & Antigravity AI
Fecha: 2026-08-16
"""

import os

# Autoridad común sin efectos de escritura al importar.
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from siti_semantic_registry import SemanticRegistry
import csv
import sys
import json
import re
import unicodedata
from collections import Counter
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD, SKOS, BNode, URIRef

# 1. Definición de Espacios de Nombres (Namespaces)
BASE_URI = "http://www.semanticweb.org/jcgr/SITI/"
ONTOLOGY_IRI = "http://www.semanticweb.org/jcgr/SITI"
SITI = Namespace(BASE_URI)

def get_ifc_class_mapping(code_raw, desc, clas, filename):
    registry = SemanticRegistry(os.path.dirname(os.path.dirname(__file__)))
    code = code_raw.replace(' ', '_').replace('/', '_')
    mapping = registry.mapping(filename.replace('.csv', ''), code, desc)
    if mapping is None:
        raise ValueError(f'Referencia no seleccionable: {code}')
    return tuple(mapping[k] for k in ('entity', 'predefined_type', 'property_set', 'description'))


def create_siti_ontology(registry=None, output_dir=None, *, fixed_artifacts=None):
    """Genera C1 desde una revisión fijada; kits y datos se publican explícitamente."""
    registry = registry or SemanticRegistry(os.path.dirname(os.path.dirname(__file__)))
    registry.require_promotable()
    g = Graph()
    
    # 1. Vincular prefijos estándar
    g.bind("", SITI)
    g.bind("siti", SITI)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("rdf", RDF)
    g.bind("xsd", XSD)
    g.bind("skos", SKOS)

    # 2. Declaración de la Ontología
    ont_node = SITI[""]
    g.add((ont_node, RDF.type, OWL.Ontology))
    g.add((ont_node, OWL.versionIRI, SITI[registry.version]))
    g.add((ont_node, RDFS.label, Literal("Ontología del Sistema de Clasificación de Infraestructura de Transporte Intermodal (SITI)", lang="es")))
    g.add((ont_node, RDFS.comment, Literal("Taxonomía colombiana SITI con lenguajes A/B desacoplados y contratos explícitos. Mapeos IFC y referencias técnicas conservan fuente y estado de revisión; su presencia no certifica conformidad normativa ni importación nativa.", lang="es")))

    # 3. Propiedades de Anotación (Annotation Properties)
    prop_codigo = SITI["codigoSITI"]
    prop_nivel = SITI["nivel"]
    prop_clasificacion = SITI["clasificacion"]
    prop_lenguaje = SITI["lenguaje"]
    prop_origen = SITI["origenCSV"]

    # Fase 5: Anotaciones Semánticas de Interoperabilidad IFC (ISO 16739-1:2024) y GIS/CRS
    prop_ifc_entity = SITI["ifcEntity"]
    prop_ifc_ptype = SITI["ifcPredefinedType"]
    prop_ifc_pset = SITI["ifcPropertySet"]
    prop_ifc_desc = SITI["ifcMappingDescription"]
    prop_ifc_gis_crs = SITI["ifcGisCRS"]
    prop_ifc_linear_ref = SITI["ifcLinearReferencing"]
    prop_ifc_gis_rep = SITI["ifcGisRepresentation"]

    for prop, label_text in [
        (prop_codigo, "Código SITI"),
        (prop_nivel, "Nivel de la jerarquía"),
        (prop_clasificacion, "Tipo de clasificación (Tabla, Grupo, Subgrupo, Sección, Objeto, Subobjeto)"),
        (prop_lenguaje, "Lenguaje SITI (A: Geométrico, B: Parámetros de Gestión)"),
        (prop_origen, "Archivo CSV de origen"),
        (prop_ifc_entity, "Entidad IFC (ISO 16739-1:2024)"),
        (prop_ifc_ptype, "Tipo Predefinido IFC (PredefinedType)"),
        (prop_ifc_pset, "Conjunto de Propiedades IFC (PropertySet)"),
        (prop_ifc_desc, "Descripción de Mapeo Interoperable IFC"),
        (prop_ifc_gis_crs, "Georreferenciación GIS / CRS IFC (ISO 19111 / IfcProjectedCRS / EPSG)"),
        (prop_ifc_linear_ref, "Referenciación Lineal ISO 19148 / Abscisado IFC (IfcAlignment)"),
        (prop_ifc_gis_rep, "Representación Geográfica GIS-BIM (IfcGeographicElement / IfcSite)")
    ]:
        g.add((prop, RDF.type, OWL.AnnotationProperty))
        g.add((prop, RDFS.label, Literal(label_text, lang="es")))

    # Helpers para creación de Object Properties
    def add_obj_prop(id_name, label_es, comment_es, domain=None, range_=None, inverse_id=None, inverse_label=None, inverse_comment=None, is_transitive=False, is_symmetric=False, is_asymmetric=False, is_irreflexive=False):
        p_node = SITI[id_name]
        g.add((p_node, RDF.type, OWL.ObjectProperty))
        g.add((p_node, RDFS.label, Literal(label_es, lang="es")))
        g.add((p_node, RDFS.comment, Literal(comment_es, lang="es")))
        if domain:
            g.add((p_node, RDFS.domain, domain))
        if range_:
            g.add((p_node, RDFS.range, range_))
        if is_transitive:
            g.add((p_node, RDF.type, OWL.TransitiveProperty))
        if is_symmetric:
            g.add((p_node, RDF.type, OWL.SymmetricProperty))
        if is_asymmetric:
            g.add((p_node, RDF.type, OWL.AsymmetricProperty))
        if is_irreflexive:
            g.add((p_node, RDF.type, OWL.IrreflexiveProperty))

        if inverse_id:
            inv_node = SITI[inverse_id]
            g.add((inv_node, RDF.type, OWL.ObjectProperty))
            g.add((inv_node, RDFS.label, Literal(inverse_label or f"inversa de {label_es}", lang="es")))
            g.add((inv_node, RDFS.comment, Literal(inverse_comment or f"Relación inversa de {label_es}.", lang="es")))
            if range_:
                g.add((inv_node, RDFS.domain, range_))
            if domain:
                g.add((inv_node, RDFS.range, domain))
            if is_transitive:
                g.add((inv_node, RDF.type, OWL.TransitiveProperty))
            if is_symmetric:
                g.add((inv_node, RDF.type, OWL.SymmetricProperty))
            if is_asymmetric:
                g.add((inv_node, RDF.type, OWL.AsymmetricProperty))
            if is_irreflexive:
                g.add((inv_node, RDF.type, OWL.IrreflexiveProperty))

            g.add((p_node, OWL.inverseOf, inv_node))
            g.add((inv_node, OWL.inverseOf, p_node))

    # ==================================================================
    # 4.1. FASE 2: OBJECT PROPERTIES DEL LENGUAJE A (Geométrico/Espacial)
    # ==================================================================
    Class_A = SITI["A"]
    Class_A10 = SITI["A10"]
    Class_A20 = SITI["A20"]
    Class_A30 = SITI["A30"]
    Class_A40 = SITI["A40"]
    Class_A50 = SITI["A50"]

    Class_B = SITI["B"]
    Class_B10 = SITI["B10"]
    Class_B20 = SITI["B20"]
    Class_B30 = SITI["B30"]
    Class_B40 = SITI["B40"]
    Class_B50 = SITI["B50"]

    # Composición mereológica y albergue desacoplado
    add_obj_prop("hasPart", "tiene parte", "Relación mereológica general que indica que un activo o entidad contiene o está compuesto por otra.", domain=Class_A, range_=Class_A, inverse_id="isPartOf", inverse_label="es parte de", is_transitive=True)
    add_obj_prop("albergaElemento", "alberga elemento de infraestructura", "Permite que una entidad espacial (A10) o infraestructura (A20) albergue elementos de cualquier otra tabla sin obligar una estructura rígida.", domain=Class_A, range_=Class_A, inverse_id="albergadoEn", inverse_label="está albergado en")
    add_obj_prop("compuestoPorElemento", "está compuesto por elemento", "Relación jerárquica desacoplada de composición física entre elementos del Lenguaje A.", domain=Class_A, range_=Class_A, inverse_id="parteDeElemento", inverse_label="es parte de elemento", is_transitive=True)
    add_obj_prop("alojaElementoDirectamente", "aloja elemento directamente", "Relación desacoplada directa A10 -> A40.", domain=Class_A10, range_=Class_A40, inverse_id="alojadoDirectamenteEn", inverse_label="está alojado directamente en zona geográfica")
    add_obj_prop("tieneComponenteEstructurante", "tiene componente estructurante", "Relación desacoplada A40 -> A50.", domain=Class_A40, range_=Class_A50, inverse_id="esComponenteEstructuranteDe", inverse_label="es componente estructurante de")
    add_obj_prop("constaDeCapaOMaterial", "consta de capa o material", "Relación desacoplada A30 -> A50.", domain=Class_A30, range_=Class_A50, inverse_id="esCapaDeEspacio", inverse_label="es capa de espacio o terreno")
    add_obj_prop("tieneSubcomponente", "tiene subcomponente", "Relación desacoplada de anidamiento A50 -> A50.", domain=Class_A50, range_=Class_A50, inverse_id="esSubcomponenteDe", inverse_label="es subcomponente de", is_transitive=True)

    # Dimensión Longitudinal (Alineamiento / ISO 19148)
    add_obj_prop("sigueLongitudinalmenteA", "sigue longitudinalmente a", "Orden secuencial de elementos a lo largo del alineamiento longitudinal de la infraestructura.", domain=Class_A, range_=Class_A, inverse_id="precedeLongitudinalmenteA", inverse_label="precede longitudinalmente a", is_transitive=True)
    add_obj_prop("contiguoLongitudinalmenteCon", "es contiguo longitudinalmente con", "Relación de continuidad espacial directa entre dos tramos o elementos a lo largo de la vía.", domain=Class_A, range_=Class_A, is_symmetric=True)
    add_obj_prop("estaPrecedidoDirectamentePor", "está precedido directamente por", "Adyacencia lineal directa anterior.", domain=Class_A, range_=Class_A, inverse_id="estaSeguidoDirectamentePor", inverse_label="está seguido directamente por", is_asymmetric=True, is_irreflexive=True)
    add_obj_prop("subdivididoEnSector", "está subdividido en sector/tramo", "Segmentación longitudinal de una infraestructura en sectores, tramos o sub-tramos.", domain=Class_A, range_=Class_A, inverse_id="sectorPerteneceA", inverse_label="es sector/tramo de")
    add_obj_prop("tieneSegmentoLongitudinal", "tiene segmento longitudinal", "Segmentación lineal ISO 19148.", domain=Class_A, range_=Class_A, inverse_id="esSegmentoLongitudinalDe", inverse_label="es segmento longitudinal de", is_transitive=True)

    # Dimensión Transversal (Sección Transversal / Adyacencia Lateral)
    add_obj_prop("adyacenteTransversalmenteA", "es adyacente transversalmente a", "Relación de disposición lateral en la sección transversal de la vía (ej. Calzada <-> Berma <-> Sardinel <-> Cuneta).", domain=Class_A, range_=Class_A, is_symmetric=True)
    add_obj_prop("delimitadoTransversalmentePor", "está delimitado transversalmente por", "Especifica el elemento de contención o borde lateral (ej. sardinel, barrera de seguridad, talud).", domain=Class_A, range_=Class_A, inverse_id="delimitaTransversalmenteA", inverse_label="delimita transversalmente a")
    add_obj_prop("flanqueadoPor", "está flanqueado por", "Relación de protección o borde a ambos lados o en los costados de un elemento transversal.", domain=Class_A, range_=Class_A, inverse_id="flanqueaA", inverse_label="flanquea a")
    add_obj_prop("estaALaIzquierdaDe", "está a la izquierda de", "Disposición en el margen izquierdo.", domain=Class_A, range_=Class_A, inverse_id="estaALaDerechaDe", inverse_label="está a la derecha de", is_asymmetric=True, is_irreflexive=True)
    add_obj_prop("esLateralA", "es lateral a", "Ubicación en margen lateral.", domain=Class_A, range_=Class_A, inverse_id="esCentralA", inverse_label="es central a")

    # Dimensión Vertical / Alzado (Estratigrafía y Estructura Portante)
    add_obj_prop("superpuestoA", "está superpuesto a (encima de)", "Relación de alzado/estratigrafía vertical (ej. Carpeta Asfáltica superpuesta a Base; Base superpuesta a Subbase; Subbase superpuesta a Subrasante).", domain=Class_A, range_=Class_A, inverse_id="subyaceA", inverse_label="subyace a (debajo de)", is_transitive=True)
    add_obj_prop("soportaEstructuralmenteA", "soporta estructuralmente a", "Relación de soporte de cargas mecánicas y físicas entre elementos de infraestructura.", domain=Class_A, range_=Class_A, inverse_id="soportadoPorEstructuralmente", inverse_label="es soportado estructuralmente por", is_transitive=True)
    add_obj_prop("cimentadoEn", "está cimentado en", "Relación de apoyo o cimentación de elementos o estructuras sobre el terreno/subrasante o pilotes.", domain=Class_A, range_=Class_A, inverse_id="sirveDeCimentacionA", inverse_label="sirve de cimentación a")
    add_obj_prop("estaDirectamenteSobre", "está directamente sobre", "Contacto vertical directo superior.", domain=Class_A, range_=Class_A, inverse_id="estaDirectamenteDebajoDe", inverse_label="está directamente debajo de", is_asymmetric=True, is_irreflexive=True)

    # ==================================================================
    # 4.2. FASE 3: OBJECT PROPERTIES DEL LENGUAJE B (Nomenclatura Corregida)
    # ==================================================================
    add_obj_prop("sitiManagementRelation", "Relación general de gestión SITI", "Propiedad de objeto raíz abstracta del Lenguaje B.", domain=Class_B, range_=Class_B)
    add_obj_prop("hasManagementPart", "tiene parte de gestión", "Relación mereológica general del Lenguaje B.", domain=Class_B, range_=Class_B, inverse_id="isManagementPartOf", inverse_label="es parte de gestión de", is_transitive=True)

    # B10 (Fases, BIM, Riesgo, Documentos)
    add_obj_prop("requiereModeloBIM", "requiere modelo BIM", "Vincula una fase del proyecto (B10_015) con la tipología de modelo BIM adecuada (B10_025).", domain=SITI["B10_015"], range_=SITI["B10_025"], inverse_id="modeloBIMUsadoEnFase", inverse_label="es modelo BIM usado en fase")
    add_obj_prop("requiereNivelInformacionLOIN", "requiere nivel de información LOIN", "Vincula una fase de proyecto (B10_015) con el nivel de detalle de información LOIN requerido (B10_025).", domain=SITI["B10_015"], range_=SITI["B10_025"], inverse_id="nivelInformacionRequeridoEn", inverse_label="es nivel de información requerido en")
    add_obj_prop("ejecutaUsoBIM", "ejecuta uso GIS-BIM", "Asigna casos de uso o aplicaciones GIS-BIM (B10_025) a una fase del ciclo de vida (B10_015).", domain=SITI["B10_015"], range_=SITI["B10_025"], inverse_id="usoBIMEjecutadoEn", inverse_label="es uso GIS-BIM ejecutado en")
    add_obj_prop("aplicaFormatoDocumental", "aplica formato documental", "Vincula una entidad pública (B20_025) o actor con los documentos y formatos oficiales exigidos (B10_010).", domain=Class_B20, range_=SITI["B10_010"], inverse_id="formatoDocumentalAplicaAEntidad", inverse_label="es formato documental aplicable a entidad")

    # B20 (Personal y Actores)
    add_obj_prop("tieneDependenciaEstructurada", "tiene dependencia estructurada", "Conecta una entidad pública ejecutora (ej. ANI, INVIAS B20_025) con sus dependencias orgánicas autorizadas (B20_015).", domain=SITI["B20_025"], range_=SITI["B20_015"], inverse_id="dependenciaPerteneceAEntidad", inverse_label="es dependencia de entidad")
    add_obj_prop("perteneceAEntidadOPrivada", "pertenece a entidad pública o sector privado", "Vincula un actor/interesado (B20_030) con su entidad pública de origen (B20_025) o figura jurídica privada (B20_035).", domain=SITI["B20_030"], range_=Class_B20, inverse_id="vinculaActorOInteresado", inverse_label="vincula a actor o interesado")
    add_obj_prop("desempenaRol", "desempeña rol o empleo público", "Asigna a un interesado (B20_030) una o varias denominaciones según empleos públicos (B20_010).", domain=SITI["B20_030"], range_=SITI["B20_010"], inverse_id="rolDesempenadoPor", inverse_label="es rol desempeñado por")
    add_obj_prop("poseeDisciplina", "posee disciplina técnica", "Relaciona un actor o profesional con una o múltiples disciplinas profesionales (B20_020).", domain=Class_B20, range_=SITI["B20_020"], inverse_id="disciplinaAsignadaA", inverse_label="es disciplina asignada a")
    add_obj_prop("desempenaRolBIM", "desempeña rol GIS-BIM", "Asigna a un actor un rol en la gestión GIS-BIM (ej. Director, Coordinador, Auditor, Modelador BIM B20_040).", domain=Class_B20, range_=SITI["B20_040"], inverse_id="rolBIMDesempenadoPor", inverse_label="es rol GIS-BIM desempeñado por")
    add_obj_prop("tieneInteresadoAsociado", "tiene interesado asociado", "Permite que una entidad pública (B20_025) o proyecto vincule múltiples interesados internos o externos (B20_030).", domain=Class_B20, range_=SITI["B20_030"], inverse_id="interesadoAsociadoA", inverse_label="es interesado asociado a")

    # B40, B50, B30 (Actividades, Especificaciones, KPIs, Recursos, APU)
    add_obj_prop("regidoPorEspecificacionTecnica", "está regido por especificación técnica", "Conecta actividades e ítems de obra (B40) con especificaciones técnicas normativas (B50_005).", domain=Class_B40, range_=SITI["B50_005"], inverse_id="especificacionTecnicaAplicaA", inverse_label="es especificación técnica que aplica a")
    add_obj_prop("evaluadoPorKPI", "es evaluado por indicador KPI", "Vincula fases, procesos o actividades (B10, B40) con los indicadores de rendimiento y niveles de servicio KPI (B50_010).", domain=Class_B, range_=SITI["B50_010"], inverse_id="kpiEvalua", inverse_label="es KPI que evalúa")
    add_obj_prop("requiereRecursoOMaterial", "requiere recurso o material", "Asocia un proceso o actividad de obra (B40) con los materiales (B30_010), herramientas y equipos (B30_015) necesarios para su ejecución.", domain=Class_B40, range_=Class_B30, inverse_id="esRecursoRequeridoPara", inverse_label="es recurso requerido para")
    add_obj_prop("tieneItemPrecioUnitario", "tiene ítem de precio unitario", "Asocia un presupuesto o actividad de obra (B10, B40) con los ítems de precios unitarios de referencia distritales o nacionales (B40_015, B40_020).", domain=Class_B, range_=Class_B40, inverse_id="esItemPrecioUnitarioPara", inverse_label="es ítem de precio unitario para")

    # ==================================================================
    # 4.3. FASE 4: OBJECT PROPERTIES CRUZADAS (Lenguaje A <-> Lenguaje B)
    # ==================================================================
    add_obj_prop("sitiCrossRelation", "Relación cruzada SITI (A <-> B)", "Propiedad de objeto raíz abstracta cruzada entre entidades físicas del Lenguaje A y parámetros del Lenguaje B.", domain=Class_A, range_=Class_B, inverse_id="isCrossRelationFor", inverse_label="es relación cruzada inversa para")

    # Refinamiento Modal A20 -> A30
    add_obj_prop("tieneAreaModal", "tiene área de modalidad especializada", "Vincula una infraestructura (A20) con sus áreas (A30) respetando la modalidad de transporte.", domain=Class_A20, range_=Class_A30, inverse_id="areaModalPerteneceAInfraestructura", inverse_label="es área modal de infraestructura")

    # Fases de Proyecto (B10_015) aplicables a nivel de Áreas / Espacios
    add_obj_prop("enFaseDeProyecto", "está en fase de proyecto", "Establece la fase del ciclo de vida (B10_015) aplicable a nivel de área, espacio o elemento.", domain=Class_A, range_=SITI["B10_015"], inverse_id="faseDeProyectoAplicaAArea", inverse_label="es fase de proyecto aplicable a área/elemento")

    # Gestión del Riesgo (B10_020)
    add_obj_prop("sujetoARiesgo", "está sujeto a riesgo", "Vincula cualquier entidad del Lenguaje A (A10 a A50) con la gestión del riesgo (B10_020).", domain=Class_A, range_=SITI["B10_020"], inverse_id="riesgoAplicaAElemento", inverse_label="es riesgo aplicable a elemento")

    # Indicadores KPI Específicos (B50_010)
    add_obj_prop("evaluadoPorKPIEspecifico", "es evaluado por indicador KPI específico", "Permite evaluar con indicadores KPI (B50_010) a áreas, calzadas, sistemas o componentes específicos.", domain=Class_A, range_=SITI["B50_010"], inverse_id="kpiEspecificoEvaluaElemento", inverse_label="es KPI específico que evalúa elemento")

    # Materiales de Construcción (B30_010)
    add_obj_prop("compuestoPorMaterialEspecializado", "está compuesto por material especializado", "Vincula elementos físicos (A30, A40, A50) con materiales de construcción e insumos (B30_010).", domain=Class_A, range_=SITI["B30_010"], inverse_id="materialEspecializadoUsadoEn", inverse_label="es material especializado usado en")

    # Gobernanza Institucional (B20_025 / B20)
    add_obj_prop("gestionadoPorEntidadEjecutora", "es gestionado por entidad ejecutora", "Conecta un activo de infraestructura o área (A10, A20, A30) con la entidad pública ejecutora o dueña del proyecto (B20_025).", domain=Class_A, range_=SITI["B20_025"], inverse_id="entidadEjecutaActivo", inverse_label="es entidad ejecutora de activo")

    # Presupuestación por Precios Unitarios (B40 / B40_015 / B40_020)
    add_obj_prop("presupuestadoEnItemPrecios", "está presupuestado en ítem de precios unitarios", "Vincula elementos constructivos o componentes (A40, A50) con sus ítems de precios unitarios de referencia distritales o nacionales (B40).", domain=Class_A, range_=Class_B40, inverse_id="itemPreciosPresupuestaElemento", inverse_label="es ítem de precios que presupuesta elemento")

    # Actividades de Obra y Mantenimiento (B40)
    add_obj_prop("ejecutadoPorActividadDeObra", "es ejecutado o intervenido por actividad de obra", "Vincula espacios (A30), sistemas (A40) y componentes (A50) con actividades de obra, mantenimiento y seguridad vial (B40).", domain=Class_A, range_=Class_B40, inverse_id="actividadEjecutadaEnActivo", inverse_label="es actividad ejecutada en activo de infraestructura")

    # Maquinaria y Equipos de Construcción (B30_015)
    add_obj_prop("intervenidoConEquipo", "es construido o intervenido con equipo/maquinaria", "Asocia sistemas (A40) o componentes (A50) con la maquinaria y equipos de construcción (B30_015).", domain=Class_A, range_=SITI["B30_015"], inverse_id="equipoUtilizadoEnActivo", inverse_label="es maquinaria utilizada en construcción/mantenimiento")

    # Subsistema de Peajes, Aforos y Recaudación (A30_035_010_015 <-> A40_050 / A50 / B50)
    add_obj_prop("tieneSistemaPeaje", "tiene sistema de peaje vehicular", "Conecta la plaza o estación de peaje (A30_035_010_015) con el sistema operativo de recaudo y telepeaje (A40_050).", domain=Class_A30, range_=Class_A40, inverse_id="sistemaPeajeInstaladoEnPlaza", inverse_label="es sistema de peaje instalado en plaza")
    add_obj_prop("cuentaConSensorAforo", "cuenta con sensor o equipo de aforo", "Asocia la estación o carril de peaje (A30_035_010_015) con los equipos y sensores electrónicos de conteo vehicular (A50_035_005_030).", domain=Class_A30, range_=Class_A50, inverse_id="sensorAforoInstaladoEnEstacion", inverse_label="es sensor de aforo instalado en estación")
    add_obj_prop("aplicaEsquemaTarifario", "aplica esquema tarifario y tarifas diferenciales", "Vincula la estación de peaje con el sistema de gestión de tarifas dinámicas, descuentos y categorías comunitarias (A40_075_015_005).", domain=Class_A30, range_=Class_A40, inverse_id="esquemaTarifarioAplicaAEstacion", inverse_label="es esquema tarifario que aplica a estación")
    add_obj_prop("reportaMetricasOETR", "reporta métricas e indicadores de peaje OETR", "Conecta la estación de peaje con indicadores B50 identificados por campo, fuente y periodo. Trafico usa el conteo B50_010_035_020; no representa vehículos únicos, TPDM ni recaudo monetario.", domain=Class_A30, range_=Class_B50, inverse_id="metricasOETRReportadasPorEstacion", inverse_label="son métricas OETR reportadas por estación")

    # Subsistema de Interoperabilidad Ferroviaria (A30_015 <-> B30_015_020 / A40_145)
    add_obj_prop("operaConMaterialRodante", "opera con material rodante compatible", "Conecta un tramo de vía férrea o espacio de gálibo ferroviario (A30_015) con los equipos férreos y material rodante (B30_015_020 / IfcVehicle) compatibles en trocha, gálibo y carga por eje.", domain=Class_A30, range_=SITI["B30_015_020"], inverse_id="materialRodanteCompatibleCon", inverse_label="es material rodante compatible con vía o gálibo")
    add_obj_prop("controladoPorSistemaFerroviario", "está controlado por sistema ferroviario", "Vincula un área, desvío o vía férrea (A30_015) con los sistemas de señalización, enclavamiento y control de tráfico ferroviario (A40_145).", domain=Class_A30, range_=SITI["A40_145"], inverse_id="sistemaFerroviarioControlaArea", inverse_label="es sistema ferroviario que controla área o vía")

    # ==================================================================
    # 5. PROCESAMIENTO DE ARCHIVOS CSV Y GENERACIÓN DE CLASES
    # ==================================================================
    # ==================================================================
    # 5. PROCESAMIENTO DE ARCHIVOS CSV Y GENERACIÓN DE CLASES
    # ==================================================================
    csv_file_pairs = [
        ("capa1_taxonomia_A10.csv", "A10.csv"),
        ("capa1_taxonomia_A20.csv", "A20.csv"),
        ("capa1_taxonomia_A30.csv", "A30.csv"),
        ("capa1_taxonomia_A40.csv", "A40.csv"),
        ("capa1_taxonomia_A50.csv", "A50.csv"),
        ("capa1_taxonomia_B10.csv", "B10.csv"),
        ("capa1_taxonomia_B20.csv", "B20.csv"),
        ("capa1_taxonomia_B30.csv", "B30.csv"),
        ("capa1_taxonomia_B40.csv", "B40.csv"),
        ("capa1_taxonomia_B50.csv", "B50.csv")
    ]

    code_counts = {}
    total_processed = 0
    total_classes = 0

    # Sólo autoridad revisada: ningún alias heredado se convierte en evidencia.
    from collections import defaultdict
    reviewed_by_code = defaultdict(list)
    for alias_code, alias_lang, alias_text in registry.reviewed_aliases():
        reviewed_by_code[alias_code].append((alias_lang, alias_text))
    lexicon = getattr(registry, "lexicon", None)
    print(f"Expresiones revisadas por contrato: {sum(map(len, reviewed_by_code.values()))}; la validación técnica no demuestra equivalencia.")

    print("Iniciando procesamiento de los 10 archivos CSV de la taxonomía SITI (Capa 1)...")
    this_dir = str(registry.catalog_dir)
    target_dir = os.path.abspath(output_dir or this_dir)
    os.makedirs(target_dir, exist_ok=True)

    for primary, fallback in csv_file_pairs:
        candidates = [os.path.join(this_dir, primary)]
        filename = None
        for cand in candidates:
            if os.path.exists(cand):
                filename = cand
                break
        
        if not filename:
            raise ValueError(f"Falta fuente de la revisión fijada: {primary}")
        
        base_code = primary.replace("capa1_taxonomia_", "").replace(".csv", "")
        lenguaje_type = "A" if base_code.startswith("A") else "B"
        stack = {}  # mapa de nivel (1..7) -> IRI node

        with open(filename, encoding='utf-8-sig', errors='strict') as fp:
            reader = csv.DictReader(fp, delimiter=';')
            file_rows = 0

            for r in reader:
                total_processed += 1
                file_rows += 1

                lvl_str = r.get('Nivel', '').strip()
                code_raw = r.get('Código SITI', '').strip()
                desc = r.get('Descripción', '').strip()
                clas = r.get('Clasificación', '').strip()

                if not lvl_str or not code_raw:
                    continue

                lvl = int(lvl_str)
                code_sanitized = code_raw.replace(' ', '_').replace('/', '_')

                # Manejo de códigos repetidos para garantizar IRIs únicos sin pérdida de nodos
                if code_sanitized in ("A", "B"):
                    iri_key = code_sanitized
                elif code_sanitized in code_counts:
                    code_counts[code_sanitized] += 1
                    iri_key = f"{code_sanitized}_{code_counts[code_sanitized]}"
                else:
                    code_counts[code_sanitized] = 1
                    iri_key = code_sanitized

                # El contador de identidad ya avanzó: filtrar nunca renumera sufijos.
                if not registry.is_assignable(iri_key):
                    continue
                class_node = SITI[iri_key]
                g.add((class_node, SITI.selectable, Literal(True, datatype=XSD.boolean)))
                g.add((class_node, SITI.lifecycleStatus, Literal("active")))

                # Declarar como owl:Class y skos:Concept
                g.add((class_node, RDF.type, OWL.Class))
                g.add((class_node, RDF.type, SKOS.Concept))
                total_classes += 1

                # Anotaciones principales
                g.add((class_node, RDFS.label, Literal(desc, lang="es")))
                g.add((class_node, SKOS.prefLabel, Literal(desc, lang="es")))
                g.add((class_node, prop_codigo, Literal(code_raw)))
                g.add((class_node, prop_nivel, Literal(lvl, datatype=XSD.integer)))
                g.add((class_node, prop_clasificacion, Literal(clas)))
                g.add((class_node, prop_lenguaje, Literal(lenguaje_type)))
                g.add((class_node, prop_origen, Literal(f"{base_code}.csv")))

                definition = registry.definitions.get(iri_key)
                if definition:
                    g.add((class_node, SKOS.definition, Literal(definition['text'], lang='es')))
                    g.add((class_node, SITI.definitionSourceIds, Literal(json.dumps(definition['source_ids']))))
                for alias_lang, alias_text in reviewed_by_code.get(iri_key, []):
                    if not (alias_lang == 'es' and alias_text.casefold() == desc.casefold()):
                        g.add((class_node, SKOS.altLabel, Literal(alias_text, lang=alias_lang)))
                if lexicon:
                    lexical_evidence = lexicon.reviewed_by_code(iri_key)
                    if lexical_evidence:
                        g.add((class_node, SITI.lexicalEvidence, Literal(json.dumps(lexical_evidence, ensure_ascii=False, sort_keys=True))))
                alias_provenance = [item for item in registry.alias_reviews
                                    if item['code'] == iri_key and item.get('status') == 'reviewed']
                if alias_provenance:
                    g.add((class_node, SITI.aliasProvenance, Literal(json.dumps(alias_provenance, ensure_ascii=False))))

                # Fase 5: Anotaciones de Interoperabilidad IFC (ISO 16739-1:2024)
                mapping = registry.mapping(base_code, iri_key, desc)
                ifc_ent, ifc_pt, ifc_ps, ifc_desc_text = (
                    mapping[key] for key in ('entity', 'predefined_type', 'property_set', 'description'))
                g.add((class_node, SITI.ifcMappingStatus, Literal(mapping['status'])))
                g.add((class_node, SITI.ifcMappingSourceIds, Literal(json.dumps(mapping['source_ids']))))
                g.add((class_node, prop_ifc_entity, Literal(ifc_ent)))
                g.add((class_node, prop_ifc_ptype, Literal(ifc_pt)))
                g.add((class_node, prop_ifc_pset, Literal(ifc_ps)))
                g.add((class_node, prop_ifc_desc, Literal(ifc_desc_text, lang="es")))

                # Anotaciones de Georreferenciación GIS (CRS) y Referenciación Lineal (Abscisado ISO 19148 / IFC4x3)
                if base_code.startswith("A10") or base_code.startswith("A20") or base_code.startswith("A30"):
                    g.add((class_node, prop_ifc_gis_crs, Literal("Soporta georreferenciación espacial mediante IfcProjectedCRS (ISO 19111) y coordenadas EPSG (MAGNA-SIRGAS Colombia)", lang="es")))
                    g.add((class_node, prop_ifc_linear_ref, Literal("Soporta alineamiento 1D/2D/3D y abscisado lineal mediante IfcAlignment (ISO 19148)", lang="es")))
                    g.add((class_node, prop_ifc_gis_rep, Literal("Soporta representación semántica geográfica GIS-BIM mediante IfcGeographicElement e IfcSite", lang="es")))
                elif base_code.startswith("A40") or base_code.startswith("A50"):
                    g.add((class_node, prop_ifc_linear_ref, Literal("Ubicable por abscisado relativo en el alineamiento mediante IfcAlignmentReferenced", lang="es")))

                # Jerarquía (rdfs:subClassOf & skos:broader/narrower)
                if lvl > 1 and (lvl - 1) in stack:
                    parent_node = stack[lvl - 1]
                    g.add((class_node, RDFS.subClassOf, parent_node))
                    g.add((class_node, SKOS.broader, parent_node))
                    g.add((parent_node, SKOS.narrower, class_node))

                # Actualizar stack de padres por nivel
                stack[lvl] = class_node

                # Limpiar niveles superiores
                for k in list(stack.keys()):
                    if k > lvl:
                        del stack[k]

        print(f"  [+] {filename} ({base_code}): {file_rows} registros procesados.")

    # ==================================================================
    # Homologaciones internacionales skos:exactMatch (ERA, EULYNX, IFC 4.3 Add2)
    # ==================================================================
    # Las propuestas de exactMatch del JSON heredado no constituyen aprobación.
    # Conservamos las relaciones de la publicación fijada, sin activar otras.
    if fixed_artifacts is not None:
        from siti_semantic_build import previous_ontology_bytes
        prior_raw = previous_ontology_bytes(fixed_artifacts)
    else:
        prior_raw = registry.read_published_artifact('capa1_ontologia/capa1_siti_ontology.ttl')
    prior_graph = Graph().parse(data=prior_raw.decode('utf-8'), format='turtle')
    for subject, target in prior_graph.subject_objects(SKOS.exactMatch):
        if not isinstance(subject, URIRef) or not isinstance(target, URIRef):
            raise ValueError('Una equivalencia publicada exige URI explícitas.')
        g.add((SKOS.exactMatch, RDF.type, OWL.ObjectProperty))
        g.add((subject, RDF.type, OWL.NamedIndividual))
        g.add((target, RDF.type, OWL.NamedIndividual))
        g.add((subject, SKOS.exactMatch, target))

    # ==================================================================
    # Referencias históricas: resolubles, sin incorporación a jerarquía activa.
    for prop in (SITI.selectable, SITI.lifecycleStatus, SITI.legacyParent, SITI.assignmentReview,
                 SITI.ifcMappingStatus, SITI.ifcMappingSourceIds, SITI.definitionSourceIds,
                 SITI.legacyIfcEntity, SITI.legacyIfcPredefinedType, SITI.legacyIfcPropertySet,
                 SITI.sourceRegistry, SITI.aliasProvenance):
        g.add((prop, RDF.type, OWL.AnnotationProperty))
    g.add((URIRef(ONTOLOGY_IRI), SITI.sourceRegistry,
           Literal(json.dumps(registry.sources, ensure_ascii=False))))
    if lexicon:
        g.add((URIRef(ONTOLOGY_IRI), SITI.lexiconRevision, Literal(lexicon.revision)))
        g.add((URIRef(ONTOLOGY_IRI), SITI.lexiconSourceRegistry,
               Literal(json.dumps(lexicon.sources, ensure_ascii=False, sort_keys=True))))
    for item in registry.reference_catalog()["legacy_references"]:
        node = SITI[item["code"]]
        g.add((node, RDF.type, OWL.Class))
        g.add((node, RDF.type, SKOS.Concept))
        g.add((node, RDFS.label, Literal(item["name"], lang="es")))
        g.add((node, SKOS.prefLabel, Literal(item["name"], lang="es")))
        g.add((node, SITI.codigoSITI, Literal(item["raw_code"])))
        g.add((node, SITI.nivel, Literal(item["level"], datatype=XSD.integer)))
        g.add((node, SITI.clasificacion, Literal(item["classification"])))
        g.add((node, SITI.lenguaje, Literal(item["table_id"][0])))
        g.add((node, SITI.origenCSV, Literal(item["table_id"] + ".csv")))
        g.add((node, OWL.deprecated, Literal(True, datatype=XSD.boolean)))
        g.add((node, SITI.selectable, Literal(False, datatype=XSD.boolean)))
        g.add((node, SITI.lifecycleStatus, Literal("retired")))
        g.add((node, SITI.legacyParent, SITI[item["parent_code"]]))
        old_ifc = item.get('legacy_ifc_mapping', {})
        for prop, key in ((SITI.legacyIfcEntity, 'entity'),
                          (SITI.legacyIfcPredefinedType, 'predefined_type'),
                          (SITI.legacyIfcPropertySet, 'property_set')):
            if key in old_ifc:
                g.add((node, prop, Literal(old_ifc[key])))
        g.add((node, SITI.ifcMappingStatus, Literal('retired_not_assignable')))
        g.add((node, SITI.assignmentReview, Literal(json.dumps(item["review"], ensure_ascii=False))))

    # Contratos operacionales de composición y registros topológicos. No son
    # nuevas clases de activo ni importaciones de las ontologías externas.
    contract_path = os.path.join(this_dir, 'capa1_contratos_intermodales.json')
    if os.path.exists(contract_path):
        with open(contract_path, encoding='utf-8') as handle:
            intermodal = json.load(handle)
        g.add((ont_node, SITI.intermodalContractRevision, Literal(intermodal['revision'])))
        for code, contract in intermodal['property_contracts'].items():
            if not registry.lookup(code) or registry.lookup(code)['table_id'] != 'B50':
                raise ValueError('Contrato de propiedad no canónica: '+code)
            g.add((SITI[code], SITI.dataContract, Literal(json.dumps(contract, ensure_ascii=False,sort_keys=True))))
        add_obj_prop('composicionDirectaIntertabular', 'composición directa entre tablas',
            'Composición física directa entre activos de tablas A diferentes; el contrato rechaza ciclos y retornos a la tabla de un ancestro. No obliga a instanciar cinco niveles.', domain=Class_A, range_=Class_A)
        add_obj_prop('conexionTopologicaEntreExtremos', 'conexión topológica entre extremos',
            'Conexión entre registros de extremos C2. No afirma coincidencia XY ni permiso de circulación. El extremo no es un puerto logístico ni una clase de activo.',is_symmetric=True)
        add_obj_prop('navegacionDirigidaEntreExtremos', 'navegación dirigida entre extremos',
            'Enlace dirigido entre registros de extremos C2. Sus estados confirmado/desconocido/cerrado, fuentes y distancias se conservan; no certifica seguridad o factibilidad.')
        for name in ('tieneSubcomponente','esSubcomponenteDe'):
            g.add((SITI[name], OWL.deprecated, Literal(True,datatype=XSD.boolean)))
            g.add((SITI[name], SITI.operationalStatus, Literal('historical_not_assignable')))
            g.add((SITI[name], SKOS.scopeNote, Literal('URI histórica preservada. No admite nuevas afirmaciones de composición A50→A50 en SITI.',lang='es')))
        g.add((SITI.composicionDirectaIntertabular,SITI.contractSourceIds,
               Literal(json.dumps(intermodal['source_ids']))))

    # 6. RESTRICCIONES AXIOMÁTICAS Y MODALES
    # ==================================================================
    def add_all_values_from_restriction(subclass_node, on_property_node, to_class_node):
        res_node = BNode()
        g.add((res_node, RDF.type, OWL.Restriction))
        g.add((res_node, OWL.onProperty, on_property_node))
        g.add((res_node, OWL.allValuesFrom, to_class_node))
        g.add((subclass_node, RDFS.subClassOf, res_node))

    print("\nAplicando restricciones modales A20 -> A30...")
    modal_pairs = [
        ("A20_005", "A30_005"), # Aeroportuaria
        ("A20_010", "A30_010"), # Cable
        ("A20_015", "A30_015"), # Férrea
        ("A20_020", "A30_020"), # Fluvial
        ("A20_025", "A30_025"), # Marítima
        ("A20_030", "A30_030"), # Lacustre
        ("A20_035", "A30_035"), # Carretera
        ("A20_040", "A30_040")  # Otras/Intermodal
    ]

    prop_tieneAreaModal = SITI["tieneAreaModal"]
    for code_a20, code_a30 in modal_pairs:
        if SITI[code_a20] in g.subjects() and SITI[code_a30] in g.subjects():
            add_all_values_from_restriction(SITI[code_a20], prop_tieneAreaModal, SITI[code_a30])


    # ==================================================================
    # 6.B. AXIOMATIZACIÓN OWL 2 DL INTERTABULAR Y RECETAS PARA PROTÉGÉ
    # ==================================================================
    super_props_spec = [{'id': 'propiedadComposicionFisicaIntertabularA', 'label_es': 'Propiedad de composición física intertabular (lenguaje A)', 'label_en': 'Physical intertabular composition property (language A)', 'label_fr': 'Propriété de composition physique intertabulaire (langage A)', 'definition_es': 'Superpropiedad organizadora de la ontología SITI que agrupa las relaciones de composición física, alojamiento espacial y soporte funcional intertabular estrictamente acíclicas dentro del lenguaje físico A (A10 -> A20 -> A30 -> A40 -> A50), sin meronimia intratabular.', 'domain': 'A', 'range': 'A'}, {'id': 'propiedadAcoplamientoTransversalAB', 'label_es': 'Propiedad de acoplamiento transversal interlenguaje (A y B)', 'label_en': 'Cross-language coupling property (A and B)', 'label_fr': 'Propriété de couplage transversal inter-langages (A et B)', 'definition_es': 'Superpropiedad organizadora de la ontología SITI que agrupa los acoplamientos transversales entre entidades físicas del lenguaje A (A10 a A50) y facetas del lenguaje B (fases B10, actores B20, materiales y equipos B30, actividades B40 y propiedades e indicadores B50).', 'domain': None, 'range': None}, {'id': 'propiedadGobernanzaIntertabularB', 'label_es': 'Propiedad de gobernanza intertabular (lenguaje B)', 'label_en': 'Intertabular governance property (language B)', 'label_fr': 'Propriété de gouvernance intertabulaire (langage B)', 'definition_es': 'Superpropiedad organizadora de la ontología SITI que agrupa las relaciones de gobernanza contractual, supervisión institucional, consumo de recursos y evaluación paramétrica entre tablas distintas del lenguaje B (B10, B20, B30, B40 y B50).', 'domain': 'B', 'range': 'B'}]
    new_props_spec = [{'id': 'ejecutaOSupervisaProceso', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': None, 'label_es': 'ejecuta o supervisa proceso o actividad', 'label_en': 'executes or supervises process or activity', 'label_fr': 'exécute ou supervise un processus ou une activité', 'definition_es': 'Vincula un actor, rol o entidad institucional (B20) con las actividades de construcción, operación, mantenimiento o gestión (B40) que ejecuta o supervisa.', 'domain': 'B20', 'range': 'B40'}, {'id': 'regulaProcesoCicloVida', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': None, 'label_es': 'regula proceso del ciclo de vida', 'label_en': 'regulates lifecycle process', 'label_fr': 'régule le processus du cycle de vie', 'definition_es': 'Vincula un instrumento contractual, fase de proyecto o documento de gestión (B10) con los procesos y actividades (B40) que regula a lo largo del ciclo de vida.', 'domain': 'B10', 'range': 'B40'}, {'id': 'emiteDocumento', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'aplicaFormatoDocumental', 'label_es': 'emite documento o entregable oficial', 'label_en': 'issues official document or deliverable', 'label_fr': 'émet un document ou livrable officiel', 'definition_es': 'Subpropiedad especializada que vincula una entidad o actor (B20) con la emisión formal de un documento técnico, apéndice o acta contractual (B10).', 'domain': 'B20', 'range': 'B10'}, {'id': 'emiteOGobiernaDocumento', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'aplicaFormatoDocumental', 'label_es': 'emite o gobierna documento normativo o contractual', 'label_en': 'issues or governs normative or contractual document', 'label_fr': 'émet ou gouverne un document normatif ou contractuel', 'definition_es': 'Subpropiedad especializada que vincula una autoridad o actor institucional (B20) con los documentos normativos, manuales o apéndices contractuales (B10) bajo su gobernanza.', 'domain': 'B20', 'range': 'B10'}, {'id': 'consumeRecursoB30', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'requiereRecursoOMaterial', 'label_es': 'consume recurso o insumo de construcción (B30)', 'label_en': 'consumes construction resource or input (B30)', 'label_fr': 'consomme une ressource ou un intrant de construction (B30)', 'definition_es': 'Relación intertabular derivada de los análisis de precios unitarios (los APU) que vincula una actividad de obra (B40) con los materiales e insumos (B30) consumidos.', 'domain': 'B40', 'range': 'B30'}, {'id': 'consumeRecursoOEquipo', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'requiereRecursoOMaterial', 'label_es': 'consume recurso, material o equipo de obra', 'label_en': 'consumes construction resource, material or equipment', 'label_fr': 'consomme une ressource, un matériau ou un équipement de chantier', 'definition_es': 'Relación intertabular que vincula una actividad o ítem de obra (B40) con la maquinaria, herramientas o materiales (B30) requeridos para su ejecución.', 'domain': 'B40', 'range': 'B30'}, {'id': 'exigeIndicadorContractual', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'evaluadoPorKPI', 'label_es': 'exige indicador o parámetro contractual', 'label_en': 'requires contractual indicator or parameter', 'label_fr': 'exige un indicateur ou paramètre contractuel', 'definition_es': 'Vincula una fase, documento o proceso de gestión (B10, B40) con los indicadores de nivel de servicio y parámetros técnicos (B50) exigibles contractualmente.', 'domain': 'B', 'range': 'B50'}, {'id': 'restituyeIndicador', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'evaluadoPorKPI', 'label_es': 'restituye indicador de nivel de servicio', 'label_en': 'restores service level indicator', 'label_fr': 'restitue un indicateur de niveau de service', 'definition_es': 'Vincula una actividad de mantenimiento, rehabilitación o intervención (B40) con el indicador funcional o estructural (B50) cuyo umbral normativo restituye.', 'domain': 'B40', 'range': 'B50'}, {'id': 'restituyeOEvaluaIndicador', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'evaluadoPorKPI', 'label_es': 'restituye o evalúa indicador técnico', 'label_en': 'restores or evaluates technical indicator', 'label_fr': 'restitue ou évalue un indicateur technique', 'definition_es': 'Vincula una actividad de obra o auscultación (B40) con el indicador o parámetro técnico (B50) que evalúa o restituye.', 'domain': 'B40', 'range': 'B50'}, {'id': 'evaluadoPorIndicador', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'evaluadoPorKPI', 'label_es': 'es evaluado por indicador o parámetro (B50)', 'label_en': 'is evaluated by indicator or parameter (B50)', 'label_fr': 'est évalué par un indicateur ou paramètre (B50)', 'definition_es': 'Vincula una entidad de gestión o recurso (B10..B40) con los indicadores o parámetros técnicos (B50) que cuantifican su desempeño.', 'domain': 'B', 'range': 'B50'}, {'id': 'defineIndicador', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'kpiEvalua', 'label_es': 'define indicador o umbral normativo', 'label_en': 'defines indicator or normative threshold', 'label_fr': 'définit un indicateur ou seuil normatif', 'definition_es': 'Vincula un documento contractual o apéndice técnico (B10) con los indicadores de desempeño y umbrales técnicos (B50) que define formalmente.', 'domain': 'B10', 'range': 'B50'}, {'id': 'especificaMaterial', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'especificacionTecnicaAplicaA', 'label_es': 'especifica requisito técnico de material', 'label_en': 'specifies technical material requirement', 'label_fr': 'spécifie une exigence technique de matériau', 'definition_es': 'Vincula un insumo o material de construcción (B30) con las especificaciones técnicas y propiedades de ensayo (B50) que rigen su aceptación.', 'domain': 'B30', 'range': 'B50'}, {'id': 'regidoPorNorma', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'regidoPorEspecificacionTecnica', 'label_es': 'está regido por norma o especificación', 'label_en': 'is governed by standard or specification', 'label_fr': 'est régi par une norme ou spécification', 'definition_es': 'Vincula una actividad o entidad con la norma técnica o especificación (B10, B50) que regula su diseño, construcción o verificación.', 'domain': 'B', 'range': 'B50'}, {'id': 'auditaCumplimiento', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'desempenaRol', 'label_es': 'audita cumplimiento técnico o contractual', 'label_en': 'audits technical or contractual compliance', 'label_fr': 'audite la conformité technique ou contractuelle', 'definition_es': 'Vincula un rol de interventoría, supervisión o auditoría (B20) con las fases, entregables o indicadores (B10, B50) cuyo cumplimiento verifica.', 'domain': 'B20', 'range': 'B'}, {'id': 'ejecutaProceso', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'ejecutaOSupervisaProceso', 'label_es': 'ejecuta proceso operativo o constructivo', 'label_en': 'executes operational or construction process', 'label_fr': 'exécute un processus opérationnel ou de construction', 'definition_es': 'Vincula una entidad ejecutora o contratista (B20) con el proceso o actividad de obra (B40) que ejecuta directamente.', 'domain': 'B20', 'range': 'B40'}, {'id': 'exigeRequisitosEirLoin', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'requiereNivelInformacionLOIN', 'label_es': 'exige requisitos de intercambio de información (EIR/LOIN)', 'label_en': 'requires information exchange requirements (Eir/Loin)', 'label_fr': "exige des exigences d'échange d'informations (Eir/Loin)", 'definition_es': 'Vincula una entidad contratante (B20) con los requisitos de intercambio de información y nivel de información necesaria (B10) conforme a la serie ISO 19650.', 'domain': 'B20', 'range': 'B10'}, {'id': 'suscribeYEjecutaBep', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'ejecutaUsoBIM', 'label_es': 'suscribe y ejecuta plan de ejecución BIM (BEP)', 'label_en': 'subscribes and executes BIM execution plan (Bep)', 'label_fr': "souscrit et exécute le plan d'exécution BIM (Bep)", 'definition_es': 'Vincula al concesionario o contratista (B20) con la formulación y ejecución del plan de ejecución BIM (B10) del contrato.', 'domain': 'B20', 'range': 'B10'}, {'id': 'estructuraFlujoCde', 'super': 'propiedadGobernanzaIntertabularB', 'parent_prop': 'modeloBIMUsadoEnFase', 'label_es': 'estructura flujo de trabajo en entorno común de datos (CDE)', 'label_en': 'structures workflow in common data environment (Cde)', 'label_fr': "structure le flux de travail dans l'environnement de données commun (Cde)", 'definition_es': 'Vincula el contenedor o plan de información (B10) con los procesos de coordinación, revisión y publicación en el entorno común de datos (B40).', 'domain': 'B10', 'range': 'B40'}, {'id': 'contieneSistema', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'albergaElemento', 'label_es': 'contiene sistema o complejo de infraestructura (A10 -> A20)', 'label_en': 'contains infrastructure system or complex (A10 -> A20)', 'label_fr': "contient un système ou complexe d'infrastructure (A10 -> A20)", 'definition_es': 'Relación de composición física intertabular que vincula una zona geográfica o territorio (A10) con los complejos y sistemas de infraestructura (A20) que alberga.', 'domain': 'A10', 'range': 'A20'}, {'id': 'integraZonaEspacial', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'tieneAreaModal', 'label_es': 'integra zona o área espacial funcional (A20 -> A30)', 'label_en': 'integrates functional spatial zone or area (A20 -> A30)', 'label_fr': 'intègre une zone ou aire spatiale fonctionnelle (A20 -> A30)', 'definition_es': 'Relación de composición física intertabular que vincula una infraestructura o corredor (A20) con las áreas y espacios funcionales (A30) que lo conforman.', 'domain': 'A20', 'range': 'A30'}, {'id': 'integraElementoConstructivo', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'composicionDirectaIntertabular', 'label_es': 'integra elemento o sistema constructivo (A30 -> A40)', 'label_en': 'integrates constructive element or system (A30 -> A40)', 'label_fr': 'intègre un élément ou système constructif (A30 -> A40)', 'definition_es': 'Relación de composición física intertabular que vincula un área o espacio funcional (A30) con los sistemas e instalaciones operativas o constructivas (A40) dispuestos en él.', 'domain': 'A30', 'range': 'A40'}, {'id': 'alojaDirectamente', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'alojaElementoDirectamente', 'label_es': 'aloja directamente sistema o instalación (A30 -> A40)', 'label_en': 'directly hosts system or installation (A30 -> A40)', 'label_fr': 'héberge directement un système ou une installation (A30 -> A40)', 'definition_es': 'Relación de composición física intertabular que vincula un espacio funcional (A30) con el sistema constructivo o instalación (A40) que aloja directamente.', 'domain': 'A30', 'range': 'A40'}, {'id': 'soportaComponente', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'tieneComponenteEstructurante', 'label_es': 'soporta componente técnico funcional (A40 -> A50)', 'label_en': 'supports functional technical component (A40 -> A50)', 'label_fr': 'supporte un composant technique fonctionnel (A40 -> A50)', 'definition_es': 'Relación de composición física intertabular que vincula un sistema o instalación (A40) con los componentes técnicos funcionales (A50) que soporta o integra.', 'domain': 'A40', 'range': 'A50'}, {'id': 'tieneComponenteFuncional', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'constaDeCapaOMaterial', 'label_es': 'tiene componente técnico funcional (A30/A40 -> A50)', 'label_en': 'has functional technical component (A30/A40 -> A50)', 'label_fr': 'a un composant technique fonctionnel (A30/A40 -> A50)', 'definition_es': 'Relación de composición física intertabular que vincula un espacio funcional (A30) o sistema (A40) con sus componentes técnicos funcionales (A50) sin especificar material.', 'domain': 'A', 'range': 'A50'}, {'id': 'despliegaActivoFuncional', 'super': 'propiedadComposicionFisicaIntertabularA', 'parent_prop': 'albergaElemento', 'label_es': 'despliega activo o componente funcional (A30 -> A50)', 'label_en': 'deploys functional asset or component (A30 -> A50)', 'label_fr': 'déploie un actif ou composant fonctionnel (A30 -> A50)', 'definition_es': 'Relación de composición física intertabular que vincula un área o zona operativa (A30) con los sensores, dispositivos o componentes funcionales (A50) desplegados en ella.', 'domain': 'A30', 'range': 'A50'}, {'id': 'intervieneActivo', 'super': 'propiedadAcoplamientoTransversalAB', 'parent_prop': 'actividadEjecutadaEnActivo', 'label_es': 'interviene activo físico de infraestructura (B40 -> A)', 'label_en': 'intervenes physical infrastructure asset (B40 -> A)', 'label_fr': "intervient sur un actif physique d'infrastructure (B40 -> A)", 'definition_es': 'Relación de acoplamiento transversal que vincula una actividad de construcción, rehabilitación o mantenimiento (B40) con la entidad física del lenguaje A sobre la cual recae.', 'domain': 'B40', 'range': 'A'}]
    for sp in super_props_spec:
        sp_node = SITI[sp['id']]
        g.add((sp_node, RDF.type, OWL.ObjectProperty))
        g.add((sp_node, RDFS.label, Literal(sp['label_es'], lang='es')))
        g.add((sp_node, RDFS.label, Literal(sp['label_en'], lang='en')))
        g.add((sp_node, RDFS.label, Literal(sp['label_fr'], lang='fr')))
        g.add((sp_node, SKOS.definition, Literal(sp['definition_es'], lang='es')))
        g.add((sp_node, RDFS.comment, Literal(sp['definition_es'], lang='es')))
        if sp['domain']:
            g.add((sp_node, RDFS.domain, SITI[sp['domain']]))
        if sp['range']:
            g.add((sp_node, RDFS.range, SITI[sp['range']]))
    # Organizar propiedades existentes bajo las 3 super-propiedades para Protégé
    for existing_p in list(g.subjects(RDF.type, OWL.ObjectProperty)):
        if not isinstance(existing_p, URIRef) or not str(existing_p).startswith(str(SITI)):
            continue
        pname = str(existing_p)[len(str(SITI)):]
        if pname in {sp['id'] for sp in super_props_spec}:
            continue
        doms = [str(o)[len(str(SITI)):] for o in g.objects(existing_p, RDFS.domain) if isinstance(o, URIRef) and str(o).startswith(str(SITI))]
        rngs = [str(o)[len(str(SITI)):] for o in g.objects(existing_p, RDFS.range) if isinstance(o, URIRef) and str(o).startswith(str(SITI))]
        d0 = doms[0][0] if doms else ''
        r0 = rngs[0][0] if rngs else ''
        if d0 == 'A' and r0 == 'A':
            g.add((existing_p, RDFS.subPropertyOf, SITI['propiedadComposicionFisicaIntertabularA']))
        elif d0 == 'B' and r0 == 'B':
            g.add((existing_p, RDFS.subPropertyOf, SITI['propiedadGobernanzaIntertabularB']))
        else:
            g.add((existing_p, RDFS.subPropertyOf, SITI['propiedadAcoplamientoTransversalAB']))
    # Declarar nuevas ObjectProperty de C2 y recetas
    for np in new_props_spec:
        np_node = SITI[np['id']]
        g.add((np_node, RDF.type, OWL.ObjectProperty))
        g.add((np_node, RDFS.subPropertyOf, SITI[np['super']]))
        if np.get('parent_prop'):
            g.add((np_node, RDFS.subPropertyOf, SITI[np['parent_prop']]))
        g.add((np_node, RDFS.label, Literal(np['label_es'], lang='es')))
        g.add((np_node, RDFS.label, Literal(np['label_en'], lang='en')))
        g.add((np_node, RDFS.label, Literal(np['label_fr'], lang='fr')))
        g.add((np_node, SKOS.definition, Literal(np['definition_es'], lang='es')))
        g.add((np_node, RDFS.comment, Literal(np['definition_es'], lang='es')))
        if np.get('domain'):
            g.add((np_node, RDFS.domain, SITI[np['domain']]))
        if np.get('range'):
            g.add((np_node, RDFS.range, SITI[np['range']]))
    g.add((SITI['vinculoIntertabularCertificado'], RDF.type, OWL.AnnotationProperty))
    g.add((SITI['vinculoIntertabularCertificado'], RDFS.label, Literal('Vínculo intertabular certificado en C1 y C2', lang='es')))
    g.add((SITI['recetaEnsamblajeIntertabular'], RDF.type, OWL.AnnotationProperty))
    g.add((SITI['recetaEnsamblajeIntertabular'], RDFS.label, Literal('Receta canónica de ensamblaje intertabular', lang='es')))
    if os.path.exists(contract_path):
        for edge in intermodal.get('c2_intertabular_edges', []):
            src_code = edge['source_siti_code']
            tgt_code = edge['target_siti_code']
            prop_local = edge['owl_object_property'].split(':', 1)[-1]
            if not registry.lookup(src_code) or not registry.lookup(tgt_code):
                continue
            res_bn = BNode()
            g.add((res_bn, RDF.type, OWL.Restriction))
            g.add((res_bn, OWL.onProperty, SITI[prop_local]))
            g.add((res_bn, OWL.someValuesFrom, SITI[tgt_code]))
            g.add((SITI[src_code], RDFS.subClassOf, res_bn))
            g.add((SITI[src_code], SITI['vinculoIntertabularCertificado'], Literal(json.dumps({
                'relation_id': edge['relation_id'],
                'cypher_edge_type': edge['cypher_edge_type'],
                'owl_object_property': edge['owl_object_property'],
                'target_siti_code': tgt_code,
                'evidence_count': edge.get('evidence_count', 1)
            }, ensure_ascii=False, sort_keys=True))))
        for rec in intermodal.get('c2_assembly_recipes', []):
            rec_id_safe = rec['recipe_id'].replace('-', '_')
            rec_prop = SITI['ensamblajeReceta_' + rec_id_safe]
            super_prop = SITI['propiedadComposicionFisicaIntertabularA'] if rec['recipe_id'].startswith('REC-A') else SITI['propiedadGobernanzaIntertabularB']
            g.add((rec_prop, RDF.type, OWL.ObjectProperty))
            g.add((rec_prop, RDFS.subPropertyOf, super_prop))
            g.add((rec_prop, RDFS.label, Literal(f"ensamblaje intertabular {rec['recipe_id']}: {rec['recipe_name']}", lang='es')))
            g.add((rec_prop, RDFS.label, Literal(f"intertabular assembly {rec['recipe_id']} ({rec['chain_pattern']})", lang='en')))
            g.add((rec_prop, RDFS.label, Literal(f"assemblage intertabulaire {rec['recipe_id']} ({rec['chain_pattern']})", lang='fr')))
            g.add((rec_prop, SKOS.definition, Literal(rec['meronymy_proof'], lang='es')))
            g.add((rec_prop, RDFS.comment, Literal(rec['meronymy_proof'], lang='es')))
            first_code = rec.get('a10_code', '')
            last_code = rec.get('a50_code', '')
            if first_code and last_code:
                g.add((rec_prop, RDFS.domain, SITI[first_code.split('_')[0]]))
                g.add((rec_prop, RDFS.range, SITI[last_code.split('_')[0]]))
                if registry.lookup(first_code) and registry.lookup(last_code):
                    rec_bn = BNode()
                    g.add((rec_bn, RDF.type, OWL.Restriction))
                    g.add((rec_bn, OWL.onProperty, rec_prop))
                    g.add((rec_bn, OWL.someValuesFrom, SITI[last_code]))
                    g.add((SITI[first_code], RDFS.subClassOf, rec_bn))
                    g.add((SITI[first_code], SITI['recetaEnsamblajeIntertabular'], Literal(json.dumps(rec, ensure_ascii=False, sort_keys=True))))

    # Completar declaraciones W3C del vocabulario ya utilizado. El papel SKOS
    # y la clase OWL comparten URI mediante punning, no identidad de activo.
    from siti_rdf_contract import declare_profile_terms, validate_order_assertions, ORDER_PAIRS
    declare_profile_terms(g)
    for names in ORDER_PAIRS:
        for name in names:
            g.add((SITI[name],SITI.assertedOrderConstraint,
                Literal('Aserciones de orden acíclicas verificadas por siti_rdf_contract.validate_order_assertions; no axioma de propiedad simple.')))
            g.add((SITI[name],SITI.formalProfileSource,
                URIRef('https://www.w3.org/TR/owl2-syntax/#Global_Restrictions_on_Axioms_in_OWL_2_DL')))
    validate_order_assertions(g)

    print(f"\nProcesamiento completo: {total_processed} registros CSV, {total_classes} ocurrencias procesadas; las clases únicas se informan por el catálogo de identidad.")

    # ==================================================================
    # 7. SERIALIZACIÓN DE LA ONTOLOGÍA (CAPA 1)
    # ==================================================================
    ttl_output = os.path.join(target_dir, "capa1_siti_ontology.ttl")
    owl_output = os.path.join(target_dir, "capa1_siti_ontology.owl")

    print(f"\nSerializando ontología a formato Turtle ({ttl_output})...")
    g.serialize(destination=ttl_output, format="turtle")
    print(f"  [OK] Generado: {ttl_output} ({os.path.getsize(ttl_output) / (1024*1024):.2f} MB)")

    print(f"Serializando ontología a formato RDF/XML ({owl_output})...")
    g.serialize(destination=owl_output, format="xml")
    print(f"  [OK] Generado: {owl_output} ({os.path.getsize(owl_output) / (1024*1024):.2f} MB)")

    # Los kits son consumidores explícitos de la publicación. Esta función no
    # ejecuta otros generadores ni modifica C3 como efecto de serializar C1.
    return len(g), total_processed, total_classes

if __name__ == "__main__":
    triples_count, processed_count, classes_count = create_siti_ontology()
    print(f"\nOntología SITI regenerada exitosamente con {triples_count} triplas y {classes_count} clases.")
