import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <router-outlet></router-outlet>
  `,
  styles: []
})
export class AppComponent implements OnInit {
  title = 'OneSite';

  constructor(private translate: TranslateService) {
    // Configurar idiomas disponibles
    translate.addLangs(['en', 'es']);
    translate.setDefaultLang('es');
  }

  ngOnInit() {
    // Intentar usar el idioma del navegador, si no está disponible usar español
    const browserLang = this.translate.getBrowserLang();
    this.translate.use(browserLang?.match(/en|es/) ? browserLang : 'es');
  }
} 