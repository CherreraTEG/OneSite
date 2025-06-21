import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { CompanyStateService } from '../../../core/services/company-state.service';
import { TruckIconComponent } from '../icons/truck-icon.component';
import { CostsIconComponent } from '../icons/costs-icon.component';
import { ReportsIconComponent } from '../icons/reports-icon.component';
import { GroupsIconComponent } from '../icons/groups-icon.component';

interface MenuItem {
  icon: string;
  label: string;
  route?: string;
  subItems?: MenuItem[];
  expanded?: boolean;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    TranslateModule,
    TruckIconComponent,
    CostsIconComponent,
    ReportsIconComponent,
    GroupsIconComponent
  ],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  @Output() sidebarToggle = new EventEmitter<boolean>();
  
  collapsed = false;
  selectedCompany: string = '1';

  companies = [
    { id: '1', name: 'Elite Flower' },
    { id: '2', name: 'FlorAndina' },
    { id: '3', name: 'Agroelite' }
  ];

  constructor(
    private companyStateService: CompanyStateService,
    private router: Router
  ) {}

  ngOnInit() {
    this.selectedCompany = this.companyStateService.getSelectedCompany();
  }

  menuItems: MenuItem[] = [
    { 
      icon: 'truck', 
      label: 'SIDEBAR.TRUCKS', 
      expanded: false,
      subItems: [
        { 
          icon: 'ecommerce', 
          label: 'SIDEBAR.E_COMMERCE', 
          route: '/trucks/ecommerce' 
        },
        { 
          icon: 'costs', 
          label: 'SIDEBAR.EXTRA_COSTS', 
          route: '/trucks/extra-costs' 
        },
        { 
          icon: 'groups', 
          label: 'SIDEBAR.DISPATCH_GROUPS', 
          route: '/trucks/dispatch-groups' 
        }
      ]
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

  onMenuItemClick(item: MenuItem) {
    if (this.hasSubItems(item)) {
      this.toggleSubmenu(item);
    } else if (item.route) {
      this.router.navigate([item.route]);
    }
  }

  toggleSubmenu(item: MenuItem) {
    if (item.subItems) {
      item.expanded = !item.expanded;
    }
  }

  isActive(item: MenuItem): boolean {
    if (this.hasSubItems(item) && item.subItems) {
      return item.subItems.some(subItem => this.isActive(subItem));
    } else if (item.route) {
      return this.router.isActive(item.route, false);
    }
    return false;
  }

  onCompanyChange(event: Event) {
    const selectedId = (event.target as HTMLSelectElement).value;
    this.selectedCompany = selectedId;
    this.companyStateService.setSelectedCompany(selectedId);
  }

  getTooltipText(text: string): string {
    return this.collapsed ? text : '';
  }

  hasSubItems(item: MenuItem): boolean {
    return !!(item.subItems && item.subItems.length > 0);
  }
} 