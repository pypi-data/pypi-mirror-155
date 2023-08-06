import subprocess
import re

def get_wifi_password_by_profile():
    s = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']).decode('gbk')
    wifi_ssid=re.findall(':\s(.+)\r',s)
    print(wifi_ssid)
    info = {}
    for i in wifi_ssid:
        profile_info = subprocess.check_output(
              ['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('gbk')
        pwd=re.findall('关键内容\s+:\s(\w+)',profile_info )
        info[i] = pwd
    return info

if __name__ == '__main__':
    d = get_wifi_password_by_profile()
    print(d)

