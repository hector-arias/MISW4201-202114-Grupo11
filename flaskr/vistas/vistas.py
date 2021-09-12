from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, UsuarioListaSchema

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
usuarioLista_schema = UsuarioListaSchema()
album_schema = AlbumSchema()


class VistaCanciones(Resource):

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [cancion_schema.dump(ca) for ca in usuario.canciones]


class VistaCancionesUsuario(Resource):

    def post(self, id_usuario):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"],
                                segundos=request.json["segundos"], interprete=request.json["interprete"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre', 409

        return cancion_schema.dump(nueva_cancion)


class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo", cancion.titulo)
        cancion.minutos = request.json.get("minutos", cancion.minutos)
        cancion.segundos = request.json.get("segundos", cancion.segundos)
        cancion.interprete = request.json.get("interprete", cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '', 204


class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]


class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


class VistaAlbumsUsuario(Resource):

    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"],
                            descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre', 409

        return album_schema.dump(nuevo_album)

    # @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]


class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)

        if "id_cancion" in request.json.keys():

            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea', 404
        else:
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"],
                                    segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]


class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo", album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '', 204


class VistaCancionesCompartidas(Resource):
    def get(self):
        cancion = Cancion.query.all()
        return [cancion_schema.dump(ca) for ca in cancion]

    def post(self):
        cancion = Cancion.query.get_or_404(request.json["id_cancion"])
        usuarios_compartir = None

        if "id_usuario" in request.json.keys():
            usuarios_compartir = request.json["id_usuario"]
        else:
            return 'falta id usuario', 404

        for x in usuarios_compartir:
            print(x)
            if cancion.usuario == x:
                return 'No se puede compartir con si mismo', 404

        for x in usuarios_compartir:

            user = Usuario.query.get(x)
            print("****user ", user)
            if user is not None:
                cancion.usuarios.append(user)
                db.session.commit()
            else:
                return 'Canción errónea', 404

        db.session.commit()
        return cancion_schema.dump(cancion)


class VistaUsuario(Resource):
    def get(self, id_cancion):
        noCompartidos = []
        cancion = Cancion.query.filter(Cancion.id == id_cancion).first()
        if cancion is not None:
            listaUsuarios = Usuario.query.all()
            for users in listaUsuarios:
                print(users.id, cancion.usuario)
                if users not in cancion.usuarios and users.id != cancion.usuario: noCompartidos.append(users)
            return [usuarioLista_schema.dump(ca) for ca in noCompartidos]
        else:
            return 'Esta canción no existe'

class VistaUsuarioAlbum(Resource):
    def get(self, id_album):
        noCompartidos = []
        album = Album.query.filter(Album.id == id_album).first()
        if album is not None:
            listaUsuarios = Usuario.query.all()
            for users in listaUsuarios:
                print(users.id, album.usuario)
                if users not in album.compartido_con and users.id != album.usuario: noCompartidos.append(users)
            return [usuarioLista_schema.dump(ca) for ca in noCompartidos]
        else:
            return 'Este album no existe'


class VistaAlbumCompartido(Resource):

    @jwt_required()
    def post(self, id_album):
        album = Album.query.filter(Album.id == id_album).first()
        if album is None:
            return {"error": "El álbum con id {0} no existe.".format(id_album)}, 400
        if "ids_usuarios" in request.json.keys():
            ids_usuarios = request.json["ids_usuarios"]
        else:
            return {"error": "Se debe seleccionar por lo menos un usuario para compartir el álbum."}, 400
        if album.usuario in ids_usuarios:
            return {"error": "El propietario no puede compartir el álbum con él mismo."}, 400
        for usuario_id in ids_usuarios:
            if len(album.compartido_con) > 0:
                for usuario_compartido in album.compartido_con:
                    if usuario_compartido.id == usuario_id:
                        return {"error": "El álbum ya había sido compartido con {0}".format(
                            usuario_compartido.nombre)}, 400
            usuario_compartir = Usuario.query.filter(Usuario.id == usuario_id).first()
            if usuario_compartir is None:
                return {"error": "El usuario con id {0} no existe.".format(usuario_id)}, 400
            usuario_compartir.albumes_compartidos.append(album)
        db.session.commit()
        return {"mensaje": "El álbum se ha compartido exitosamente con los usuarios."}
