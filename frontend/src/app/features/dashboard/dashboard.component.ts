import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardComponent } from '../../shared/components/card/card.component';
import { ButtonComponent } from '../../shared/components/button/button.component';
import { SidebarComponent } from '../../shared/components/sidebar/sidebar.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, CardComponent, ButtonComponent, SidebarComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {
  // Datos de ejemplo para el dashboard
  userInfo = {
    name: 'John Doe',
    role: 'Administrator',
    lastLogin: new Date().toLocaleDateString()
  };

  quickStats = [
    { title: 'Total Users', value: '1,234', icon: '👥' },
    { title: 'Active Sessions', value: '42', icon: '🟢' },
    { title: 'Pending Tasks', value: '15', icon: '📋' }
  ];

  // Estado del sidebar
  sidebarCollapsed = false;

  // Método para recibir el estado del sidebar
  onSidebarToggle(collapsed: boolean) {
    this.sidebarCollapsed = collapsed;
  }
} 