#
# draft
#

TBLS_EXCLUDE = ['refs', 'trans', 'enums', 'information_schema_catalog_name', 'check_constraint_routine_usage', 'applicable_roles',
                'administrable_role_authorizations','collation_character_set_applicability', 'attributes', 'check_constraints',
                'character_sets', 'collations', 'column_domain_usage', 'column_column_usage', 'column_privileges',
                'column_udt_usage', 'columns', 'constraint_column_usage', 'schemata', 'constraint_table_usage',
                'domain_constraints', 'sql_packages', 'domain_udt_usage', 'sequences', 'domains', 'enabled_roles',
                'key_column_usage', 'parameters', 'referential_constraints', 'sql_features', 'role_column_grants',
                'routine_privileges', 'role_routine_grants', 'routines', 'sql_implementation_info', 'sql_parts',
                'sql_languages', 'sql_sizing', 'sql_sizing_profiles', 'table_constraints', 'table_privileges',
                'role_table_grants', 'views', 'tables', 'transforms', 'triggered_update_columns', '_pg_foreign_servers',
                'triggers', 'data_type_privileges', 'udt_privileges', 'role_udt_grants', 'usage_privileges', 'element_types',
                'role_usage_grants', 'user_defined_types', '_pg_foreign_table_columns', 'view_column_usage', 'view_routine_usage',
                'view_table_usage', 'foreign_server_options', 'column_options', '_pg_foreign_data_wrappers',
                'foreign_data_wrapper_options', 'foreign_tables', 'foreign_data_wrappers', 'foreign_servers',
                'foreign_table_options', 'user_mappings', 'user_mapping_options']

DRILLS = {
    'tbls': {'canal': ['zona', 'subzona', 'agente']}
}

TYPES = {
    'character varying': 'S',
    'character': 'S',
    'integer': 'I',
    'real': 'P',
    'double precision': 'F',
    'money': 'C',
    'date': 'D',
    'timestamp with time zone': 'T',
    'boolean': 'B',
    'ARRAY': 'ARRAY',
    'json': 'JSON',
    'USER-DEFINED': 'ENUM'
}

Q_DROP = """
    DROP TABLE flds;
    DROP TABLE enums;
    DROP TABLE refs;
    DROP TABLE tbls;
    DROP TYPE aligns;
"""

Q_CREATE = """
    CREATE TYPE aligns AS ENUM ('Left', 'Center', 'Right');
    
    CREATE TABLE tbls (
        tbl varchar(64) primary key,
        name varchar(64),
        keys TEXT [],
        descf varchar(64),
        drills json
    );

    CREATE TABLE flds (
        tbl varchar(64) NOT NULL references tbls(tbl),
        fld varchar(64) NOT NULL,
        name varchar(64),
        type varchar(64),
        size char(16),
        frmt char(16),
        ronly boolean,
        align aligns,
        PRIMARY KEY(tbl, fld)
    );
    
    CREATE TABLE refs (
        tbl varchar(64) NOT NULL references tbls(tbl),
        fld varchar(64) NOT NULL,
        tbl_ref varchar(64) NOT NULL references tbls(tbl),
        fld_ref varchar(64) NOT NULL
    );
    
    CREATE TABLE enums (
        name varchar(64) NOT NULL,
        values TEXT []
    );
    
"""

Q_TBLS = """
    SELECT table_name FROM information_schema.tables;
"""

Q_FLDS_ = f"""
    SELECT table_name as tbl, column_name as fld, column_name as name, data_type as type, character_maximum_length as size
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_name IN 
"""

Q_KEYS = """
    SELECT tc.table_name as tbl, c.column_name as fld
    FROM information_schema.table_constraints tc 
    JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
    JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
        AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
    WHERE constraint_type = 'PRIMARY KEY';
"""

Q_REFS = """
    SELECT
        tc.table_name as tbl, 
        kcu.column_name as fld, 
        ccu.table_name AS tbl_ref,
        ccu.column_name AS fld_ref
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
          AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY' and tc.constraint_name ='flds_tbl_fkey';
"""

Q_ENUMS = """
    select t.typname as ename,  
           e.enumlabel as evalue
    from pg_type t 
       join pg_enum e on t.oid = e.enumtypid  
       join pg_catalog.pg_namespace n ON n.oid = t.typnamespace;
"""
async def build_meta(db):
    for q in Q_DROP.split(";"): await db.query(q)
    for q in Q_CREATE.split(";"): await db.query(q)
    
    tbls = await db.query(Q_TBLS)
    tbls_list = [e['table_name'] for e in tbls
            if e['table_name'] not in TBLS_EXCLUDE and not e['table_name'].startswith('pg') and not e['table_name'].startswith('_pg')]
    keys = await db.query(Q_KEYS)
    tbls = [{'tbl': e, 'name': e, 'keys': [e1['fld'] for e1 in keys if e1['tbl']==e], 'drills': DRILLS[e] if e in DRILLS else {}}
            for e in tbls_list]
    await db.insert_rows('tbls', tbls, delete=False)
    
    TBLS_LIST = ', '.join([f'\'{e}\'' for e in tbls_list])
    Q_FLDS = f'{Q_FLDS_} ({TBLS_LIST});'
    flds = await db.query(Q_FLDS)
    for fld in flds:
        fld['name'] = fld['name'].title()
        fld['type'] = TYPES[fld['type']]
        fld['align'] = 'Left' if fld['type'] in ['S', 'D', 'T'] else 'Right'
    await db.insert_rows('flds', flds, delete=True)
        
    enums = await db.query(Q_ENUMS)
    enums = [{'name': e, 'values': [e1['evalue'] for e1 in enums if e1['ename']==e]} for e in set([e['ename'] for e in enums])]
    await db.insert_rows('enums', enums, delete=True)
    
    refs = await db.query(Q_REFS)
    await db.insert_rows('refs', refs, delete=True)

async def update_meta(db, meta):
    for tbl in meta['tables']:
        if 'fields' not in meta['tables'][tbl]: continue
        for fld in meta['tables'][tbl]['fields']:
            d = {'tbl': tbl, 'fld': fld}
            for attr in meta['tables'][tbl]['fields'][fld]:
                d[attr] = meta['tables'][tbl]['fields'][fld][attr]
            res = await db.update('flds', ['tbl', 'fld'], d)

async def get_meta(db):
    tbls = await db.select('tbls')
    if tbls is None: return None
    flds = await db.select('flds')
    if flds is None: return None
    meta = {'tables': {e['tbl']: {'table': e, 'fields': {e1['fld']: e1 for e1 in flds if e1['tbl']==e['tbl']}} for e in tbls}}
    return meta