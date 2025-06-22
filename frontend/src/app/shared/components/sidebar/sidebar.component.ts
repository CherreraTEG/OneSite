import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { CompanyStateService } from '../../../core/services/company-state.service';
import { TruckIconComponent } from '../icons/truck-icon.component';
import { CostsIconComponent } from '../icons/costs-icon.component';
import { ReportsIconComponent } from '../icons/reports-icon.component';
import { PermissionsIconComponent } from '../icons/permissions-icon.component';
import { CompanyIconComponent } from '../icons/company-icon.component';
import { AuditIconComponent } from '../icons/audit-icon.component';
import { DispatchIconComponent } from '../icons/dispatch-icon.component';
import { RpaIconComponent } from '../icons/rpa-icon.component';

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
    PermissionsIconComponent,
    CompanyIconComponent,
    AuditIconComponent,
    DispatchIconComponent,
    RpaIconComponent
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
    console.log('Sidebar initialized with menu items:', this.menuItems);
  }

  menuItems: MenuItem[] = [
    { 
      icon: 'truck', 
      label: 'SIDEBAR.TRUCKS', 
      expanded: false,
      subItems: [
        { 
          icon: 'truck', 
          label: 'SIDEBAR.TRUCK_CONTROL', 
          route: '/trucks/control' 
        },
        { 
          icon: 'truck', 
          label: 'SIDEBAR.TRUCK_CONTROL_WMT', 
          route: '/trucks/control-wmt' 
        }
      ]
    },
    { 
      icon: 'costs', 
      label: 'SIDEBAR.COSTS', 
      expanded: false,
      subItems: [
        { 
          icon: 'ecommerce', 
          label: 'SIDEBAR.E_COMMERCE', 
          route: '/costs/ecommerce' 
        },
        { 
          icon: 'costs', 
          label: 'SIDEBAR.EXTRA_COSTS', 
          route: '/costs/extra-costs' 
        },
        { 
          icon: 'groups', 
          label: 'SIDEBAR.DISPATCH_GROUPS', 
          route: '/costs/dispatch-groups' 
        }
      ]
    },
    { 
      icon: 'reports', 
      label: 'SIDEBAR.REPORTS', 
      route: '/reports' 
    },
    { 
      icon: 'audit', 
      label: 'SIDEBAR.AUDITS', 
      route: '/audits' 
    },
    { 
      icon: 'dispatch', 
      label: 'SIDEBAR.DISPATCHES', 
      route: '/dispatches' 
    },
    { 
      icon: 'rpa', 
      label: 'SIDEBAR.RPA', 
      route: '/rpa' 
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
    console.log('Menu item clicked:', item);
    if (this.hasSubItems(item)) {
      console.log('Item has subitems, toggling submenu');
      this.toggleSubmenu(item);
    } else if (item.route) {
      console.log('Navigating to route:', item.route);
      this.router.navigate([item.route]);
    }
  }

  toggleSubmenu(item: MenuItem) {
    if (item.subItems) {
      item.expanded = !item.expanded;
      console.log('Submenu toggled for item:', item.label, 'Expanded:', item.expanded);
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
    const hasSubItems = !!(item.subItems && item.subItems.length > 0);
    console.log('Checking if item has subitems:', item.label, hasSubItems);
    return hasSubItems;
  }
} 