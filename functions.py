import datetime
from database_sqlite.crud import DB_Queries as DB_SQLite
from database_sqlserver.crud import DB_Queries as DB_SQLserver
import database_sqlite.base as dbx
import os
from dateutil.relativedelta import relativedelta
import pandas as pd
import xlsxwriter


class Client(DB_SQLite,DB_SQLserver):

    def __init__(self,data):
        super().__init__()
        self.rut = str(data['rut'])
        self.multiplier = 0.02
        self.venc_months = relativedelta(months=+12)
        self.mensaje_existe = 'Cliente ya Existe'
        self.mensaje_no_random = 'Debe crear a cliente en random'
        self.mensaje_no_base = 'Cliente no Existe'

        self.rut_0 = False
        id_ = self.sqlite_query('SELECT id FROM clients_info WHERE rut = "{}"'.format(str(self.rut)))
        if len(id_)!=0:
            self.id = id_[0][0]
            bool_ref2 = self.sqlite_query('SELECT referido_bool,id_referido FROM clients_points WHERE id_client = {}'.format(self.id))
            self.ref_bool,self.id_ref = bool_ref2[0]
        else:
            if len(data)<2:
                data['referido'] = '0'
            self.id = 0
            if data['referido'] != "0":
                rut_ref = str(data['referido'])
                id_2 = self.sqlite_query('SELECT id FROM clients_info WHERE rut = "{}"'.format(rut_ref))
                print(id_2,rut_ref)
                self.id_ref = id_2[0][0]
                self.ref_bool = True
            else: 
                self.id_ref = 0
                self.ref_bool = False

        
    def check_random(self):
        cliente = self.sqlserver_get_algunos_dic({'RTEN': self.rut},'MAEEN')
        if len(cliente)==0:
            return False,[]
        else:
            return True,cliente

    def check_base(self):
        cliente = self.sqlite_get_algunos({'rut':self.rut},'clients_info')
        if len(cliente)==0:
            return False
        else:
            return True

    def check_base2(self):
        ans = self.check_base()
        if ans:
            return ['',ans]
        else:
            return ['Cliente no existe',False]

    def create(self,cliente):
        cliente = cliente[0]
        data = {
            'rut': str(self.rut),
            'phone': cliente['FOEN'],
            'name': cliente['NOKOEN'],
            'mail': cliente['EMAILCOMER']
        }
        ans = self.sqlite_crear_dato(data,'clients_info')
        if ans == False:
            return False
        id_client = ans
        points = 0
        data = {
            'id_client': id_client,
            'points': points,
            'date_creation': datetime.date.today(),
            'date_last_update': datetime.date.today(),
            'time_grab': 0,
            'referido_bool': self.ref_bool,
            'id_referido': self.id_ref
        }
        
        ans = self.sqlite_crear_dato(data,'clients_points')

        data_rec = {
            'id_client': id_client,
            'type_trans': 'crear',
            'date_trans': datetime.datetime.now(),
            'monto': points,
            'saldo': points
        }
        ans2 = self.add_record(data_rec)
        return ans
        
    def create_verify_new(self):
        base = self.check_base()
        if base:
            return [self.mensaje_existe,False]
        random,cliente = self.check_random()
        if not random:
            return [self.mensaje_no_random,False]
        numero = str(cliente[0]['FOEN']).replace(' ','')
        nombre = str(cliente[0]['NOKOEN']).replace(' ','')
        mail = str(cliente[0]['EMAILCOMER']).replace(' ','')
        if numero=='' or nombre=='' or mail=='':
            return ['Faltan datos del cliente en Random. Agregar datos en Random y luego crear cliente', False]
        ans = self.create(cliente)
        if ans:
            return ['',True]
        return ['Error inseperado',False]

    def calculate_purchases_update(self):
        data = self.sqlite_get_algunos_dic({'id_client':self.id},'clients_points')
        fecha_update = data[0]['date_last_update']
        hora_update = data[0]['time_grab']
        dt = datetime.datetime.fromisoformat(fecha_update)
        fecha_update = dt
        ans = self.sqlserver_query_name_data('Pedir_ventas_fecha',[str(self.rut),fecha_update,'FCV','NCV','BLV'])
        newsum = 0
        #print(ans,self.rut)
        if len(ans)==0:
            return (int(newsum),int(hora_update))
        if fecha_update.date()==datetime.date.today():
            L_horas= [int(hora_update)]
        else:
            L_horas = [0]
        for valor,tipo,nudo,fecha,hora in ans:
            if self.check_pago_dia({'doc':str(tipo)+str(nudo),'fecha':fecha,'monto':valor}) or tipo=='NCV':
                nud_str = str(nudo)
                if len(nud_str)!=0:
                    if nud_str[0]!='V' and nud_str[0]!='v':
                        if fecha==fecha_update and hora>int(hora_update):
                            if tipo=='NCV':
                                newsum -= valor*self.multiplier
                                ans4 = self.cargar_vencimiento(-int(valor*self.multiplier),fecha.date())
                            else:
                                newsum += valor*self.multiplier
                                ans4 = self.cargar_vencimiento(int(valor*self.multiplier),fecha.date())
                                if self.ref_bool:
                                    self.add_ref_points(valor,fecha.date())
                        elif fecha>fecha_update:
                            if tipo=='NCV':
                                newsum -= valor*self.multiplier
                                ans4 = self.cargar_vencimiento(-int(valor*self.multiplier),fecha.date())
                            else:
                                newsum += valor*self.multiplier
                                ans4 = self.cargar_vencimiento(int(valor*self.multiplier),fecha.date())
                                if self.ref_bool:
                                    self.add_ref_points(valor,fecha.date())
                        if fecha.date()==datetime.date.today():
                            L_horas.append(hora)
        horagrab = max(L_horas)
        return (int(newsum),horagrab)

    def add_ref_points(self,valor,fecha):
        puntos_ref = self.sqlite_get_algunos_dic({'id_client':self.id_ref},'clients_points')[0]
        print(puntos_ref)
        new_points = int(int(puntos_ref['points']) + int(valor)*self.multiplier)
        self.sqlite_actualizar({'points': new_points},{'id_client':self.id_ref},'clients_points')

        data_rec = {
            'id_client': self.id_ref,
            'type_trans': 'referidos',
            'date_trans': datetime.datetime.now(),
            'monto': int(int(valor)*self.multiplier),
            'saldo': new_points
        }
        ans2 = self.add_record(data_rec)
        ans3 = self.cargar_vencimiento_ref(int(int(valor)*self.multiplier),fecha) # vencimiento al otro
        self.ref_bool = False
        self.sqlite_actualizar({'referido_bool': False},{'id_client':self.id},'clients_points')

    def check_pago_dia(self,data):
        ans = self.sqlserver_query_name_data('Pedir_pagos_dia',[data['doc']])
        sum_pay = 0
        for pagado,fecha in ans:
            if fecha == data['fecha']:
                sum_pay += int(pagado)
        if int(sum_pay)>=int(data['monto']):
            return True
        else:
            return False

    def update_points(self):
        newsum,hora = self.calculate_purchases_update()
        old_points = self.sqlite_query('SELECT points FROM clients_points WHERE id_client = {}'.format(self.id))[0][0]
        resta = self.check_venc()
        new_points = old_points + newsum - resta
        ans = self.sqlite_actualizar({'points': new_points,'date_last_update': datetime.date.today(),'time_grab':hora},{'id_client':self.id},'clients_points')

        data_rec = {
            'id_client': self.id,
            'type_trans': 'actualizar',
            'date_trans': datetime.datetime.now(),
            'monto': newsum,
            'saldo': old_points+newsum
        }
        if newsum!=0:
            ans2 = self.add_record(data_rec)
        
        data_rec = {
            'id_client': self.id,
            'type_trans': 'vencimiento',
            'date_trans': datetime.datetime.now(),
            'monto': -1*resta,
            'saldo': new_points
        }
        if resta!=0:
            ans2 = self.add_record(data_rec)

        return ans

    def update_client(self):
        base = self.check_base()
        if not base:
            return [self.mensaje_no_base,False]
        random,_ = self.check_random()
        if not random:
            return [self.mensaje_no_random,False]
        ans = self.update_points()
        if ans:
            return ['',ans]
        return ['Error inseperado',ans]

    def check_venc(self):
        data = self.sqlite_query('SELECT * FROM vencimientos WHERE id_client={} ORDER BY date_venc ASC'.format(self.id))
        resta = 0
        hoy = datetime.date.today()
        for id_,_,puntos,date_venc in data:
            if datetime.date.fromisoformat(date_venc)<hoy:
                resta += int(puntos)
                ans = self.sqlite_borrar({'id':id_},'vencimientos')
        return resta

    def get_last_venc(self):
        data = self.sqlite_query('SELECT puntos,date_venc FROM vencimientos WHERE id_client={} ORDER BY date_venc ASC'.format(self.id))
        return data

    def cargar_vencimiento(self,points,fecha):
        fecha = fecha + self.venc_months
        data = {
            'id_client': self.id,
            'puntos': points,
            'date_venc': fecha
        }
        ans = self.sqlite_crear_dato(data,'vencimientos')
        return ans

    def cargar_vencimiento_ref(self,points,fecha):
        fecha = fecha + self.venc_months
        data = {
            'id_client': self.id_ref,
            'puntos': points,
            'date_venc': fecha
        }
        ans = self.sqlite_crear_dato(data,'vencimientos')
        return ans


    def get_all(self):
        ans0 = self.update_client()
        data1 = self.sqlite_get_algunos_dic({'id':self.id},'clients_info')
        data2 = self.sqlite_get_algunos_dic({'id_client':self.id},'clients_points')
        return [data1,data2]

    def get_client(self):
        base = self.check_base()
        if not base:
            return [self.mensaje_no_base,False]
        random,_ = self.check_random()
        if not random:
            return [self.mensaje_no_random,False]
        ans = self.get_all()
        if ans:
            return ['',ans]
        return ['Error inseperado',ans]

    def get_points(self):
        ans0 = self.update_client()
        ans = self.sqlite_get_algunos_dic({'id_client':self.id},'clients_points')
        points = ans[0]['points']
        return [points]

    def add_transaction(self,data):
        points = data['points']
        old_points = self.sqlite_query('SELECT points FROM clients_points WHERE id_client = {}'.format(self.id))[0][0]
        new_points = old_points - int(points)
        ans = self.sqlite_actualizar({'points': new_points,'date_last_update': datetime.date.today()},{'id_client':self.id},'clients_points')
        if ans:
            ans4 = self.update_venc(points)
            data_rec = {
                'id_client': self.id,
                'type_trans': 'canjear',
                'date_trans': datetime.datetime.now(),
                'monto': -1*int(points),
                'saldo': new_points
            }
            ans2 = self.add_record(data_rec)
            ans3 = self.print_record(data_rec,ans2)

            return ['Puntos Canjeados',ans]
        else:
            return ['Error Inseperado',ans]

    def update_venc(self,points):
        total = int(points)
        data = self.sqlite_query('SELECT * FROM vencimientos WHERE id_client={} ORDER BY date_venc ASC'.format(self.id))
        resta = 0
        L_id = list()
        for id_,_,puntos,_ in data:
            val = int(puntos)
            if val-total>0:
                ans = self.sqlite_actualizar({'puntos':val-total},{'id':id_},'vencimientos')
                break
            elif val-total==0:
                ans = self.sqlite_borrar({'id':id_},'vencimientos')
                break
            elif val-total<0:
                total -= val
                ans = self.sqlite_borrar({'id':id_},'vencimientos')
        return True
        

    def print_record(self,data,id_r):
        ans = self.sqlite_get_algunos_dic({'id':self.id},'clients_info')
        path_file = os.getcwd()
        name_file = 'record_{}_{}.txt'.format(str(id_r),str(ans[0]['rut']))
        path_file = os.path.join(path_file,'OUTPUT','RECORDS',name_file)
        print(path_file)
        with open(path_file,'w') as f:
            f.write('CLUB DE BENEFICIOS'+'\n')
            f.write('BIJIT MATERIALES'+'\n')
            f.write('\n')
            f.write('REGISTRO DE CANJE DE PUNTOS')
            f.write('\n')
            f.write('\n')
            f.write('Fecha: ')
            f.write(str(datetime.date.today()))
            f.write('\n')
            f.write('Folio: '+str(id_r)+'\n')
            f.write('\n')
            f.write('\n')
            f.write('Rut: '+ans[0]['rut']+'\n')
            f.write('Cliente: '+ans[0]['name']+'\n')
            f.write('\n')
            f.write('\n')
            f.write('Puntos Canjeados: '+str(data['monto']) +'      Nuevo Saldo: '+str(data['saldo'])+ '\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('Producto Canjeado: _________________________'+'\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('Firma: ____________________')
            os.startfile(path_file)

    def add_record(self,data):
        ans = self.sqlite_crear_dato(data,'records')
        return ans

    def get_records(self):
        ans = self.sqlite_get_algunos_dic({'id_client':self.id},'records')
        return ans

    def export_records(self):
        data = self.sqlite_get_n_tablas_dic([[['rut','name','phone','mail'],'clients_info'],[['type_trans','date_trans','monto','saldo'],'records']],['id','id_client'],{'id':self.id})
        print(data)
        path_book = os.path.join(os.getcwd(),'OUTPUT','Records.xlsx')
        df = pd.DataFrame(data)
        writer = pd.ExcelWriter(path_book, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Records')
        workbook  = writer.book
        workbook.filename = path_book
        writer.save()
        os.startfile(path_book)
        return True

    def modificar_cliente(self,data):
        puntos = int(data['puntos'])
        old_points,hora = self.sqlite_query('SELECT points,time_grab FROM clients_points WHERE id_client = {}'.format(self.id))[0]

        new_points = int(old_points) + puntos
        ans = self.sqlite_actualizar({'points': new_points,'date_last_update': datetime.date.today(),'time_grab':hora},{'id_client':self.id},'clients_points')

        data_rec = {
            'id_client': self.id,
            'type_trans': 'editar',
            'date_trans': datetime.datetime.now(),
            'monto': puntos,
            'saldo': old_points+puntos
        }
        if new_points!=0:
            ans2 = self.add_record(data_rec)
            ans4 = self.cargar_vencimiento(int(puntos),datetime.date.today())
        
        return ['Error Inesperado',ans]


class Clients(DB_SQLite,DB_SQLserver):

    def __init__(self):
        super().__init__()

        
    def get_all(cls):
        ans = cls.sqlite_get_n_tablas([[['id','name','rut'],'clients_info'],[['points','date_creation'],'clients_points']],['id','id_client'],[])
        return ans


    def get_registros(cls):
        ans = cls.sqlite_get_n_tablas([[['rut'],'clients_info'],[['id','type_trans','date_trans','monto','saldo'],'records']],['id','id_client'],[])
        return ans

    def update_all(cls):
        data = cls.sqlite_query("SELECT rut FROM clients_info")
        for rut in data:
            client = Client({'rut':rut[0]})
            client.update_points()
            print(client.id)

    def export_data(cls,data):
        if data['check']:
            cls.update_all()
        try:
            path_book = os.path.join(os.getcwd(),'OUTPUT','Export_Data.xlsx')
            writer = pd.ExcelWriter(path_book, engine='xlsxwriter')
            data1 = cls.sqlite_get_n_tablas_dic([[['id','rut','name','phone','mail'],'clients_info'],[['points','date_creation','id_referido',],'clients_points']],['id','id_client'],{})
            df = pd.DataFrame(data1)
            df.to_excel(writer, sheet_name='Clients')

            data2 = cls.sqlite_get_n_tablas_dic([[['rut'],'clients_info'],[['id_client','type_trans','date_trans','monto','saldo'],'records']],['id','id_client'],{})
            df2 = pd.DataFrame(data2)
            df2.to_excel(writer, sheet_name='Records')

            workbook  = writer.book
            workbook.filename = path_book
            writer.save()
            os.startfile(path_book)
            return ['',True]
        except Exception as e:
            return ['Debe cerrar hoja de excel ya que no se pude sobreescribir',False]
        return True


if __name__=='__main__':
    dbx.start()
    i = 1
    with open('test.txt','r') as f:
        for line in f:
            #print(line.strip().split('xxx'))
            rut,fecha = line.strip().split('xxx') 
            if i == 1:
                a = 1
                if a:
                    db = Client({'rut': str(rut)})
                    ans = db.create_verify_new()
                    #print(ans[1])
                    if not ans[1]:
                        print(rut)
                        continue
                db = Client({'rut': str(rut)})
                if a:
                    dt = datetime.datetime.fromisoformat(fecha)
                    #print(dt.date())
                    ans = db.sqlite_actualizar({'date_last_update':dt.date(),'date_creation':dt.date()},{'id_client':db.id},'clients_points')
                #print(db.sqlite_get_algunos_dic({'id_client':db.id},'clients_points'))
                #db.update_points()
                #print(db.sqlite_get_algunos_dic({'id':db.id},'clients_info'))
                #print(db.sqlite_get_algunos_dic({'id_client':db.id},'clients_points'))
                
            #i = i +1
           # db.update_points()
             

    #db = Client({'rut':77164093})
    #print(db.get_client())
    #db.export_records()
    
    # ans = db.sqlserver_query_name_data('Pedir_pagos_dia',['BLV0000135290'])
    # print(ans)
    # ans = db.sqlserver_query_name_data('Pedir_nudo',['0000135290'])
    # print(ans)
    # db = Clients()
    # #print(db.get_all())
    # db.update_all()