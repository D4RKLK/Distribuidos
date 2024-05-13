import socket
from threading import Thread
import tkinter as tk

def ouvir_servidor(referencia):
    while referencia[1]:
        try:
            data = referencia[0].recv(1024).decode()
            if data != "\0":
                msg = f"{data}"

                n = msg.find(":")

                m_name = msg[:n+1].replace(f"{referencia[-1]}:", "Você:")

                msg_final = m_name + msg[n+1:]

                novo_chat(msg_final)
                print(msg_final)
        except:
            referencia[1], referencia[0] = conectar(referencia[1])

### SOCKET ###
HOST = "localhost"
PORT = 9999
PORT_BACKUP = 10000

conectado = True

def conectar(conectado):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
    except:
        try:
            cliente.connect((HOST, PORT_BACKUP))
        except:
            conectado = False

            window = tk.Tk()
            window.geometry("800x400")
            window.title("Chat")

            frame_chat = tk.Frame()
            frame_chat.grid(row=0, column=0)

            chat_label = tk.Label(frame_chat, text="Não foi possivel conectar ao servidor\n(servidor ta ligado? ip e portas corretas?)", height=15, width=75, font=25, justify="center")
            chat_label.grid(row=0, column=0)

            window.mainloop()
    return conectado, cliente

### Janela ###

nome = ""

def enviar(nome):
    mensagem = input_text.get("1.0", "end")
    input_text.delete("1.0", "end")
    mensagem = mensagem[:-1]
    referencia[0].sendall(f"{nome[0]}: {mensagem}".encode())
    msg = f"Você: {mensagem}"
    novo_chat(msg)

def novo_chat(msg):
    if len(chats) >= 9:
        chats[0].forget()
        chats.pop(0)

    label_text = tk.Label(frame_chat, height=2, width=100, anchor="w", justify="left", text=msg)
    label_text.pack()
    chats.append(label_text)

def set_nome(nome):
    nome[0] = name_input.get("1.0", "end")
    nome[0] = nome[0][:-1]

    referencia.append(nome[0])

    frame_name.forget()

    frame_chat.grid(row=0, column=0)
    frame_bot.grid(row=1, column=0)

    for _ in range(9):
        novo_chat("")
    
    referencia[0].sendall("#BANCO".encode())

conectado, cliente = conectar(conectado)

if conectado:
    texto = ""
    chats = []
    nome = ["sem nome"]

    referencia = [cliente, conectado, texto]
    thread = Thread(target=ouvir_servidor, args=(referencia, ))
    thread.start()

    window = tk.Tk()
    window.geometry("800x400")
    window.resizable(0,0)
    window.title("Chat")

    frame_name = tk.Frame()
    frame_name.grid(row=0, column=0)
    name_label = tk.Label(frame_name, text="Digite o nome:")
    name_label.grid(row=0 ,column=0, padx=(200, 0), pady=(160, 0), columnspan = 2)

    name_input = tk.Text(frame_name, height=3, width=15)
    name_input.grid(row=1, column=0, padx=(275, 10))

    name_button = tk.Button(frame_name, text="Confirmar", height=3, width=10, command=lambda: set_nome(nome))
    name_button.grid(row=1, column=1, padx=(0, 0))

    frame_chat = tk.Frame()
    frame_bot = tk.Frame()

    input_text = tk.Text(frame_bot, height=5, width=90)
    input_button = tk.Button(frame_bot, text="Enviar", height=5, width=10, command=lambda: enviar(nome))

    input_text.grid(row=1, column=0)
    input_button.grid(row=1, column=1)

    window.mainloop()

    referencia[1] = False
    referencia[0].sendall(f"#EXIT".encode())