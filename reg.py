import json, os

def main():
    print("Enter the name of host to start registration or \"stop\".")
    while True:
        data = dict()


        print("Enter the name:")
        host = input()
        if host == "stop":
            return 0
        if not host:
            print("Name cannot be empty.")
            continue
        if os.path.exists(f"hosts/{host}.json"):
            print(f"{host} is already registered.")
            continue


        print("Enter the address:")
        address = input() #Надо будет добавить валидатор
        if not address:
            print("Address cannot be empty.")
            continue
        data["address"] = address


        print("Enter the path to the certificate:")
        path_to_cert = input()  #Нужна проверка, что разрешение crt
        if not path_to_cert:
            print("Path cannot be empty.")
            continue
        if not os.path.exists(path_to_cert):
            print(f"{path_to_cert} does not exist.")
            continue
        data["path_to_cert"] = path_to_cert


        with open(f"hosts/{host}.json", "w") as f:
            json.dump(data, f, indent=2)

        print(f"{host} is registered.")

main()