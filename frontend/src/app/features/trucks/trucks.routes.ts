import { Routes } from '@angular/router';

export const TRUCKS_ROUTES: Routes = [
    {
        path: 'control',
        loadComponent: () => import('./components/truck-control-form/truck-control-form.component').then(c => c.TruckControlFormComponent)
    },
    {
        path: '',
        redirectTo: 'control',
        pathMatch: 'full'
    }
]; 