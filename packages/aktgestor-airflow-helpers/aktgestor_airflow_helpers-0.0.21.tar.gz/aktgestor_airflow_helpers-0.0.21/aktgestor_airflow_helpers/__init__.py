from jinjasql import JinjaSql
import re
jinja = JinjaSql(param_style='pyformat')

def read_sql_file(file_path,params = None):
    with open(file_path, 'r') as f:
        sql = f.read()
        if params == None:
            return {'sql':sql}
        query, bind_params = jinja.prepare_query(sql, params)
        return {'sql' : query, 'parameters' : bind_params}

def get_table_updated_at(hook, control_table, table_name):
    sql = f"SELECT updated_at FROM {control_table} where tablename = '{table_name}'; \n"
    datetime_str = (hook.get_first(sql))[0].strftime('%Y-%m-%d %H:%M:%S')
    return datetime_str

def set_table_updated_at(hook,control_table, table_name, datetime_str):
    sql = f"UPDATE {control_table} SET updated_at = '{datetime_str}' WHERE tablename = '{table_name}'; \n"
    hook.run(sql)
  
def get_dbtime_now(hook):
    sql = "SELECT NOW() - INTERVAL 3 HOUR as timenow FROM DUAL"
    return (hook.get_first(sql))[0].strftime('%Y-%m-%d %H:%M:%S')

def get_etl_definitions(hook,control_table, table_name):
    sql = f"select tablename,updated_at,type,primary_keys,active from {control_table} where tablename = '{table_name}';"
    data = hook.get_first(sql)
    table_name = data[0]
    updated_at = data[1].strftime('%Y-%m-%d %H:%M:%S')
    type = data[2]
    primary_keys = data[3].split(',')
    active = data[4]
    return {'table_name':table_name, 'updated_at':updated_at, 'type':type, 'primary_keys':primary_keys, 'active':active}

def get_update_table_sql(arn, bucket, tenant_subdomain, datamart, file, columns, primary_keys, target_table):
    columns = ','.join(columns)
    """
    Retorna a query para atualizar a tabela
    arn: arn do s3
    bucket: nome do bucket
    conn_id: nome da conexão do airflow
    datamart: nome do datamart
    file: nome do arquivo
    columns: colunas da tabela
    primary_keys: chaves primárias da tabela
    """

    sql_insert = """

    CREATE temp TABLE stage_{target_table} (LIKE {target_table});

    COPY stage_{target_table} ({columns})
        FROM 's3://{bucket}/{tenant_subdomain}/{datamart}/{target_table}/{file}' -- file url
        iam_role '{arn}'
        csv;

    BEGIN TRANSACTION;

        DELETE FROM {target_table}
        USING stage_{target_table}
        WHERE {where_clause};

        INSERT INTO {target_table} 
        SELECT * FROM stage_{target_table};

    END TRANSACTION;

    DROP TABLE stage_{target_table}; 

    """
    where_clause = ' AND '.join([f'{target_table}.{key} = stage_{target_table}.{key}' for key in primary_keys])

    sql = sql_insert.format(arn=arn,target_table=target_table, columns=columns, bucket=bucket, tenant_subdomain=tenant_subdomain, datamart=datamart, file=file, primary_keys=primary_keys, where_clause=where_clause)
    return [item for item in sql.split(';')][:-1]

def get_columns_from_sql(sql):
    """
    Retorna as colunas da tabela baseado no sql de update
    """
    def removeNestedParentheses(s):
        ret = ''
        skip = 0
        for i in s:
            if i == '(':
                skip += 1
            elif i == ')'and skip > 0:
                skip -= 1
            elif skip == 0:
                ret += i
        return ret
    result = removeNestedParentheses(sql)
    result = result.split('select')[1].split('from')[0].replace('\'','').replace('\"','').split(',')
    result = [col.split(' ')[-1].strip() for col in result]
    result = [col for col in result if len(col)>0]
    result = [col.split('.')[-1] for col in result]
    return result

def sql_parser(sql, params, dialect= 'mysql'):
    """
    Parses SQL template and replaces placeholders with values.
    :param sql: SQL template
    :param params: dictionary of parameters
    :return: SQL string
    """

    # get param name inside {{}}
    param_name = set(re.findall(r'\{\{(.*?)\}\}', sql))
    print(param_name)

    params_positions = {}

    for param in param_name:
        # count param occurrences in sql
        params_positions[param] =[(m.start(), m.end()) for m in re.finditer(r'\{\{' + param + r'\}\}', sql)]

    print(params_positions)

    # numberize params
    keys = list(params.keys())
    for key in keys:
        if len(params_positions[key]) > 1:
            positions_to_add = 0
            for i, position_value in enumerate(params_positions[key]):
                numbered_param = key + '__' + str(i)
                sql = sql[:position_value[0]+2+positions_to_add] + numbered_param + sql[position_value[1]-2+positions_to_add:]
                positions_to_add += len('__' + str(i))
                params[numbered_param] = params[key]
            del params[key]


    # replace {{}} with sql placeholder
    if dialect == 'mysql':
        sql = sql.replace('{{', '%(')
        sql = sql.replace('}}', ')s')
    elif dialect == 'postgres':
        sql = sql.replace('{{', '$(')
        sql = sql.replace('}}', ')s')
    return(sql, params)