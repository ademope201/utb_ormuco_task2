""" 
TODO
1. Listar imagenes (Glance)
2. Listar redes (Neutron)
3. Listar flavors (Nova)
4. Listar par de llaves (Nova)
5. Listar grupos de seguridad (Neutron)
6. Crear instancias (Nova)
----------------------------------------------
7. Asignar FIP a instancias ()
"""
import requests
url = 'https://api-uat-001.ormuco.com:5000/v3/auth/tokens'
urlImage = 'https://api-uat-001.ormuco.com:9292/v2/images'

from flask import Flask, jsonify

app = Flask(__name__) 

"""
@app.route('/login', methods=['GET'])
def login ():
  return jsonify({"message": "pong!"})
 
@app.route('/elements')
def getElements ():
  return jsonify({"elements": elements})
"""

payload = {
  "auth": {
    "identity": {
      "methods": [
        "password"
      ],
      "password": {
        "user": {
          "name": "workshop2022@utb.edu.co",
          "domain": {
            "name": "Default"
          },
          "password": "ILOVECLOUD2022"
        }
      }
    }
  }
}


# 1. Authentication request
@app.route('/login', methods=['POST'])
def login():
    restoken = requests.post(url = url, json = payload)
    token_id = restoken.json().get('token').get('id')
    return jsonify(token_id)

    # 2. Images list request
    headers = {"X-Auth-Token": token_id}
    family = 'Linux'
    username = 'ubuntu'
    version = '18.04'
    imageId = ''
    for image in images:
        if(image.get("os_version",False) and version == image.get("os_version")):
            if(image.get("username") == username):
                    imageId = image['id']
                    #print(image['username'],image['os_version'],'ID:',image['id'])
            else:
                if(image.get("username") == username):
                    imageId = image['id']
                    #print(image['username'],image['version'],'ID:',image['id'])

    @app.route('/imagen', methods=['GET'])
    def imagen():
        section = requests.get(url = urlImage, headers = headers)
        images = section.json().get('images')
        return images

    # 3. Networks in listed
    @app.route('/networker', methods=['GET'])
    def networker():
        urlNetworks = 'https://api-uat-001.ormuco.com:9696/v2.0/networks'
        networks = requests.get(url = urlNetworks, headers = headers)
        network = networks.json().get('networks')
        findNetwork = 'default-network'
        idNetwork = ''
        for network in network:
            if(network['name'] == findNetwork):
                idNetwork = network['id']
        return network

    # 4. Listado de flavors (Nova)
    @app.route('/flavores', methods=['GET'])
    def flavores():
        urlFlavors = 'https://api-uat-001.ormuco.com:8774/v2.1/flavors'
        flavors = requests.get(url = urlFlavors,headers = headers)
        flavor = flavors.json().get('flavors')
        findFlavor = 'general.pico.uat.linux'
        idFlavor = ''
        for flavor in flavor:
            if(flavor['name'] == findFlavor):
                idFlavor = flavor['id']
        return (flavor)

    # 5. Para el par de llaves o 'Keypairs' (Nova)
    @app.route('/keypairs', methods=['GET'])
    def keypairs():
        urlKey = 'https://api-uat-001.ormuco.com:8774/v2.1/os-keypairs'
        keyPairs = requests.get(url = urlKey, headers = headers)
        print(keyPairs.json())


    # 6. Listar grupos de seguridad (Neutron)
    @app.route('/mysecurity_groups', methods=['GET'])
    def mysecurity_groups():
        urlGroup = 'https://api-uat-001.ormuco.com:8774/v2.1/os-security-groups'
        Security_groups = requests.get(url = urlGroup, headers = headers)
        print(Security_groups.json())
        return Security_groups

# 7. Creacion de instancia
@app.route('/youserver', methods=['POST'])
def youserver():
    urlInstance = "https://api-uat-001.ormuco.com:8774/v2.1/servers"
    data = {
            "server": {
                "name": "Adalberto_Python",
                "imageRef": imageId,
                "flavorRef": idFlavor,
                "networks": [{"uuid": idNetwork}],
                "min_count": 1,
                "max_count": 1,
                "config_drive": True,
                "block_device_mapping_v2": [
                    {"uuid": imageId, "source_type": "image", "boot_index": 0,
                    "delete_on_termination": True}],
                "metadata": {"source_image": imageId}
            }
    }
    response = requests.post(url=urlInstance, headers=headers, json=data)
    print(response.json())
    return jsonify(response) 

