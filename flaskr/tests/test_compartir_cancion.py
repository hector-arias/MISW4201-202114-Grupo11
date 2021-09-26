from . import BaseTestClass
from ..modelos import Usuario


def adicionar_cancion(client, id_usuario, token):
    return client.post('/usuario/{0}/canciones'.format(id_usuario), json={
        "titulo": "Titulo",
        "minutos": 10,
        "segundos": 10,
        "interprete": "Claudia",
        "genero": "ROCK"
    }, headers={'Authorization': 'Bearer {0}'.format(token)})


def compartir_cancion(client, id_cancion, id_usuario, token):
    return client.post('/canciones/usuarios', json={
        "id_usuario":[id_usuario],
        "id_cancion":id_cancion
}, headers={'Authorization': 'Bearer {0}'.format(token)})


class CancionCompartirTestCase(BaseTestClass):

    def test_compartir_cancion(self):
        rv = self.login(self.USUARIO, self.CONTRASENA)
        json_data = rv.get_json()
        self.assertEqual("Inicio de sesión exitoso", json_data['mensaje'])
        propietario = Usuario.query.filter(Usuario.nombre == self.USUARIO).first()
        compartir_con = Usuario.query.filter(Usuario.nombre == self.USUARIO_2).first()
        token = json_data['token']
        json_cancion= adicionar_cancion(self.client, propietario.id, token).get_json()
        self.assertEqual("Titulo", json_cancion['titulo'])
        json_compartir = compartir_cancion(self.client, json_cancion['id'], compartir_con.id, token).get_json()
        self.assertEqual([compartir_con.id], json_compartir['usuarios_compartidos'])
