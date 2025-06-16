import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'permisos',
    loadChildren: () => import('./modules/permisos/permisos.module').then(m => m.PermisosModule)
  },
  {
    path: 'costos',
    loadChildren: () => import('./modules/costos/costos.module').then(m => m.CostosModule)
  },
  {
    path: 'camiones',
    loadChildren: () => import('./modules/camiones/camiones.module').then(m => m.CamionesModule)
  },
  {
    path: 'auditoria',
    loadChildren: () => import('./modules/auditoria/auditoria.module').then(m => m.AuditoriaModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { } 