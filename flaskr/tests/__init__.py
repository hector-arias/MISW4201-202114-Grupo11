import unittest

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from flaskr import create_app, urls
from ..modelos import db, Usuario
from .. import app
from ..vistas import VistaCanciones, VistaCancion, VistaAlbumesCanciones, VistaSignIn, VistaLogIn, VistaAlbumsUsuario, \
    VistaAlbum, VistaCancionesAlbum, VistaAlbumCompartido, VistaCancionesUsuario, VistaCancionesCompartidas, \
    VistaUsuario,VistaCancionFavorita,VistaUsuarioAlbum


class BaseTestClass(unittest.TestCase):
    USUARIO = "prueba"
    CONTRASENA = "12345"
    USUARIO_2 = "prueba2"

    def setUp(self):
        self.app = create_app(config_name="config/testing.py")
        self.client = self.app.test_client()
        db.init_app(self.app)

        # Crea un contexto de aplicación
        with self.app.app_context() as c:
            c.push()            
            self.load_context()
            # Creamos usuarios
            BaseTestClass.create_user(self.USUARIO, self.CONTRASENA)
            BaseTestClass.create_user(self.USUARIO_2, self.CONTRASENA)

    def load_context(self):
        # Crea las tablas de la base de datos
        db.create_all()
        cors = CORS(self.app)       
        app.load_context_app(self.app)
        jwt = JWTManager(self.app)

    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(name, password):
        user = Usuario(nombre=name, contrasena=password)
        db.session.add(user)
        db.session.commit()
        return user

    def login(self, usuario, password):
        return self.client.post('/logIn', json={
            "nombre": usuario,
            "contrasena": password
        })
