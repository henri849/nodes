import subprocess

COMMAND = "dmesg | grep 'now attached to' | tail -1 | awk '{print $NF}'"
def get_last_usb_path():
    process = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    result = output.decode().strip()
    return f'/dev/{result}'

if __name__ == '__main__':
    path = get_last_usb_path()
    print(path)