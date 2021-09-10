import {Component, OnInit} from '@angular/core';
import {UsuarioService} from "../usuario.service";
import {UsuarioLista} from "../usuario";
import {ToastrService} from "ngx-toastr";
import {ActivatedRoute, Router} from "@angular/router";
import {CancionService} from "../../cancion/cancion.service";
import {CancionCompartida} from "../../cancion/cancion";
import {Location} from '@angular/common';
import {AlbumService} from "../../album/album.service";

@Component({
  selector: 'app-usuario-list',
  templateUrl: './usuario-list.component.html',
  styleUrls: ['./usuario-list.component.css']
})
export class UsuarioListComponent implements OnInit {

  listaUsuarios = new Array<UsuarioLista>();
  listaUsuariosB = new Array<UsuarioLista>();
  private token: string;
  private idUsuario: string;
  private idMedio: string;
  labelMedio: string = "";
  labelRoute: string = "";
  titulo: string;

  constructor(private _location: Location, private router: ActivatedRoute, private routerPath: Router, private usuarioService: UsuarioService, private cancionService: CancionService, private albumService: AlbumService, private toastr: ToastrService,) {
  }

  ngOnInit(): void {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {

      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    } else {
      this.idUsuario = this.router.snapshot.params.userId;
      this.token = this.router.snapshot.params.userToken;
      this.labelMedio = this.router.snapshot.params.medioLabel;
      this.idMedio = this.router.snapshot.params.medioId;
      this.labelMedio === "canciones" ? this.labelRoute = "canciones" : this.labelRoute = "albumes";
      this.showUsers();
    }
  }

  showError(error: string) {
    this.toastr.error(error, "Error de autenticación")
  }

  showUsers() {
    this.usuarioService.usersList(this.token, this.idMedio)
      .subscribe(res => {
          this.listaUsuariosB = res;
          this.listaUsuarios = res;
        },
        error => {
          this.showError(`Ha ocurrido un error: ${error.message}`)
        })
    this.buscarMedio();
  }

  listar() {
    this.labelMedio == "cancion" ? this.compartirCancion() : this.compartirAlbum;
  }

  showSuccess() {
    this.toastr.success(`El ${this.labelMedio} se ha compartido`, "Proceso exitoso");
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }

  volver() {
    this._location.back();
  }

  compartirAlbum() {
    console.log("Compartiendo Album")
  }

  buscarUsuario(busqueda: string) {
    let usuarioBusqueda: Array<UsuarioLista> = []
    this.listaUsuariosB.map(usuario => {
      if (usuario.nombre.toLocaleLowerCase().includes(busqueda.toLocaleLowerCase())) {
        usuarioBusqueda.push(usuario)
      }
    })
    this.listaUsuarios = usuarioBusqueda
  }

  compartirCancion() {
    let cancionCompartida = new CancionCompartida(this.idMedio, this.listaUsuarios.filter(s => s.checked == true).map(s => s.id.toString()));
    this.cancionService.compartirCancion(cancionCompartida, parseInt(this.idUsuario), this.token)
      .subscribe(res => {
          this.showSuccess()
          this.routerPath.navigate([`/albumes/${this.idUsuario}/${this.token}`])
        },
        error => {
          this.mostrarError(error)
        })
  }

  buscarMedio() {
    console.log(this.idMedio)
    if (this.labelMedio == "cancion") {
      this.cancionService.getCancion(parseInt(this.idMedio))
        .subscribe(res => {
            console.log(res)
            this.titulo = res.titulo
          },
          error => {
            this.mostrarError(error)
          })
    } else {
      this.albumService.getAlbum(parseInt(this.idMedio))
        .subscribe(res => {
            this.titulo = res.titulo
          },
          error => {
            this.mostrarError(error)
          })
    }
  }

  mostrarError(error: any) {
    if (error.statusText === "UNAUTHORIZED") {
      this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.")
    } else if (error.statusText === "UNPROCESSABLE ENTITY") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    } else {
      this.showError("Ha ocurrido un error. " + error.message)
    }
  }
}
