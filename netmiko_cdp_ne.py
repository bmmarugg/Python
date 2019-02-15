from netmiko import Netmiko
import json
import time
from pprint import pprint

device = input("What is the IP address you need CDP Neighbors for?: ")
username = input("Username: ")
password = input("Password: ")
print("\n" + "Please wait just a moment! Devices with more CDP neighbors will take longer to process.")

cisco1 = {
    "host": device,
    "username": username,
    "password": password,
    "device_type": "cisco_ios",
}

net_connect = Netmiko(**cisco1)
command = "show cdp ne d"
output = net_connect.send_command(command)
out_list = output.split("\n")


network_devices = []  # Initializes list to accept each CDP entry as a unique dictionary value

for line in out_list:
    if '--------------' in line:  # Separates each CDP entry
        device = {}  # Initializes new dictionary for each device
    if 'Device ID: ' in line:
        hostname = line.split()[-1]
        device["hostname"] = hostname
    if 'IP address: ' in line:
        ip = line.split()[-1]
        device["ip"] = ip
    if "Platform" in line:
        pltfm_list = line.split()
        pltfm_rm = [s.strip(',') for s in pltfm_list]  # Strips out the commas in each entry in the list
        platform = pltfm_rm[1] + " " + pltfm_rm[2]
        device["platform"] = platform
    if "Interface: " in line:
        int_list = line.split()
        int_list_rm = [s.strip(',') for s in int_list]  # Strips out the commas in each entry in the list
        local_int = int_list_rm[1]
        remote_int = int_list_rm[-1]
        device["local_int"] = local_int
        device["remote_int"] = remote_int
        network_devices.append(device)

print("\n")
print("-" * 100)

for device in network_devices:
    print("Hostname: {:<50}".format(device["hostname"]))
    print("{:>15} {:>25}".format("IP address: ", device["ip"]))
    print("{:>15} {:>25}".format("Platform: ", device["platform"]))
    print("{:>15} {:>25}".format("Local Int: ", device["local_int"]))
    print("{:>15} {:>25}".format("Remote Int: ", device["remote_int"]))
    print("~" * 100)
