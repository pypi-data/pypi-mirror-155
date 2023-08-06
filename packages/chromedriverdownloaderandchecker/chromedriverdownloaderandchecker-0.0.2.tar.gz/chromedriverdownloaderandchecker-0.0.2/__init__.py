import os
import zipfile
import wget
import subprocess
import requests
from win32com.client.dynamic import Dispatch


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

def driver_download_code(chrome_driver_path, chrome_browser_path):

    chrome_version = get_version_via_com(chrome_browser_path)
    print(f'Chrome version = {chrome_version}')
    url_link = 'https://chromedriver.storage.googleapis.com/'
    r = requests.get(url_link)
    p1 = str(r.text).find(chrome_version.split('.')[0] + '.')
    p2 = str(r.text).find('/chromedriver_win32.zip', p1)
    driver_version = str(r.text)[p1:p2].split('/')[0]
    print(f'Chrome driver version = {driver_version}')
    download_url = "https://chromedriver.storage.googleapis.com/" + driver_version + "/chromedriver_win32.zip"
    wget.download(download_url, chrome_driver_path)
    with zipfile.ZipFile(chrome_driver_path + '\\' + 'chromedriver_win32.zip', 'r') as zip_ref:
        zip_ref.extractall(chrome_driver_path)
    os.remove(chrome_driver_path + '\\' + 'chromedriver_win32.zip')
    print('Your chrome browser compatible chrome driver has downloaded')

def check_driver(chrome_driver_path, chrome_browser_path):
    old_dir = os.getcwd()
    if os.path.exists(chrome_driver_path):
        if os.path.exists(chrome_driver_path + '\\' + 'chromedriver.exe'):

            chrome_version = get_version_via_com(chrome_browser_path)
            print(f'Chrome version = {chrome_version}')
            chrome_version = chrome_version.split('.')[0] + '.'
            try:
                os.chdir(chrome_driver_path)
                cmd = "chromeDriver --version"
                returned_value = subprocess.check_output(cmd)
                chrome_driver_version = str(returned_value.decode("utf-8")).split(' ')[1]
                print(f'Chrome driver version = {chrome_driver_version}')
                chrome_driver_version = chrome_driver_version.split('.')[0] + '.'
                if chrome_driver_version == chrome_version:
                    print('Chrome browser and chrome driver version are same')
                else:
                    try:
                        os.system(f'taskkill /f /im chromedriver.exe')
                    except Exception as e:
                        print(str(e))
                        print('Chrome driver is not in process')
                    for i in os.listdir(chrome_driver_path):
                        os.remove(chrome_driver_path + '\\' + i)
                    driver_download_code(chrome_driver_path, chrome_browser_path)
            except Exception as e:
                print(str(e))
                os.system(f'taskkill /f /im chromedriver.exe')
                for i in os.listdir(chrome_driver_path):
                    os.remove(chrome_driver_path + '\\' + i)
                driver_download_code(chrome_driver_path, chrome_browser_path)
        else:
            driver_download_code(chrome_driver_path, chrome_browser_path)
    else:
        os.mkdir(chrome_driver_path)
        driver_download_code(chrome_driver_path, chrome_browser_path)
    os.chdir(old_dir)