import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { TruckIconComponent } from '../icons/truck-icon.component';
import { CostsIconComponent } from '../icons/costs-icon.component';
import { ReportsIconComponent } from '../icons/reports-icon.component';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    TranslateModule,
    TruckIconComponent,
    CostsIconComponent,
    ReportsIconComponent
  ],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent {
  @Output() sidebarToggle = new EventEmitter<boolean>();
  
  collapsed = false;

  menuItems = [
    { 
      icon: 'truck', 
      label: 'SIDEBAR.TRUCKS', 
      route: '/trucks' 
    },
    { 
      icon: 'costs', 
      label: 'SIDEBAR.COSTS', 
      route: '/costs' 
    },
    { 
      icon: 'reports', 
      label: 'SIDEBAR.REPORTS', 
      route: '/reports' 
    },
    { 
      icon: 'permissions', 
      label: 'SIDEBAR.PERMISSIONS', 
      route: '/permissions' 
    }
  ];

  toggleSidebar() {
    this.collapsed = !this.collapsed;
    this.sidebarToggle.emit(this.collapsed);
  }

  getTooltipText(text: string): string {
    return this.collapsed ? text : '';
  }
} 