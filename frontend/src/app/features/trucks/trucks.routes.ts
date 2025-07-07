import { Routes } from '@angular/router';

export const TRUCKS_ROUTES: Routes = [
    {
        path: '',
        loadComponent: () => import('./components/trucks-list/trucks-list.component').then(c => c.TrucksListComponent)
    },
    {
        path: 'control',
        loadComponent: () => import('./components/truck-control-form/truck-control-form.component').then(c => c.TruckControlFormComponent)
    },
    {
        path: ':id',
        loadComponent: () => import('./components/truck-detail/truck-detail.component').then(c => c.TruckDetailComponent)
    },
    {
        path: ':id/edit',
        loadComponent: () => import('./components/truck-control-form/truck-control-form.component').then(c => c.TruckControlFormComponent)
    }
]; 