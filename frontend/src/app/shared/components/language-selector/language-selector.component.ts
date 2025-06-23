import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-language-selector',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  templateUrl: './language-selector.component.html',
  styleUrls: ['./language-selector.component.scss']
})
export class LanguageSelectorComponent implements OnInit {
  isOpen = false;
  currentLanguage = 'es';
  languages = [
    { code: 'es', name: 'Español' },
    { code: 'en', name: 'English' },
    { code: 'fr', name: 'Français' }
  ];

  constructor(private translateService: TranslateService) {}

  ngOnInit() {
    this.currentLanguage = this.translateService.currentLang || 'es';

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
} 