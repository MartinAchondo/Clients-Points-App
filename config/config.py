import os
import ctypes
import json
import uuid


def hideConsole():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd,0)

def verify_keys():
   filename = os.path.join(os.getcwd(),"config" ,"keys.json")
   with open(filename,"r") as file_json:
      data = json.load(file_json)
      id_pc = str(str(uuid.getnode()).encode("utf-8").decode("utf-8"))
      keys = data["keys"]
      if id_pc in keys.values():
         return True
      else:
         return False

def new_key(password):
   filename = os.path.join(os.getcwd(),"config", "keys.json")
   with open(filename,"r") as file_json:
      data = json.load(file_json)
      pass1 = data["password"]
      if pass1 != password:
         return False
   os.remove(filename)
   with open(filename,"w") as file_json:
        id_pc = str(str(uuid.getnode()).encode("utf-8").decode("utf-8"))
        num = len(data["keys"])
        n_key = "key" + str(num+1)
        data["keys"][n_key] = id_pc
        json.dump(data,file_json,indent=4)
        return True
    

