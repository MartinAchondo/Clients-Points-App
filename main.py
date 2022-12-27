import eel
import functions as fn
import config.config as cf
import database_sqlite.base as db
import codecs
#---------------------

@eel.expose
def pass_html(path):
    with codecs.open(path, "r", "utf-8") as file:
        html = file.read()
    return html


#---------- CREAR CLIENTE -----------------------#
@eel.expose
def crear_cliente(data):
    cliente = fn.Client(data)
    ans = cliente.create_verify_new()
    #ans = cls['Crear_Cliente'].crear_verificar_nuevo(data)
    return ans

#----------- ACTUALIZAR CLIENTE -----------------#

@eel.expose
def actualizar_cliente(data):
    cliente = fn.Client(data)
    ans = cliente.update_client()
    return ans

#------------ PEDIR CLIENTE ---------------------#

@eel.expose
def pedir_cliente(data):
    cliente = fn.Client(data)
    ans = cliente.get_client()
    return ans

@eel.expose
def verificar_cliente(data):
    client = fn.Client(data)
    ans = client.check_base2()
    return ans

@eel.expose
def get_points_client(data):
    client = fn.Client(data)
    ans = client.get_points()
    return ans

@eel.expose
def get_records_client(data):
    client = fn.Client(data)
    ans = client.get_records()
    return ans

@eel.expose
def pedir_clientes_tabla():
    clientes = fn.Clients()
    ans = clientes.get_all()
    return ans


@eel.expose
def get_last_venc(data):
    client = fn.Client(data)
    ans = client.get_last_venc()
    return ans



#------ CANJEAR PUNTOS ---------- #

@eel.expose
def canjear_cliente(data):
    client = fn.Client(data)
    ans = client.add_transaction(data)
    return ans


#-------- REGISTROS ---------- #

@eel.expose
def pedir_registros_all():
    clients = fn.Clients()
    ans = clients.get_registros()
    return ans

#### la nueva de excelll !!
@eel.expose
def print_data_excel(data):
    clientes = fn.Clients()
    ans = clientes.export_data(data)
    return ans

@eel.expose
def modificar_cliente(data):
    client = fn.Client(data)
    ans = client.modificar_cliente(data)
    return ans

#------------------------------------------------#

def start_classes():
    cls = {'Crear_Cliente': fn.Client()}
    return cls

def start_app():
    cf.hideConsole()
    eel.start('index.html')

def update_base():
    print('Iniciando App')
    print('Actualizando base de datos...')
    clients = fn.Clients()
    clients.update_all()

if __name__=='__main__':
    dev = False
    eel.init('frontend',allowed_extensions=['.js', '.html'])
    #cls = start_classes()
    db.start()
    #update_base()
    if dev:
        eel.start('index.html')
    if cf.verify_keys():
        start_app()
    else:
        password = input('Ingrese Clave: ')
        if cf.new_key(password):
            start_app()
            
    print('Clave incorrecta')
    input("")
