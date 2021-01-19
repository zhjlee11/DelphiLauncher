import os
import zipfile
import requests
import sqlite3

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_package(url, ui=None):
    file_list = childDirectories = next(os.walk("./minecraft_files"))[1]

    try:
        package_info = requests.get(url + 'package_info').json()
    except:
        return None



    num = 0
    while str(num) in file_list:
        num += 1

    # 파일 호스팅 직접 다운로드
    if package_info['share_mode'] == 0:
        with open('./temp/{0}.zip'.format(num), "wb") as file:
            response = requests.get(url+'package_download')
            file.write(response.content)

    #구글 드라이브
    elif package_info['share_mode'] == 1:
        driveid = requests.get(url+'package_download').json()['driveid']
        download_file_from_google_drive(driveid, './temp/{0}.zip'.format(num))

    os.mkdir("./minecraft_files/{0}".format(num))
    unzip_path = "./minecraft_files/{0}".format(num)

    zf = zipfile.ZipFile('./temp/{0}.zip'.format(num)).extractall(unzip_path)

    package_info['minecraft_path'] = "./minecraft_files/{0}".format(num)
    package_info['id'] = num

    if os.path.isfile('./temp/{0}.zip'.format(num)):
        os.remove('./temp/{0}.zip'.format(num))

    return package_info

def install(ip, db_path="data\\DelphiDB.db", ui=None):
    package_info = download_package(ip, ui=ui)

    if package_info == None:
        return None

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO launch_profile Values (?, ?, ?);", (package_info['id'], package_info['package_name'], package_info['version_name']))
    conn.commit()
    cur.close()
    conn.close()

    return package_info
