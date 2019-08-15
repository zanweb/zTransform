__author__ = "zanweb <zanweb@163.com>"


class OracleData_SQL:
    def __init__(self):
        self.show_fields = []
        self.where_fields = []
        self.value_fields = []
        self.sql = ''

    def insert_sql(self, values, user):
        # values 为读取的字典数组
        # user 为登录用户
        # 返回多行插入的sql语句
        self.sql = 'INSERT INTO [dbo].[OracleData] VALUES '
        for value in values:
            tmp_sql = "('"
            tmp_sql += value['ORG'] + "',"
            tmp_sql += str(value['Order Num']) + ",'"
            tmp_sql += value['Item Cat'] + "',"
            tmp_sql += str(value['Batch Id']) + ","
            tmp_sql += str(value['Sort Id']) + ","
            tmp_sql += str(value['Seq']) + ","
            tmp_sql += str(value['Dept']) + ",'"
            tmp_sql += value['Res'] + "','"
            tmp_sql += value['Res Desc'] + "','"
            tmp_sql += value['Raw Material'] + "',"
            tmp_sql += str(value['Coil Width']) + ",'"
            tmp_sql += value['Coil Color'] + "','"
            tmp_sql += value['Sort Complete'] + "','"
            tmp_sql += value['Fa Job'] + "','"
            tmp_sql += value['Fa Item'] + "','"
            tmp_sql += value['Item Desc'] + "','"
            tmp_sql += value['Mark No'] + "','"
            if value['Prd Width']:
                tmp_sql = tmp_sql[0:-1] + str(value['Prd Width']) + ",'"
            else:
                tmp_sql = tmp_sql[0:-1] + 'NULL,'
            tmp_sql += str(value['Stack']) + ","
            tmp_sql += str(value['Fa Seq']) + ","
            tmp_sql += str(value['Line Seq']) + ","
            tmp_sql += str(value['Fa Qty']) + ",'"
            tmp_sql += value['Bundle'] + "',"
            tmp_sql += str(value['Unit Length']) + ",'"
            tmp_sql += user
            tmp_sql += "'),'"
            self.sql += tmp_sql
        self.sql = self.sql[:-2]
        return self.sql

    def insert_sql_head(self, head=None):
        if not head:
            self.sql = "INSERT INTO [dbo].[OracleData] VALUES (%s, %d, %s, %d, %d, %d, %s, %s, %s, " \
                       "%s, %d, %s, %s, %s, %s, %s, %s, %d, %d, %d, %d, %d, %s, %d, %s, %s, %s)"
        return self.sql

    def insert_sql_values(self, values, user, user_group):
        tmp_list = []
        for value in values:
            tmp_v = (
                value['ORG'], value['Order Num'], value['Item Cat'], value['Batch Id'], value['Sort Id'], value['Seq'],
                value['Dept'],
                value['Res'], value['Res Desc'], value['Raw Material'], value['Coil Width'], value['Coil Color'],
                value['Sort Complete'], value['Fa Job'],
                value['Fa Item'], value['Item Desc'], value['Mark No'], value['Prd Width'], value['Stack'],
                value['Fa Seq'],
                value['Line Seq'],
                value['Fa Qty'], value['Bundle'], value['Unit Length'], str(user), str(user_group), None)
            # print(tmp_v)
            tmp_list.append(tmp_v)
        return tmp_list

    def select_sql_head(self, show_fields, params_name=None, params_type=None):
        self.sql = 'SELECT '
        tmp_sql = ''
        for field in show_fields:
            tmp_sql += field + ','
        tmp_sql = tmp_sql[0:-1]
        self.sql += tmp_sql
        self.sql += ' FROM [dbo].[OracleData]'
        if params_name:
            self.sql += ' WHERE '
            tmp_param = ''
            for i in range(len(params_name)):
                # print(i)
                tmp_param += params_name[i] + '=' + params_type[i] + ' AND '
            self.sql += tmp_param[0:-5]

            self.sql += ' ORDER BY [Unit Length] DESC'
        return self.sql

    def select_sql_in_auto(self, tuple_auto):
        sql = 'SELECT *, convert(int, dbo.GET_NUMBER2([Bundle])) as BundleNo FROM [dbo].[OracleData] WHERE [AutoNo] IN '
        tmp_sql = ''
        for index in range(len(tuple_auto)):
            tmp_sql += '%d ,'
        sql += '(' + tmp_sql[0:-1] + ')'
        sql += ' ORDER BY BundleNo'
        return sql

    def update_sql_head(self, update_fields, update_values, params_name=None, params_type=None):
        r_sql = 'UPDATE [dbo].[OracleData] SET '
        tmp_sql = ''
        for index in range(len(update_fields)):
            tmp_sql += str(update_fields[index]) + "='"+ update_values[index] + "',"
        r_sql += tmp_sql[0:-1]
        tmp_sql = ''
        for index in range(len(params_name)):
            tmp_sql += params_name[index] + ','
        r_sql += ' WHERE (' + tmp_sql[0:-1] + ')'
        r_sql += ' IN '
        tmp_sql = ''
        for index in range(len(params_type)):
            tmp_sql += params_type[index] + ','
        r_sql += '(' + tmp_sql[0:-1] + ')'
        self.sql = r_sql
        return self.sql


class User_SQL:
    def __init__(self):
        self.show_fields = []
        self.where_fields = []
        self.value_fields = []
        self.sql = ''

    def select_sql_head(self, show_fields, params_name=None, params_type=None):
        self.sql = 'SELECT '
        tmp_sql = ''
        for field in show_fields:
            tmp_sql += field + ','
        tmp_sql = tmp_sql[0:-1]
        self.sql += tmp_sql
        self.sql += ' FROM [dbo].[User]'
        if params_name:
            self.sql += ' WHERE '
            tmp_param = ''
            for i in range(len(params_name)):
                # print(i)
                tmp_param += params_name[i] + '=' + params_type[i] + ' AND '
            self.sql += tmp_param[0:-5]
        return self.sql
