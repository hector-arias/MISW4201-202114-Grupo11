from . import BaseTestClass
from ..modelos import Usuario


def cancion_favorita(client,id_cancion, token, status):
    return client.put('/cancion-favorita/{0}'.format(id_cancion), json={
	    "favorita":status
    }, headers={'Authorization': 'Bearer {0}'.format(token)})

def adicionar_cancion(client, id_usuario, token, titulo):
    return client.post('/usuario/{0}/canciones'.format(id_usuario), json={
        "titulo": titulo,
        "minutos": 10,
        "segundos": 10,
        "interprete": "Claudia",
        "genero": "ROCK"
    }, headers={'Authorization': 'Bearer {0}'.format(token)})


class CancionFavoritaTestCase(BaseTestClass):
    def test_cancion_favorita(self):
        rv = self.login(self.USUARIO, self.CONTRASENA)
        json_data = rv.get_json()
        self.assertEqual("Inicio de sesión exitoso", json_data['mensaje'])
        propietario = Usuario.query.filter(Usuario.nombre == self.USUARIO).first()
        token = json_data['token']
        titulo = "Cancion"
        json_cancion = adicionar_cancion(self.client, propietario.id, token,titulo).get_json()
        json_favorita = cancion_favorita(self.client, json_cancion['id'],token,1).get_json() 
        self.assertEqual(1, json_favorita['favorita'])

    def test_cancion_favorita_desactivar(self):
        rv = self.login(self.USUARIO, self.CONTRASENA)
        json_data = rv.get_json()
        self.assertEqual("Inicio de sesión exitoso", json_data['mensaje'])
        propietario = Usuario.query.filter(Usuario.nombre == self.USUARIO).first()
        token = json_data['token']
        titulo = "Cancion_2"
        json_cancion = adicionar_cancion(self.client, propietario.id, token, titulo).get_json()
        json_favorita = cancion_favorita(self.client, json_cancion['id'],token,0).get_json()         
        self.assertEqual(0, json_favorita['favorita'])
