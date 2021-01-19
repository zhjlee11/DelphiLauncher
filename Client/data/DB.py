import sqlite3
import shutil

def load_launcher_profile(db_path=".\\data\\DelphiDB.db"):
    launcher_profile = {}

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM launch_profile;")
    rows = cur.fetchall()

    for row in rows:
        setting = dict(zip(["id", "package_name", "version_name"], row))
        setting['minecraft_path'] = "./minecraft_files/{0}".format(row[0])
        launcher_profile[row[0]] = setting

    cur.close()
    conn.close()

    return launcher_profile

def rename_launcher_profile(id, name, db_path=".\\data\\DelphiDB.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f"UPDATE launch_profile SET package_name = '{name}' WHERE id = {id}")
    conn.commit()

    cur.close()
    conn.close()

def remove_launcher_profile(id, db_path=".\\data\\DelphiDB.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f"DELETE FROM launch_profile WHERE id = {id}")
    conn.commit()

    cur.close()
    conn.close()

    shutil.rmtree('.\\minecraft_files\\{0}'.format(id))


if __name__ == '__main__':
    rename_launcher_profile(0, "test1", db_path="..\\data\\DelphiDB.db")