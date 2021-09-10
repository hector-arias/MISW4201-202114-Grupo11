import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
import {Usuario, UsuarioLista} from "./usuario";

@Injectable({
    providedIn: 'root'
  })
export class UsuarioService {

    private backUrl: string = "http://localhost:5000"

    constructor(private http: HttpClient) { }

    userLogIn(nombre: string, contrasena: string):Observable<any>{
        return this.http.post<any>(`${this.backUrl}/logIn`, {"nombre": nombre, "contrasena": contrasena });
    }

    userSignUp(nombre: string, contrasena: string): Observable<any>{
        return this.http.post<any>(`${this.backUrl}/signin`, {"nombre": nombre, "contrasena": contrasena})
    }

  usersList(token: string, id: string): Observable<UsuarioLista[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<any>(`${this.backUrl}/usuarios/${id}`,{headers: headers});
  }
}
