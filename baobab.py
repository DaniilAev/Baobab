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
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', 4169))
            sock.listen(2)
            print("Server started on port 4169.")
            while True: #TEMP
                try:
                    conn1, addr1 = sock.accept()
                    conn1.settimeout(10)
                    client_name = conn1.recv(1024).decode("ascii")
                    conn1.send(b'\x06')
                    conn1.settimeout(None)
                except socket.error:
                    print("Server timed out")
                    conn1.close()
                    continue
                try:
                    with open(f"hosts\\{client_name}.json", "r") as file:
                        client_data = json.loads(file.read())
                        print(client_data)
                except FileNotFoundError:
                    conn1.close()
                    print("Client not found")
                    continue
                    #####

        case 2:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            is_connected = False
            while not is_connected:
                server_data = None
                while not server_data:
                    servername = input("Enter the server's name:\n")
                    try:
                        with open(f"hosts\\{servername}.json", "r") as file:
                            server_data = json.loads(file.read())
                    except FileNotFoundError:
                        print("Server not found")
                        continue
                    except json.decoder.JSONDecodeError:
                        print("Unable to decode json")
                try:
                    sock1.settimeout(10)
                    sock1.connect((server_data["address"], 4169))
                    sock1.settimeout(None)
                    is_connected = True
                except socket.error:
                    print("Server timed out")
            try:
                sock1.send(name.encode("ascii"))
                sock1.settimeout(10)
                assert sock1.recv(1) == b"\x06"
                sock1.settimeout(None)
            except socket.error:
                print("Timed out")
            except AssertionError:
                print("Unable to handshake")
                #####

        case _:
            raise ValueError

if __name__ == "__main__":
    main()