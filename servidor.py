import socket
import threading
import json
import os

os.makedirs("arquivos", exist_ok=True)

# Inicializa arquivos se não existirem
for f, default in [("arquivos/professor.json", []), ("arquivos/adm.json", {"login_adm":"adm123","senha_adm":"adm123",'cpf_professor':[]})]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            json.dump(default, file, indent=4)

def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode()
        payload = json.loads(data)
        tipo = payload.get("tipo")
        if tipo == "adm":
            with open("arquivos/adm.json", "w") as f:
                json.dump(payload["dados"], f, indent=4)
        elif tipo == "professor":
            with open("arquivos/professor.json", "w") as f:
                json.dump(payload["dados"], f, indent=4)
        elif tipo == "get_adm":
            with open("arquivos/adm.json", "r") as f:
                adm_dados = json.load(f)
            conn.send(json.dumps(adm_dados).encode())
        elif tipo == "get_professor":
            with open("arquivos/professor.json", "r") as f:
                prof_dados = json.load(f)
            conn.send(json.dumps(prof_dados).encode())
        conn.send(b"OK")
    except Exception as e:
        print(e)
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    print("Servidor rodando na porta 5000...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
