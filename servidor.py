import socket
import threading
import json
import os

os.makedirs("arquivos", exist_ok=True)

# Inicializa arquivos se não existirem
arquivos_iniciais = {
    "arquivos/professor.json": [],
    "arquivos/aluno.json": [],
    "arquivos/adm.json": {
        "login_adm": "adm123",
        "senha_adm": "adm123",
        "cpf_professor": [],
        "curso_diciplina": []
    }
}

for caminho, default in arquivos_iniciais.items():
    if not os.path.exists(caminho):
        with open(caminho, "w") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)


def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode()
        payload = json.loads(data)
        tipo = payload.get("tipo")

        # ======== GRAVAÇÕES ========
        if tipo == "adm":
            with open("arquivos/adm.json", "w", encoding="utf-8") as f:
                json.dump(payload["dados"], f, indent=4, ensure_ascii=False)

        elif tipo == "professor":
            with open("arquivos/professor.json", "w", encoding="utf-8") as f:
                json.dump(payload["dados"], f, indent=4, ensure_ascii=False)

        elif tipo == "aluno":
            with open("arquivos/aluno.json", "w", encoding="utf-8") as f:
                json.dump(payload["dados"], f, indent=4, ensure_ascii=False)

        # ======== LEITURAS ========
        elif tipo == "get_adm":
            with open("arquivos/adm.json", "r", encoding="utf-8") as f:
                conn.send(json.dumps(json.load(f)).encode())

        elif tipo == "get_professor":
            with open("arquivos/professor.json", "r", encoding="utf-8") as f:
                conn.send(json.dumps(json.load(f)).encode())

        elif tipo == "get_aluno":
            with open("arquivos/aluno.json", "r", encoding="utf-8") as f:
                conn.send(json.dumps(json.load(f)).encode())

        conn.send(b"OK")

    except Exception as e:
        print("Erro no cliente:", e)

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
