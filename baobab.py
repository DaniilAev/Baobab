import socket, ssl, os, json, threading, cryptography
def main():
    name = "daniil" #TEMP
    #file indexing
    dir_path = "share\\"
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs("share", exist_ok=True)
    share_list = os.listdir(dir_path)
    files_json = json.dumps({file_name: os.path.getsize(dir_path + file_name) for file_name in share_list}, ensure_ascii=False)
    file_descriptors = {file_name: open(dir_path + file_name, 'rb') for file_name in share_list}

    #choosing the mode
    mode = 0
    while not mode:
        mode_str  = input("Enter the mode:\n1. Server mode\n2. Client mode\n")
        match mode_str:
            case '1':
                mode = 1
                break
            case '2':
                mode = 2
                break
            case _:
                print("Invalid mode")
                continue

    #processing the mode
    match mode:
        case 1:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.bind(('0.0.0.0', 4169))
            sock1.listen(1)
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.bind(('0.0.0.0', 4170))
            print("Server started on port 4169.")
            while True: #TEMP
                conn, addr = sock1.accept()
                client_name = conn.recv(1024).decode("ascii")
                try:
                    with open(f"hosts\{client_name}.json", "r") as file:
                        client_data = json.loads(file.read())
                except FileNotFoundError:
                    conn.close()
                    print("Client not found")

        case 2:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.bind(('0.0.0.0', 4169))
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.bind(('0.0.0.0', 4170))
            is_connected = False
            while not is_connected:
                addr_data = None
                while not addr_data:
                    servername = input("Enter the server's name:\n")
                    try:
                        with open(f"hosts\{servername}.json", "r") as file:
                            server_data = json.loads(file.read())
                    except FileNotFoundError:
                        print("Server not found")
                        continue
                try:
                    sock1.settimeout(10)
                    sock1.connect((addr_data["address"], 4169))
                    sock1.settimeout(None)
                    is_connected = True
                except socket.timeout:
                    print("Server timed out")
            sock1.send(name.encode("ascii"))
        case _:
            raise ValueError

if __name__ == "__main__":
    main()