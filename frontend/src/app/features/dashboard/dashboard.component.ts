import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { SidebarComponent } from '../../shared/components/sidebar/sidebar.component';
import { LogoutIconComponent } from '../../shared/components/icons/logout-icon.component';
import { LanguageSelectorComponent } from '../../shared/components/language-selector/language-selector.component';
import { CompanyStateService } from '../../core/services/company-state.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule,
    SidebarComponent,
    LogoutIconComponent,
    LanguageSelectorComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  private companySubscription: Subscription | undefined;

  constructor(private companyStateService: CompanyStateService) {}

  ngOnInit() {
    this.companySubscription = this.companyStateService.selectedCompany$.subscribe((companyId: string) => {
      console.log(`Dashboard: La empresa ha cambiado a ${companyId}. Aquí se recargarían los datos.`);
      // TODO: Aquí iría la lógica para recargar los datos del dashboard
      // basados en el nuevo companyId.
    });
  }

  ngOnDestroy() {
    // Es una buena práctica desuscribirse para evitar fugas de memoria.
    if (this.companySubscription) {
      this.companySubscription.unsubscribe();
    }
  }

  // Datos de ejemplo para el dashboard
  userInfo = {
    name: 'John Doe',
    role: 'Administrator',
    lastLogin: new Date().toLocaleDateString()
  };

  // Estado del sidebar
  sidebarCollapsed = false;

  // Idioma actual
  currentLanguage = 'es';

  // Método para recibir el estado del sidebar
  onSidebarToggle(collapsed: boolean) {
    this.sidebarCollapsed = collapsed;
  }

  // Método para manejar el logout
  onLogout() {
    console.log('Logout clicked');
    // Aquí puedes agregar la lógica de logout
  }

  // Método para manejar el cambio de idioma
  onLanguageChange(languageCode: string) {
    this.currentLanguage = languageCode;
    console.log('Language changed to:', languageCode);
    // Aquí puedes agregar la lógica para cambiar el idioma de la aplicación
  }
} 