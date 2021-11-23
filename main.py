from paramiko import client as cl
from config import USERNAME, PASSWORD, PORT, HOST
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=True, help="0 = turn off, 1 = turn on, 2 = toggle, 3 = status")
ap.add_argument("-w", "--wifi", required=True, help="select the network to modify")
args = vars(ap.parse_args())
mode, wifi = int(args["mode"]), int(args["wifi"])

client = cl.SSHClient()
client.load_system_host_keys()
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)


def main():
    guest_networks = [-1]

    for i in range(2):
        for j in range(1, 4):
            command = f"nvram get wl{i}.{j}_bss_enabled"
            _, stdout, _ = client.exec_command(command)

            for line in stdout.readlines():
                guest_networks.append(int(line.strip()))

    if wifi > 6 or wifi < 1:
        print(f"No wifi: {wifi}, wifi has to be from 0 - 5")

    if mode > 3 or mode < 0:
        print(f"No mode: {mode}, mode has to be from 0-3")

    if mode == 0:
        if guest_networks[wifi] == 0:
            return
        else:
            command = f"nvram set wl{int(wifi > 3)}.{wifi-(wifi > 3)*3}_bss_enabled=0"
            client.exec_command(command)

    elif mode == 1:
        if guest_networks[wifi] == 1:
            return
        else:
            command = f"nvram set wl{int(wifi > 3)}.{wifi-(wifi > 3)*3}_bss_enabled=1"
            client.exec_command(command)

    elif mode == 2:
        command = f"nvram set wl{int(wifi > 3)}.{wifi-(wifi > 3)*3}_bss_enabled={int(not bool(guest_networks[wifi]))}"
        client.exec_command(command)

    elif mode == 3:
        print(guest_networks[wifi])
        return

    client.exec_command("service restart_wireless")


if __name__ == "__main__":
    main()
