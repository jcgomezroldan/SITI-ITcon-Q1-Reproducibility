// ==============================================================================
// SITI - CAPA 2: GRAFO DE PROPIEDADES (LPG / NEO4J) - VERSIÓN AFINADA Y AUDITADA
// Archivo DDL: siti_lpg_schema.cypher
// 
// Incorpora:
// 1. Estándar de Identificadores Híbridos:
//    - Clases Taxonómicas Canónicas: UUID v5 (Determinista RFC 4122/9562 basado en Namespace SITI).
//    - Nodos de Instancia y Telemetría: UUID v7 (Secuencial Time-Ordered 128-bit RFC 9562).
// 2. Restricciones e Índices de Coalescencia y Rendimiento.
// 3. Aristas Temporales con Propiedades de Estado Operativo Dinámico (Vialidad en Emergencias).
// 4. Configuración Neosemantics (n10s) para Inferencia Directa en Neo4j.
// ==============================================================================

// ------------------------------------------------------------------------------
// 1. RESTRICCIONES DE INTEGRIDAD Y UNICIDAD (CONSTRAINTS)
// ------------------------------------------------------------------------------

CREATE CONSTRAINT siti_node_uuid_unique IF NOT EXISTS
FOR (n:SITI_Node)
REQUIRE n.uuid IS UNIQUE;

CREATE CONSTRAINT siti_code_unique IF NOT EXISTS
FOR (n:SITI_Node)
REQUIRE n.codigoSITI IS UNIQUE;

// ------------------------------------------------------------------------------
// 2. ÍNDICES DE RENDIMIENTO Y ADYACENCIA
// ------------------------------------------------------------------------------

CREATE INDEX siti_node_nivel_idx IF NOT EXISTS
FOR (n:SITI_Node)
ON (n.nivel);

CREATE INDEX siti_node_ifc_entity_idx IF NOT EXISTS
FOR (n:SITI_Node)
ON (n.ifcEntity);

CREATE INDEX siti_node_tabla_idx IF NOT EXISTS
FOR (n:SITI_Node)
ON (n.tablaOrigen);

CREATE INDEX siti_node_uuid_version_idx IF NOT EXISTS
FOR (n:SITI_Node)
ON (n.uuidVersion);

CREATE FULLTEXT INDEX siti_node_search_idx IF NOT EXISTS
FOR (n:SITI_Node)
ON EACH [n.nombre, n.codigoSITI, n.ifcMappingDescription];

// ------------------------------------------------------------------------------
// 3. CONFIGURACIÓN DEL MOTOR NEOSEMANTICS (n10s) PARA INFERENCIA NATIVA EN CAPA 2
// ------------------------------------------------------------------------------

CALL n10s.graphconfig.init({
  handleVocabUris: 'SHORTEN',
  handleMultival: 'ARRAY',
  multivalPropList: ['http://www.semanticweb.org/jcgr/SITI/ifcPropertySet'],
  keepLangTag: true,
  handleRDFTypes: 'LABELS'
});

CALL n10s.nsprefixes.add("siti", "http://www.semanticweb.org/jcgr/SITI/");
CALL n10s.nsprefixes.add("skos", "http://www.w3.org/2004/02/skos/core#");
CALL n10s.nsprefixes.add("owl", "http://www.w3.org/2002/07/owl#");

// ------------------------------------------------------------------------------
// 4. ESQUEMA DE PROPIEDADES DINÁMICAS EN ARISTAS (GRAFO TEMPORAL DE VIALIDAD)
// ------------------------------------------------------------------------------
//
// Las aristas topológicas y de contigüidad longitudinal/transversal admiten:
//   - estadoOperativo:       'HABILITADO' | 'CERRADO_POR_EMERGENCIA' | 'PASO_RESTRINGIDO' | 'EN_MANTENIMIENTO'
//   - velocidadOperativaKmH: Float (ej. 80.0, 30.0, 0.0)
//   - capacidadVehicularH:   Integer (vehículos/hora)
//   - validoDesde:           DateTime (ISO 8601 UTC)
//   - validoHasta:           DateTime (ISO 8601 UTC)
//   - motivoRestriccion:     String (ej. 'Derrumbe K58', 'Mantenimiento Preventivo')
//

// ------------------------------------------------------------------------------
// 5. METAMODELO DE PEAJES, AFOROS Y RECAUDO EN CAPA 2
// ------------------------------------------------------------------------------

CREATE CONSTRAINT peaje_id_unique IF NOT EXISTS
FOR (p:Peaje)
REQUIRE p.idPeaje IS UNIQUE;

CREATE CONSTRAINT reporte_peaje_id_unique IF NOT EXISTS
FOR (r:ReporteMensualPeaje)
REQUIRE r.idReporte IS UNIQUE;

CREATE INDEX peaje_divipola_idx IF NOT EXISTS
FOR (p:Peaje)
ON (p.divipola);

CREATE INDEX peaje_estado_operativo_idx IF NOT EXISTS
FOR (p:Peaje)
ON (p.estadoOperativo);

CREATE INDEX categoria_tarifaria_codigo_idx IF NOT EXISTS
FOR (c:CategoriaTarifaria)
ON (c.codigo);

// Relaciones Topológicas de Peaje:
//   (:Proyecto)-[:CONTIENE_ESTACION_PEAJE]->(:Peaje)
//   (:Peaje)-[:APLICA_TARIFA {tarifaCOP: Float, vigenteDesde: Date}]->(:CategoriaTarifaria)
//   (:Peaje)-[:REGISTRA_REPORTE_MENSUAL {periodo: 'YYYY-MM', traficoTotal: Integer, recaudoTotal: Float, tpdm: Float}]->(:ReporteMensualPeaje)
//   (:TramoVial)-[:TIENE_PEAJE_EN_PK {abscisaKm: Float}]->(:Peaje)

// ------------------------------------------------------------------------------
// 6. METAMODELO DE IDENTIDAD, JURISDICCIÓN ESPACIAL Y GOBERNANZA (SITI_IDENTIDAD)
// ------------------------------------------------------------------------------

CREATE CONSTRAINT identidad_usuario_id_unique IF NOT EXISTS
FOR (u:IdentidadUsuarioSITI)
REQUIRE u.id_usuario_siti IS UNIQUE;

CREATE CONSTRAINT identidad_usuario_login_unique IF NOT EXISTS
FOR (u:IdentidadUsuarioSITI)
REQUIRE u.usuario_login IS UNIQUE;

CREATE CONSTRAINT concesion_jurisdiccion_a10_unique IF NOT EXISTS
FOR (c:ConcesionJurisdiccionA10)
REQUIRE c.codigo_concesion_a10 IS UNIQUE;

CREATE CONSTRAINT proposito_misional_pbac_unique IF NOT EXISTS
FOR (p:PropositoMisionalPBAC)
REQUIRE p.codigo_proposito_pbac IS UNIQUE;

CREATE INDEX identidad_usuario_nivel_idx IF NOT EXISTS
FOR (u:IdentidadUsuarioSITI)
ON (u.nivel_acceso_siti);

CREATE INDEX identidad_usuario_rol_b20_idx IF NOT EXISTS
FOR (u:IdentidadUsuarioSITI)
ON (u.codigo_rol_b20);

// Relaciones Topológicas e Intertabulares de Identidad (Estación 1):
//   (:IdentidadUsuarioSITI)-[:CLASIFICADO_EN_ROL_B20 {codigo_entidad_b20: String, codigo_rol_b20: String}]->(:SITI_Node {tablaOrigen: 'B20_Roles'})
//   (:IdentidadUsuarioSITI)-[:TIENE_JURISDICCION_CONCESION_A10 {geocerca_wkb_Activa: Boolean, srid: 9377}]->(:ConcesionJurisdiccionA10)
//   (:IdentidadUsuarioSITI)-[:AUTORIZADO_PBAC_Y_EDICION {permisos_edicion_json: String, cuota_token_bucket_max: Float}]->(:PropositoMisionalPBAC)


