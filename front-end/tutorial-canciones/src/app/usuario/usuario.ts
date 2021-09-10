export class Usuario {
    id: number;
    nombre: string
    albumes: Array<any>

    constructor(
        id: number,
        nombre: string,
        albumes: Array<any>,
    ){
        this.id = id;
        this.nombre = nombre;
        this.albumes = albumes
    }
}

export class UsuarioLista extends Usuario {
   checked: boolean;

  constructor(
    id: number,
    nombre:string,
    albumes: Array<any>,
    checked=false
  ){
    super(id, nombre, albumes);
    this.checked = checked;
  }
}
