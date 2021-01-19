from flask import Flask, send_file
from flask_restful import Resource, Api

package_name = None
version_name = None
share_mode = None
minecraft_path = None

app = Flask(__name__)
api = Api(app)


class PackageInfo(Resource):
    def get(self):
        return {'package_name' : package_name, 'version_name' : version_name, 'share_mode':share_mode}
api.add_resource(PackageInfo, '/package_info')

class PackageDownload(Resource):
    def get(self):
        if share_mode == 0:
            return send_file(minecraft_path, package_name+".zip")
        elif share_mode == 1:
            return {'driveid' : minecraft_path}
api.add_resource(PackageDownload, '/package_download')

def run(ipaddress, port, _package_name, _version_name, _share_mode, _minecraft_path):
    global package_name, version_name, minecraft_path, share_mode
    package_name = _package_name
    version_name =_version_name
    share_mode = _share_mode
    minecraft_path = _minecraft_path
    app.run(host=ipaddress, port=int(port))