from flaskr import create_app, urls
from flask_restful import Api
from .modelos import db
from .vistas import VistaCanciones, VistaCancionesCompartidas, VistaCancionesUsuario, VistaCancion, VistaSignIn, \
    VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum, VistaLogIn, VistaAlbumesCanciones, VistaUsuario, \
    VistaAlbumCompartido, VistaUsuarioAlbum
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app("config/default.py")
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaCanciones, urls['VistaCanciones'])
api.add_resource(VistaCancionesUsuario, urls['VistaCancionesUsuario'])
api.add_resource(VistaCancion, urls['VistaCancion'])
api.add_resource(VistaAlbumesCanciones, urls['VistaAlbumesCanciones'])
api.add_resource(VistaSignIn, urls['VistaSignIn'])
api.add_resource(VistaLogIn, urls['VistaLogIn'])
api.add_resource(VistaAlbumsUsuario, urls['VistaAlbumsUsuario'])
api.add_resource(VistaAlbum, urls['VistaAlbum'])
api.add_resource(VistaCancionesAlbum, urls['VistaCancionesAlbum'])
api.add_resource(VistaCancionesCompartidas, urls['VistaCancionesCompartidas'])
api.add_resource(VistaUsuario, urls['VistaUsuario'])
api.add_resource(VistaAlbumCompartido, urls['VistaAlbumCompartido'])
api.add_resource(VistaUsuarioAlbum, urls['VistaUsuarioAlbumes'])


jwt = JWTManager(app)

