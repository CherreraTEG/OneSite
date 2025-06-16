import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './auth/guards/auth.guard';

const routes: Routes = [
  {
    path: 'login',
    loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: '',
    canActivate: [AuthGuard],
    children: [
      {
        path: 'permisos',
        loadChildren: () => import('./modules/permisos/permisos.module').then(m => m.PermisosModule),
        data: { roles: ['admin', 'supervisor'] }
      },
      {
        path: 'costos',
        loadChildren: () => import('./modules/costos/costos.module').then(m => m.CostosModule),
        data: { roles: ['admin', 'supervisor', 'usuario'] }
      },
      {
        path: 'camiones',
        loadChildren: () => import('./modules/camiones/camiones.module').then(m => m.CamionesModule),
        data: { roles: ['admin', 'supervisor'] }
      },
      {
        path: 'auditoria',
        loadChildren: () => import('./modules/auditoria/auditoria.module').then(m => m.AuditoriaModule),
        data: { roles: ['admin'] }
      }
    ]
  },
  {
    path: 'unauthorized',
    loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: '**',
    redirectTo: ''
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { } 