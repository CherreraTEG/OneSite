import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-language-selector',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  template: `
    <div class="language-selector">
      <button 
        class="language-button"
        (click)="toggleDropdown()"
        title="{{ 'COMMON.LANGUAGE' | translate }}"
      >
        <span class="current-flag">{{ getCurrentLanguageFlag() }}</span>
        <span class="current-code">{{ getCurrentLanguageName() }}</span>
        <span class="dropdown-arrow">▼</span>
      </button>
      
      <div class="dropdown-menu" [class.open]="isOpen">
        <div 
          *ngFor="let lang of languages" 
          class="language-option"
          (click)="selectLanguage(lang.code)"
          [class.active]="lang.code === currentLanguage"
        >
          <span class="flag">{{ lang.flag }}</span>
          <span class="name">{{ lang.name }}</span>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['./language-selector.component.scss']
})
export class LanguageSelectorComponent implements OnInit {
  isOpen = false;
  currentLanguage = 'es';
  languages = [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'English', flag: '🇺🇸' }
  ];

  constructor(private translateService: TranslateService) {}

  ngOnInit() {
    // Obtener el idioma actual del servicio de traducción
    this.currentLanguage = this.translateService.currentLang || 'es';
    
    // Si no hay idioma configurado, establecer español como predeterminado
    if (!this.translateService.currentLang) {
      this.translateService.setDefaultLang('es');
      this.translateService.use('es');
    }
  }

  toggleDropdown() {
    this.isOpen = !this.isOpen;
  }

  selectLanguage(languageCode: string) {
    this.currentLanguage = languageCode;
    this.translateService.use(languageCode);
    this.isOpen = false;
  }

  getCurrentLanguageName(): string {
    const lang = this.languages.find(l => l.code === this.currentLanguage);
    return lang ? lang.name : 'Español';
  }

  getCurrentLanguageFlag(): string {
    const lang = this.languages.find(l => l.code === this.currentLanguage);
    return lang ? lang.flag : '🇪🇸';
  }
} 