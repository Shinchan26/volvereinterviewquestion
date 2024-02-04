import platform
import psutil
from speedtest import Speedtest
import wmi
import ctypes
import uuid            
import requests

def get_installed_software():
    # Fetch a list of all installed software
    software_list = []
    for app in psutil.process_iter(['name']):
        software_list.append(app.info['name'])
    return software_list

def get_internet_speed():
    # Measure internet speed of download and upload
    st = Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed

def get_system_info():
    # Fetch system information using WMI (Windows Management Instrumentation)
    w = wmi.WMI()
    system_info = w.Win32_ComputerSystem()[0]
    cpu_info = w.Win32_Processor()[0]
    gpu_info = w.Win32_VideoController()[0]
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    # Get screen resolution
    screen_resolution = f"{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}"

    # Get screen size - additional libraries might be needed
    screen_size = 'N/A'

    # Get MAC addresses
    wifi_mac_address = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(2, 6, 1)])
    ethernet_mac_address = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2, 1)])

    # Get public IP address using ipify API
    try:
        public_ip_address = requests.get('https://api.ipify.org?format=json').json()['ip']
    except requests.RequestException:
        public_ip_address = 'N/A'

    return {
        'os_version': platform.version(),
        'cpu_model': cpu_info.Name,
        'cpu_cores': cpu_info.NumberOfCores,
        'cpu_threads': cpu_info.NumberOfLogicalProcessors,
        'gpu_model': gpu_info.Caption if hasattr(gpu_info, 'Caption') else 'N/A',
        'ram_size_gb': round(psutil.virtual_memory().total / (1024 ** 3), 2),
        'screen_resolution': screen_resolution,
        'screen_size': screen_size,
        'wifi_mac_address': wifi_mac_address,
        'ethernet_mac_address': ethernet_mac_address,
        'public_ip_address': public_ip_address,
    }

if __name__ == "__main__":
    installed_software = get_installed_software()
    internet_speed = get_internet_speed()
    system_info = get_system_info()

    print("Installed Software List:")
    for software in installed_software:
        print(f"  - {software}")

    print("\nInternet Speed:")
    print(f"  - Download Speed: {internet_speed[0]:.2f} Mbps")
    print(f"  - Upload Speed: {internet_speed[1]:.2f} Mbps")

    print("\nSystem Information:")
    for key, value in system_info.items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")
