from . import BaseTestClass
from ..modelos import Usuario


def adicionar_album(client, id_usuario, token):
    return client.post('/usuario/{0}/albumes'.format(id_usuario), json={
        "titulo": "Titulo",
        "anio": 2021,
        "descripcion": "Descripcion",
        "medio": "DISCO",
        "genero": "SALSA"
    }, headers={'Authorization': 'Bearer {0}'.format(token)})


def obtener_albumes_usuario(client, id_usuario, token):
    return client.get('/usuario/{0}/albumes'.format(id_usuario), headers={'Authorization': 'Bearer {0}'.format(token)})


class TestVistaAlbumsUsuario(BaseTestClass):
    def test_post(self):
        rv = self.login(self.USUARIO, self.CONTRASENA)
        json_data = rv.get_json()
        self.assertEqual("Inicio de sesión exitoso", json_data['mensaje'])
        token = json_data['token']
        propietario = Usuario.query.filter(Usuario.nombre == self.USUARIO).first()
        json_album = adicionar_album(self.client, propietario.id, token).get_json()
        self.assertEqual("SALSA", json_album['genero']['llave'])

    def test_get(self):
        rv = self.login(self.USUARIO, self.CONTRASENA)
        json_data = rv.get_json()
        self.assertEqual("Inicio de sesión exitoso", json_data['mensaje'])
        token = json_data['token']
        propietario = Usuario.query.filter(Usuario.nombre == self.USUARIO).first()
        adicionar_album(self.client, propietario.id, token).get_json()
        json_album = obtener_albumes_usuario(self.client, propietario.id, token).get_json()
        self.assertEqual("SALSA", json_album[0]['genero']['llave'])
