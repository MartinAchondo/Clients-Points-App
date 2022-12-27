import os
import json
import pyodbc

class DB_Queries():

    filename = os.path.join(os.getcwd(),'database_sqlserver','user.json')
    with open(filename,"r") as file_json:
        data = json.load(file_json)
        key = data["connection"]
    sqlserver_connection_key = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(
        key['driver'],
        key['host'],
        key['database'],
        key['user'],
        key['password'])
    sqlserver_connection = None
    sqlserver_status = False

    def __init__(self):
        if not DB_Queries.sqlserver_connection is None:
            try:
                DB_Queries.connect_server()
            except Exception as e: 
                print(e)            
    
    def sqlserver_create_connection(query_function):
        def wrapper(self,*kargs,**kwargs):
            if DB_Queries.sqlserver_status and DB_Queries.is_connected():
                ans = query_function(self,*kargs,**kwargs)
                DB_Queries.disconnect_server()
                return ans
            else:
                try: 
                    DB_Queries.connect_server()
                    ans = query_function(self,*kargs,**kwargs)
                    DB_Queries.disconnect_server()
                    return ans
                except Exception as e:
                    print(e)
        return wrapper
    
    @classmethod
    def connect_server(cls):
        try:
            cls.sqlserver_connection = pyodbc.connect(cls.sqlserver_connection_key)
            cls.sqlserver_status = True
        except Exception as e:
            print(e)

    @classmethod
    def disconnect_server(cls):
        if cls.sqlserver_status == True:
            try:
                cls.sqlserver_connection.close()
            except Exception as e:
                print(e)

    @classmethod
    def is_connected(cls):
        try:
            cur = cls.sqlserver_connection.cursor()
            cur.close()
            return True
        except Exception as e:
            cls.sqlserver_status = False
            return False

    @sqlserver_create_connection
    def sqlserver_query(self,sql):
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(sql)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return False

    @sqlserver_create_connection
    def sqlserver_query_dic(self,sql):
        try:
            cur = self.sqlserver_connection.cursor(dictionary=True)
            cur.execute(sql)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return False

    @sqlserver_create_connection
    def sqlserver_query_name(self,query_name):
        root = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(root,'sql','queries.sql')
        with open(filename,'r') as fd:
            sqlfile = fd.read()
        sqlquerys = sqlfile.split('--')
        sqlquerys.pop(0)
        names = sqlquerys[::2]
        querys = sqlquerys[1::2]
        if query_name in names:
            index = names.index(query_name)
        else:
            return []
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(querys[index])
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []

    @sqlserver_create_connection
    def sqlserver_query_name_data(self,query_name,data):
        root = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(root,'queries.sql')
        with open(filename,'r') as fd:
            sqlfile = fd.read()
        sqlquerys = sqlfile.split('--')
        sqlquerys.pop(0)
        names = sqlquerys[::2]
        querys = sqlquerys[1::2]
        if query_name in names:
            index = names.index(query_name)
        else:
            return []
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(querys[index],data)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []
        
    @sqlserver_create_connection
    def sqlserver_query_name_dic(self,query_name):
        root = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(root,'sql','queries.sql')
        with open(filename,'r') as fd:
            sqlfile = fd.read()
        sqlquerys = sqlfile.split('--')
        sqlquerys.pop(0)
        names = sqlquerys[::2]
        querys = sqlquerys[1::2]
        if query_name in names:
            index = names.index(query_name)
        else:
            return []
        try:
            cur = self.sqlserver_connection.cursor(dictionary=True)
            cur.execute(querys[index])
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []

    @sqlserver_create_connection
    def sqlserver_query_columnas(self,sql):
        try:
            cur = self.sqlserver_connection.cursor(dictionary=True)
            cur.execute(sql)
            datos = cur.fetchone()
            self.sqlserver_connection.commit()
            ans = datos.keys()
            cur.close()
            return ans
        except Exception as e:
            print(e)
            return False 

    @sqlserver_create_connection
    def sqlserver_contar(self,tabla):
        sql = '''SELECT COUNT(*) FROM {}'''.format(tabla)
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(sql)
            datos = cur.fetchone()
            self.sqlserver_connection.commit()
            cur.close()
            return datos[0]
        except Exception as e:
            print(e)
            return False

    @sqlserver_create_connection
    def sqlserver_get_todos(self,tabla):
        sql = '''
            SELECT * FROM {}
            '''.format(tabla)
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(sql)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []   

    @sqlserver_create_connection
    def sqlserver_get_todos_dic(self,tabla):
        sql = '''
            SELECT * FROM {}
            '''.format(tabla)
        try:
            cur = self.sqlserver_connection.cursor(dictionary=True)
            cur.execute(sql)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []  

    @sqlserver_create_connection
    def sqlserver_get_algunos(self,data_filtro,tabla):
        sql = '''
            SELECT * FROM {}
            '''.format(tabla)
        sql_where, data_filtro = self.sqlserver_WHERE(data_filtro)
        sql = sql + sql_where
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(sql,data_filtro)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []    

    @sqlserver_create_connection
    def sqlserver_get_algunos_dic(self,data_filtro,tabla):
        sql = '''
            SELECT * FROM {}
            '''.format(tabla)
        sql_where, data_filtro = self.sqlserver_WHERE(data_filtro)
        sql = sql + sql_where
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(sql,data_filtro)
            datos = cur.fetchall()
            keys = [column[0] for column in cur.description]
            ans = list()
            for row in datos:
                ans.append(dict(zip(keys,row)))
            self.sqlserver_connection.commit()
            cur.close()
            return ans
        except Exception as e:
            print(e)
            return []    

    @sqlserver_create_connection
    def sqlserver_get_bycol(self,cols,data_filtro,tabla):
        sql = '''
            SELECT {} FROM {}
            '''.format(','.join(cols),tabla)
        sql_where, data_filtro = self.sqlserver_WHERE(data_filtro)
        sql = sql + sql_where
        try:
            cur = self.sqlserver_connection.cursor()
            print(sql)
            cur.execute(sql,data_filtro)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return []    

    @sqlserver_create_connection
    def sqlserver_get_bycol_dic(self,cols,data_filtro,tabla):
        sql = '''
            SELECT {} FROM {}
            '''.format(','.join(cols),tabla)
        sql_where, data_filtro = self.sqlserver_WHERE(data_filtro)
        sql = sql + sql_where
        try:
            cur = self.sqlserver_connection.cursor(dictionary=True)
            cur.execute(sql,data_filtro)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return [] 

    #[[['fecha','lugar'],'ventas'],[['tipo','costo'],'inventario'],[['tipo'],'codigos']],'codigo',{'cantidad':1},db.sqlserver_create_connection
    @sqlserver_create_connection
    def sqlserver_get_n_tablas(self,data,union,filtro):
        sql,data_filtro = self.JOIN(data,union,filtro)
        try:
            cur = self.sqlserver_connection.cursor()
            cur.execute(sql,data_filtro)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return [] 

    @sqlserver_create_connection
    def sqlserver_get_n_tablas_dic(self,data,union,filtro):
        sql,data_filtro = self.JOIN(data,union,filtro)
        try:
            cur = self.sqlserver_connection.cursor(dictionary=True)
            cur.execute(sql,data_filtro)
            datos = cur.fetchall()
            self.sqlserver_connection.commit()
            cur.close()
            return datos
        except Exception as e:
            print(e)
            return [] 

    @classmethod
    def JOIN(cls,data,union,filtro):
        L_get = list()
        L_tablas = list()
        for datax,tablax in data:
            L_tablas.append(tablax)
            tablax = [tablax]
            tablax *= len(datax)
            add_t = lambda s1,s2: s1 + "." + s2
            data_n = list(map(add_t,tablax,datax))
            L_get.append(data_n)
        tabla1 = L_tablas.pop(0)
        sql = '''SELECT '''
        sql_gets = ''''''
        for tipos in L_get:
            for data_y in tipos:
                sql_gets = sql_gets + data_y +','
        sql_gets = sql_gets[:-1]
        sql_from = ''' FROM {}'''.format(tabla1)
        sql = sql + sql_gets + sql_from
        sql_join = '''''' 
        for tablas in L_tablas:
            sql_join += ''' INNER JOIN {}'''.format(tablas)
            x1 = tabla1 + '.' + union
            x2 = tablas + '.' + union 
            sql_join += ''' ON {}={}'''.format(x1,x2)
        sql += sql_join
        dic_filtro = dict()
        for filtrox in filtro:
            filtro_n =  tabla1 + '.' + filtrox
            dic_filtro[filtro_n] = filtro[filtrox]
        sql_where,data_filtro = cls.sqlserver_WHERE(dic_filtro) 
        sql += ' ' + sql_where
        return (sql,data_filtro)

    @staticmethod
    def sqlserver_WHERE(data_filtro):
        iter = True
        data = dict()
        sql = ''''''
        values = list()
        for llaves in data_filtro.keys():
            if iter:
                sql = sql + '''WHERE {0} = ? '''.format(llaves)
                values.append(data_filtro[llaves])
                iter = False
            else:
                sql = sql + '''AND {0} = ? '''.format(llaves)
                values.append(data_filtro[llaves])
        return sql,values

    @staticmethod
    def SET(data_nueva):
        iter = True
        data = dict()
        sql = ''''''
        for llaves in data_nueva.keys():
            if iter:
                sql = sql + '''SET {} = %({}n)s '''.format(llaves, llaves)
                llaves_nueva = llaves + 'n'
                data[llaves_nueva] = data_nueva[llaves]
                iter = False
            else:
                sql = sql + ''', {} = %({}n)s '''.format(llaves,llaves)
                llaves_nueva = llaves + 'n'
                data[llaves_nueva] = data_nueva[llaves]
        return sql, data 


if __name__=='__main__':
    db = DB_Queries()
    A = db.sqlserver_get_algunos_dic({'ENDO':'10982868'},'MAEEDO')
    for row in A:
        print(row)
        print('-------------')
    #print(db.sqlserver_query('SELECT ENDO FROM MAEEDO LIMIT 20'))

    