import socket, ssl, os, json, threading
def main():
    #file indexing
    dir_path = "share\\"
    os.makedirs(dir_path, exist_ok=True)
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
            print("Server started on port 4169.")
            conn, addr = sock1.accept()
            print(f"Connected by {addr}")
        case 2:
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock1.bind(('0.0.0.0', 4169))
            is_connected = False
            while not is_connected:
                addr = None
                while not addr:
                    raw_addr = input("Enter the server address:\n")
                    if is_addr_valid(raw_addr):
                        addr = raw_addr
                    else:
                        print("Invalid address.")
                try:
                    sock1.connect((addr, 4169))
                    is_connected = True
                except socket.error:
                    print("Unable to connect to the server.")
        case _:
            raise ValueError

def is_addr_valid(addr: str) -> bool:
    if addr == "localhost":
        return True
    else:
        octets = addr.split(".")
        if len(octets) != 4:
            return False
        else:
            for octet in octets:
                if int(octet) < 0 or int(octet) > 255:
                    return False
            return True



main()