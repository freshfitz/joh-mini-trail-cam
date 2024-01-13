import asyncio
import os
from bleak import BleakClient
import subprocess

ADDRESS = "ff:10:00:0d:81:72"
MODEL_NBR_UUID = ""
UART_TX_CHAR_UID = "5833ff03-9b8b-5191-6142-22a4536ef123"
UART_RX_CHAR_UUID = "f43ad982-3c98-455a-99ab-6e6e958e3529"
ip = "192.168.1.9"

def handle_rx(_: int, data: bytearray):
    print("received:",data)

async def main(ble_address, timeout=60.0):
    device = ADDRESS
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(ble_address) as client:
        await client.start_notify(UART_TX_CHAR_UID, handle_rx)
        print("Connected, start typing and press ENTER...")
        loop = asyncio.get_running_loop()
        info = b'66 66 31 30 30 30 30 64 38 31 37 32 30 31 30 36 30 30 30 35 30 34 20 37 35 35 35 30 30 31 31 32 30'
        await client.write_gatt_char(UART_RX_CHAR_UUID, info)
        print("sent:", info)

asyncio.run(main(ADDRESS))

#ssid aka wifi name
name = "Hunting Cam     "

#psk aka wifi pass
pwd =  "12345678"

def CreateWifiConfig(SSID, password):

    #setting up file contents
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        'country=US',
        '\n',
        'network={',
        '\tssid="{}"'.format(SSID),
        '\tpsk="{}"'.format(password),
        'key_mgmt=WPA-PSK',
        '}'
        ]
    config = '\n'.join(config_lines)

    #display additions
    print(config)

    #give access and writing. may have to do this manually beforehand
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    #writing to file
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)

    #displaying success
    print("wifi config added")

#run function, with vars as parameters
CreateWifiConfig(name, pwd)

#reboot, which impliments changes
os.popen("sudo wpa_cli -i wlan0 reconfigure")

def ping():
 response = os.system("ping -c 1 " + ip)

 #and then check the response...
 if response == 0:
   print(f"{ip} is up!")
   exit
 else:
   print(f"{ip} is down!")
   ping()
ping()
