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


from flask import Flask, jsonify

app = Flask(__name__) 

from elements import elements

"""
@app.route('/login', methods=['GET'])
def login ():
  return jsonify({"message": "pong!"})
""" 
@app.route('/elements')
def getElements ():
  return jsonify({"elements": elements})

@app.route('/elements/<string:element_name>')
def getElement (element_name):
  elementsFound = [element for element in elements if element['name'] == element_name]
  if (len(elementsFound) > 0):
    return jsonify({"element": elementsFound[0]})
  return jsonify({"message": "element not found"})

if __name__ == '__main__':
  app.run(debug=True, port=5000)






