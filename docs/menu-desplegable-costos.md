# Menú Desplegable de Costos - OneSite

## Descripción
Este documento describe la implementación y funcionamiento del menú desplegable para la sección de Camiones en el sidebar de OneSite.

## Estructura del Menú

### Menú Principal: Camiones
El menú de Camiones incluye las siguientes subopciones:
- **E-commerce** (`/trucks/ecommerce`)
- **Extra Costos** (`/trucks/extra-costs`) 
- **Grupos de Despacho** (`/trucks/dispatch-groups`)

## Implementación Técnica

### Componente: SidebarComponent
**Archivo:** `frontend/src/app/shared/components/sidebar/sidebar.component.ts`

#### Características principales:
- **Menú desplegable**: Los elementos con submenús se expanden/colapsan al hacer clic
- **Iconos dinámicos**: Cada opción tiene su icono correspondiente
- **Traducciones**: Soporte completo para español e inglés
- **Navegación**: Integración con Angular Router
- **Estados activos**: Resaltado visual de la opción seleccionada

#### Funciones clave:
```typescript
onMenuItemClick(item: MenuItem) // Maneja el clic en elementos del menú
toggleSubmenu(item: MenuItem)   // Expande/colapsa submenús
hasSubItems(item: MenuItem)     // Verifica si un elemento tiene submenús
isActive(item: MenuItem)        // Determina si un elemento está activo
```

### Estructura de Datos
```typescript
interface MenuItem {
  icon: string;           // Icono del elemento
  label: string;          // Etiqueta traducida
  route?: string;         // Ruta de navegación (opcional)
  subItems?: MenuItem[];  // Subelementos (opcional)
  expanded?: boolean;     // Estado de expansión
}
```

### Estilos CSS
**Archivo:** `frontend/src/app/shared/components/sidebar/sidebar.component.scss`

#### Características de diseño:
- **Animaciones suaves**: Transiciones de 0.3s para expansión/colapso
- **Efectos hover**: Resaltado visual al pasar el mouse
- **Responsive**: Adaptación para diferentes tamaños de pantalla
- **Tema consistente**: Colores y estilos alineados con el diseño general

#### Clases CSS importantes:
- `.has-submenu`: Elementos que contienen submenús
- `.expanded`: Estado de expansión del submenú
- `.submenu`: Contenedor de elementos secundarios
- `.submenu-item`: Elementos individuales del submenú

## Funcionalidades

### 1. Expansión/Colapso
- Al hacer clic en "Camiones", el submenú se expande/colapsa
- Icono de flecha indica el estado (▶ para cerrado, ▼ para abierto)
- Animación suave durante la transición

### 2. Navegación
- Los elementos del submenú navegan a rutas específicas
- Estado activo se mantiene según la ruta actual
- Integración completa con Angular Router

### 3. Responsive Design
- En modo colapsado, solo se muestran iconos
- Tooltips aparecen al hacer hover en modo colapsado
- Adaptación automática para dispositivos móviles

### 4. Traducciones
- Soporte completo para español e inglés
- Claves de traducción en `frontend/src/assets/i18n/`
- Cambio dinámico de idioma

## Archivos de Traducción

### Español (`es.json`)
```json
{
  "SIDEBAR": {
    "TRUCKS": "Camiones",
    "E_COMMERCE": "E-commerce",
    "EXTRA_COSTS": "Extra Costos",
    "DISPATCH_GROUPS": "Grupos de Despacho"
  }
}
```

### Inglés (`en.json`)
```json
{
  "SIDEBAR": {
    "TRUCKS": "Trucks",
    "E_COMMERCE": "E-commerce",
    "EXTRA_COSTS": "Extra Costs",
    "DISPATCH_GROUPS": "Dispatch Groups"
  }
}
```

## Iconos Utilizados

### Componentes de Iconos
- `TruckIconComponent`: Icono principal de camiones
- `EcommerceIconComponent`: Icono para E-commerce
- `CostsIconComponent`: Icono para costos
- `GroupsIconComponent`: Icono para grupos de despacho

### Ubicación
Todos los iconos están en: `frontend/src/app/shared/components/icons/`

## Debugging y Logs

### Logs de Depuración
El componente incluye logs de consola para facilitar el debugging:
- Inicialización del sidebar
- Clics en elementos del menú
- Estado de expansión de submenús
- Verificación de elementos con submenús

### Cómo usar los logs
1. Abrir las herramientas de desarrollador del navegador
2. Ir a la pestaña Console
3. Interactuar con el menú para ver los logs

## Próximos Pasos

### Mejoras Sugeridas
1. **Persistencia de estado**: Guardar el estado de expansión en localStorage
2. **Accesibilidad**: Agregar soporte para navegación por teclado
3. **Animaciones avanzadas**: Implementar animaciones más elaboradas
4. **Temas**: Soporte para múltiples temas de color

### Nuevas Funcionalidades
1. **Búsqueda en menú**: Filtrado de opciones
2. **Favoritos**: Marcado de opciones frecuentes
3. **Notificaciones**: Indicadores de nuevas funcionalidades
4. **Personalización**: Reordenamiento de elementos del menú

## Troubleshooting

### Problemas Comunes

#### 1. Menú no se expande
- Verificar que el elemento tenga `subItems` definidos
- Revisar la consola para errores de JavaScript
- Confirmar que los estilos CSS estén cargados

#### 2. Iconos no aparecen
- Verificar que los componentes de iconos estén importados
- Confirmar que las rutas de los iconos sean correctas
- Revisar que no haya errores de compilación

#### 3. Traducciones no funcionan
- Verificar que los archivos de traducción estén en la ubicación correcta
- Confirmar que las claves de traducción coincidan
- Revisar la configuración del módulo de traducciones

### Soluciones

#### Reiniciar el servidor de desarrollo
```bash
cd frontend
npm start
```

#### Limpiar cache
```bash
cd frontend
npm run clean
npm install
npm start
```

#### Verificar compilación
```bash
cd frontend
npm run build
```

## Conclusión

El menú desplegable de costos está completamente implementado y funcional. Proporciona una experiencia de usuario intuitiva con navegación clara y diseño responsive. La implementación sigue las mejores prácticas de Angular y mantiene la consistencia con el resto de la aplicación OneSite. 