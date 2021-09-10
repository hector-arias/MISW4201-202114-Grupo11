import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsuarioLoginComponent } from './usuario-login/usuario-login.component';
import { UsuarioSignupComponent } from './usuario-signup/usuario-signup.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { UsuarioListComponent } from './usuario-list/usuario-list.component';
import {AppHeaderModule} from "../app-header/app-header.module";


@NgModule({
  declarations: [UsuarioLoginComponent, UsuarioSignupComponent, UsuarioListComponent],
    imports: [
        CommonModule, ReactiveFormsModule, AppHeaderModule, FormsModule
    ],
  exports: [UsuarioLoginComponent, UsuarioSignupComponent, UsuarioListComponent]
})
export class UsuarioModule { }
