from . import BaseTestClass
from ..modelos import Usuario


def adicionar_album(client, id_usuario, token):
    return client.post('/usuario/{0}/albumes'.format(id_usuario), json={
        "titulo": "Titulo",
        "anio": 2021,
        "descripcion": "Descripcion",
        "medio": "DISCO"
    }, headers={'Authorization': 'Bearer {0}'.format(token)})


def compartir_album(client, id_album, id_compartir_con, token):
    return client.post('/album/{0}/compartir'.format(id_album), json={
        "ids_usuarios": [id_compartir_con]
    }, headers={'Authorization': 'Bearer {0}'.format(token)})


class AlbumCompartirTestCase(BaseTestClass):
    def test_compartir_album(self):
        rv = self.login(self.USUARIO, self.CONTRASENA)
        json_data = rv.get_json()
        self.assertEqual("Inicio de sesión exitoso", json_data['mensaje'])
        propietario = Usuario.query.filter(Usuario.nombre == self.USUARIO).first()
        compartir_con = Usuario.query.filter(Usuario.nombre == self.USUARIO_2).first()
        token = json_data['token']
        json_album = adicionar_album(self.client, propietario.id, token).get_json()
        self.assertEqual("Titulo", json_album['titulo'])
        json_compartir = compartir_album(self.client, json_album['id'], compartir_con.id, token).get_json()
        self.assertEqual("El álbum se ha compartido exitosamente con los usuarios.", json_compartir['mensaje'])
