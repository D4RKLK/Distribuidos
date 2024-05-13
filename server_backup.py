import socket
from threading import Thread
from time import sleep
import pymongo

def ouvir_cliente(conn):
    while True:
        data = conn.recv(1024)
        check = data.decode()
        if check == "#EXIT":
            break
        if check == "#BANCO":
            for x in mycol.find():
                conn.sendall(f"{x["mensagem"]}".encode())
                sleep(0.1)
        if check != "#BANCO":
            for i in clientes:
                if i[0] != conn:
                    i[0].sendall(data)
            mycol.insert_one({"mensagem": data.decode()})
            print(data.decode())

def att():
    while True:
        if len(clientes) > 0:
            for i in clientes:
                i[0].sendall("\0".encode())
        sleep(1)

# Data Base
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["chat"]
mycol = mydb["mensagens_backup"]

#mycol.delete_many({})

#mydict = { "mensagem": "Bom, dia" }
#x = mycol.insert_one(mydict)

for x in mycol.find():
    print(x["mensagem"])

HOST = "localhost"
PORT = 10000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Objeto socket
server.bind((HOST, PORT))  # Vinculando servidor

clientes = []  # Todos os clientes conectados
lista_threads = []  # Todas as threads abertas

Thread(target=att, args=()).start()

print("Servidor Ligado...")

while True:
    server.listen()  # Ouvindo clientes
    conn, addr = server.accept()  # Cliente aceito (objeto cliente, endereço)
    clientes.append((conn, addr))
    print(f"Novo Cliente conectado, {clientes[-1][1]}")
    nova_thread = Thread(target=ouvir_cliente, args=(clientes[-1][0], ))
    lista_threads.append(nova_thread)
    lista_threads[-1].start()
