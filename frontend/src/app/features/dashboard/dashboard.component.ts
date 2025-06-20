import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { SidebarComponent } from '../../shared/components/sidebar/sidebar.component';
import { LogoutIconComponent } from '../../shared/components/icons/logout-icon.component';
import { LanguageSelectorComponent } from '../../shared/components/language-selector/language-selector.component';

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
export class DashboardComponent {
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