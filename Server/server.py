from flask import Flask, send_file
from flask_restful import Resource, Api

package_name = None
version_name = None
minecraft_path = None

app = Flask(__name__)
api = Api(app)

class PackageInfo(Resource):
    def get(self):
        return {'package_name' : package_name, 'version_name' : version_name}
api.add_resource(PackageInfo, '/package_info')

class PackageDownload(Resource):
    def get(self):
        return send_file(minecraft_path, package_name+".zip")
api.add_resource(PackageDownload, '/package_download')

def run(ipaddress, port, _package_name, _version_name, _minecraft_path):
    global package_name, version_name, minecraft_path
    package_name = _package_name
    version_name =_version_name
    minecraft_path = _minecraft_path
    app.run(host=ipaddress, port=int(port))