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
8. Listar/Crear Volumenes ()
9. Asignar un volumen a una instancia ()
"""
import requests
url = 'https://api-uat-001.ormuco.com:5000/v3/auth/tokens'
urlImage = 'https://api-uat-001.ormuco.com:9292/v2/images'



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
restoken = requests.post(url = url, json = payload)
token_id = restoken.json().get('token').get('id')

# 2. Images list request
headers = {"X-Auth-Token": token_id}
section = requests.get(url = urlImage, headers = headers)
images = section.json().get('images')
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

# 3. Networks in listed
urlNetworks = 'https://api-uat-001.ormuco.com:9696/v2.0/networks'
networks = requests.get(url = urlNetworks, headers = headers)
network = networks.json().get('networks')
findNetwork = 'default-network'
idNetwork = ''
for network in network:
    if(network['name'] == findNetwork):
        idNetwork = network['id']

# 4. Listado de flavors (Nova)
urlFlavors = 'https://api-uat-001.ormuco.com:8774/v2.1/flavors'
flavors = requests.get(url = urlFlavors,headers = headers)
flavor = flavors.json().get('flavors')
findFlavor = 'general.pico.uat.linux'
idFlavor = ''
for flavor in flavor:
    if(flavor['name'] == findFlavor):
        idFlavor = flavor['id']


# 5. Para el par de llaves o 'Keypairs' (Nova)
urlKey = 'https://api-uat-001.ormuco.com:8774/v2.1/os-keypairs'
keyPairs = requests.get(url = urlKey, headers = headers)
print(keyPairs.json())


# 6. Listar grupos de seguridad (Neutron)
urlGroup = 'https://api-uat-001.ormuco.com:8774/v2.1/os-security-groups'
security_groups = requests.get(url = urlGroup, headers = headers)
print(security_groups.json())


# 7. Creacion de instancia
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


# 8. FIP
urlFip = 'https://api-uat-001.ormuco.com:9696/v2.0/floatingips'
fip = requests.get(url = urlFip, headers = headers)
Fip = fip.json().get('floatingips')
fixed = Fip[2]['fixed_ip_address']
floatingIp = Fip[2]['floating_ip_address']
new = {
    "addFloatingIp" : {
        "address": floatingIp,
        "fixed_address": fixed
    }
}
print(floatingIp)
print(fixed)
urlFIP = 'https://api-uat-001.ormuco.com:8774/v2.1/servers/3948a75c-d135-4ffa-98e6-260bb3a30c27/action'
responseFIP = requests.post(url = urlFIP,headers = headers, json = new)
print(responseFIP)

#"key_name": "AdalbertoeMoralesP",
#"Security_groups":[{"name": "web"}],