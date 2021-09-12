from flask import Flask

urls = {'VistaCanciones': '/canciones/<int:id_usuario>', 'VistaCancionesUsuario': '/usuario/<int:id_usuario>/canciones',
        'VistaCancion': '/cancion/<int:id_cancion>',
        'VistaAlbumesCanciones': '/cancion/<int:id_cancion>/albumes', 'VistaSignIn': '/signin', 'VistaLogIn': '/logIn',
        'VistaAlbumsUsuario': '/usuario/<int:id_usuario>/albumes', 'VistaAlbum': '/album/<int:id_album>',
        'VistaCancionesAlbum': '/album/<int:id_album>/canciones', 'VistaCancionesCompartidas': '/canciones/usuarios',
        'VistaUsuario': '/usuarios/<int:id_cancion>/canciones',
        'VistaUsuarioAlbumes': '/usuarios/<int:id_album>/albumes',
        'VistaAlbumCompartido': '/album/<int:id_album>/compartir'}


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_pyfile(config_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    return app
