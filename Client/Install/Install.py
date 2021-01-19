import os
import zipfile
import requests
import sqlite3

def download_package(ip, port, ui=None):
    url = "http://{0}:{1}/".format(ip, port)
    file_list = childDirectories = next(os.walk("./minecraft_files"))[1]

    try:
        package_info = requests.get(url + 'package_info').json()
    except:
        return None


    num = 0
    while str(num) in file_list:
        num += 1

    with open('./temp/{0}.zip'.format(num), "wb") as file:
        response = requests.get(url+'package_download')
        file.write(response.content)

    os.mkdir("./minecraft_files/{0}".format(num))
    unzip_path = "./minecraft_files/{0}".format(num)

    zf = zipfile.ZipFile('./temp/{0}.zip'.format(num)).extractall(unzip_path)




    package_info['minecraft_path'] = "./minecraft_files/{0}".format(num)
    package_info['id'] = num


    if os.path.isfile('./temp/{0}.zip'.format(num)):
        os.remove('./temp/{0}.zip'.format(num))

    return package_info

def install(ip, port, db_path="data\\DelphiDB.db", ui=None):
    package_info = download_package(ip, port, ui=ui)

    if package_info == None:
        return None

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO launch_profile Values (?, ?, ?);", (package_info['id'], package_info['package_name'], package_info['version_name']))
    conn.commit()
    cur.close()
    conn.close()

    return package_info
