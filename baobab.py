import socket, ssl, os, json, threading
def main():
    dir_path = "share\\"
    os.makedirs(dir_path, exist_ok=True)
    share_list = os.listdir(dir_path)
    files_json = json.dumps({file_name: os.path.getsize(dir_path + file_name) for file_name in share_list}, ensure_ascii=False)
    file_descriptors = {file_name: open(dir_path + file_name, 'rb') for file_name in share_list}




main()