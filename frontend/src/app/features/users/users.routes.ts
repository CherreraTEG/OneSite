import { Routes } from '@angular/router';
import { UserManagementComponent } from './components/user-management.component';

export const usersRoutes: Routes = [
  {
    path: '',
    component: UserManagementComponent,
    data: { title: 'USER_MANAGEMENT.TITLE' }
  }
];