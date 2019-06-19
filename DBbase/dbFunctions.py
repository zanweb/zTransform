__author__ = "zanweb <zanweb@163.com>"

from DBbase import dbunit, genSQL
from Zfile import zCSV


def oracle_data_import(user, passwd, host, database, user_group, file_with_path):
    oracle_file = zCSV.CsvFile(file_with_path)
    oracle_file.del_lines_begin(8)
    print(oracle_file)
    oracle_info = oracle_file.get_oracle_data()
    # pprint(oracle_info)
    sql = genSQL.OracleData_SQL().insert_sql_head()
    # print(sql)
    s_values = genSQL.OracleData_SQL().insert_sql_values(oracle_info, user, user_group)
    db = dbunit.DBUnit(user, passwd, host, database)
    # print(s_values)
    insert_return = db.write(sql, s_values)
    if insert_return == -1:
        print('Insert Data Error!')
    else:
        print('Insert Data OK!')
    return insert_return


def oracle_data_read(user, passwd, host, database, show_fields, params_name, params_type, params):
    db = dbunit.DBUnit(user, passwd, host, database)
    sql = genSQL.OracleData_SQL().select_sql_head(show_fields, params_name, params_type)
    # pprint(sql)
    read_return = db.read(sql, params)
    # if read_return:
    #     pprint(read_return)
    return read_return


def user_info_read(user, passwd, host, database, show_fields, params_name, params_type, params):
    db = dbunit.DBUnit(user, passwd, host, database)
    sql = genSQL.User_SQL().select_sql_head(show_fields, params_name, params_type)
    # pprint(sql)
    read_return = db.read(sql, params)
    # if read_return:
    #     pprint(read_return)
    return read_return


def oracle_data_update(user, passwd, host, database, update_fields, update_values, params_name, params_type, params,
                       option=None):
    db = dbunit.DBUnit(user, passwd, host, database)
    if not option:
        sql = genSQL.OracleData_SQL().update_sql_head(update_fields, update_values, params_name, params_type)
        # write_return = sql
        write_return = db.write(sql, params)
    return write_return


if __name__ == '__main__':
    print('begin test =====================>')
    # test04 ----- oracle_data_update(user, passwd, host, database, update_fields, update_values, params_name, params_type, params,
    #                        option=None):
    user = 'zyqsh'
    passwd = 'zyqsh123'
    host = 'zanweb\stlsojsvr04'
    database = 'DFactory'
    update_fields = ['[Sort Complete]']
    update_values = ['Y']
    params_name = ['AutoNo']
    params_type = ['%s']
    params = ['4', '5']

    back = oracle_data_update(user, passwd, host, database, update_fields, update_values, params_name, params_type,
                              params,
                              option=None)
    print(back)
    # test03 ----- user_info_read (user, passwd, host, database, show_fields, params_name, params_type, params):----
    # 返回： [{'UserGroup': 'sh        ', 'UserRes': 'all       '}]
    # user = 'zyqsh'
    # passwd = 'zyqsh123'
    # host = 'zanweb\stlsojsvr04'
    # database = 'DFactory'
    # show_fields = ['UserGroup', 'UserRes']
    # params_name = ['UserName']
    # params_type = ['%s']
    # params = ('zyqsh')
    #
    # user_info_read(user, passwd, host, database, show_fields, params_name, params_type, params)

    # test02 ----- oracle_data_import (user, passwd, host, database, file_with_path): -----------------------
    # from operator import itemgetter
    # show_fields = ['[Raw Material]', '[Order Num]', "CASE WHEN [ORG] = 'LKQ' THEN [Mark No] ELSE [Fa Item]  END AS Item",
    #                '[Fa Qty]', '[Fa Job]', '[Sort Id]', '[Sort Complete]']
    # params_name = [r"[Sort Complete]"]
    # params_type = ['%s']
    # params = (' ')
    # user = 'zyq'
    # passwd = 'zyq123'
    # host = 'zanweb\stlsojsvr04'
    # database = 'DFactory'
    # rs = oracle_data_read(user, passwd, host, database, show_fields, params_name, params_type, params)
    # pprint(rs)
    # rs_by_material = sorted(rs, key=itemgetter('Raw Material', 'Order Num'))
    # pprint(rs_by_material)

    # test01----oracle_data_import(user, passwd, host, database, file_with_path):-----------------------------------
    # oracle_data_import('zyqsh', 'zyqsh123', 'zanweb\stlsojsvr04', 'DFactory', 'sh', 'E:/Desktop/100000.CSV')

    #
