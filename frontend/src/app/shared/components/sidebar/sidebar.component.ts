import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
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
  @Input() collapsed: boolean = false;
  @Output() toggleSidebar = new EventEmitter<void>();
  
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
      label: 'SIDEBAR.MENU.TRUCKS', 
      expanded: false,
      subItems: [
        { 
          icon: 'truck', 
          label: 'SIDEBAR.MENU.TRUCKS_CONTROL', 
          route: '/trucks/control' 
        },
        { 
          icon: 'truck', 
          label: 'SIDEBAR.MENU.TRUCKS_CONTROL_WMT', 
          route: '/trucks/control-wmt' 
        }
      ]
    },
    { 
      icon: 'costs', 
      label: 'SIDEBAR.MENU.COSTS', 
      expanded: false,
      subItems: [
        { 
          icon: 'ecommerce', 
          label: 'SIDEBAR.MENU.E_COMMERCE', 
          route: '/costs/ecommerce' 
        },
        { 
          icon: 'costs', 
          label: 'SIDEBAR.MENU.EXTRA_COSTS', 
          route: '/costs/extra-costs' 
        },
        { 
          icon: 'groups', 
          label: 'SIDEBAR.MENU.DISPATCH_GROUPS', 
          route: '/costs/dispatch-groups' 
        }
      ]
    },
    { 
      icon: 'reports', 
      label: 'SIDEBAR.MENU.REPORTS', 
      route: '/reports' 
    },
    { 
      icon: 'audit', 
      label: 'SIDEBAR.MENU.AUDITS', 
      expanded: false,
      subItems: [
        { 
          icon: 'truck', 
          label: 'SIDEBAR.MENU.AUDITS_TRUCKS', 
          route: '/audits/trucks' 
        },
        { 
          icon: 'audit', 
          label: 'SIDEBAR.MENU.AUDITS_WAREHOUSE', 
          route: '/audits/warehouses' 
        }
      ]
    },
    { 
      icon: 'dispatch', 
      label: 'SIDEBAR.MENU.DISPATCHES', 
      route: '/dispatches' 
    },
    { 
      icon: 'rpa', 
      label: 'SIDEBAR.MENU.RPA', 
      route: '/rpa' 
    },
    { 
      icon: 'permissions', 
      label: 'SIDEBAR.MENU.PERMISSIONS', 
      route: '/permissions' 
    }
  ];

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