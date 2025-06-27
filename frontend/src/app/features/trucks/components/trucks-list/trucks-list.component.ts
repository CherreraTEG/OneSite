import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormControl } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { CardComponent } from '@shared/components/card/card.component';
import { InputComponent } from '@shared/components/input/input.component';
import { ButtonComponent } from '@shared/components/button/button.component';
import { TrucksService } from '../../trucks.service';
import { Truck } from '../../truck.model';
import { SidebarComponent } from '@shared/components/sidebar/sidebar.component';
import { LanguageSelectorComponent } from '@shared/components/language-selector/language-selector.component';
import { LogoutIconComponent } from '@shared/components/icons/logout-icon.component';
import { PlusIconComponent } from '@shared/components/icons/plus-icon.component';
import { XMarkIconComponent } from '@shared/components/icons/x-mark-icon.component';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { TruckControlFormComponent } from '../truck-control-form/truck-control-form.component';
import { ColumnSelectorDialogComponent } from '../../../../shared/components/column-selector-dialog/column-selector-dialog.component';

interface ColumnConfig {
  key: string;
  label: string;
  visible: boolean;
}

@Component({
  selector: 'app-trucks-list',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TranslateModule,
    CardComponent,
    InputComponent,
    ButtonComponent,
    SidebarComponent,
    LanguageSelectorComponent,
    LogoutIconComponent,
    PlusIconComponent,
    XMarkIconComponent,
    MatDialogModule
  ],
  templateUrl: './trucks-list.component.html',
  styleUrls: ['./trucks-list.component.scss']
})
export class TrucksListComponent implements OnInit {
  trucks: Truck[] = [];
  filteredTrucks: Truck[] = [];
  loading = false;
  filterForm: FormGroup;
  currentPage = 1;
  itemsPerPage = 10;
  totalItems = 0;

  // Configuración de columnas
  columns: ColumnConfig[] = [
    { key: 'id_empresa', label: 'FORMS.TRUCK_CONTROL.ID_EMPRESA', visible: true },
    { key: 'id_warehouse', label: 'FORMS.TRUCK_CONTROL.ID_WAREHOUSE', visible: true },
    { key: 'ship_date', label: 'FORMS.TRUCK_CONTROL.SHIPDATE', visible: true },
    { key: 'carrier', label: 'FORMS.TRUCK_CONTROL.CARRIER', visible: true },
    { key: 'customer_facility', label: 'FORMS.TRUCK_CONTROL.CUSTOMER_FACILITY', visible: true },
    { key: 'estatus', label: 'FORMS.TRUCK_CONTROL.ESTATUS', visible: true }
  ];

  // Estado del sidebar
  sidebarCollapsed: boolean = window.innerWidth <= 900;

  // Método para alternar el estado del sidebar
  toggleSidebar() {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  filtersCollapsed = true;

  toggleFiltersCollapse() {
    this.filtersCollapsed = !this.filtersCollapsed;
  }

  @ViewChild('btn', { static: false }) newButton!: ButtonComponent;

  newButtonIconColor: string = '#545386';

  onNewButtonMouseEnter() {
    this.newButtonIconColor = '#fff';
  }
  onNewButtonMouseLeave() {
    this.newButtonIconColor = '#545386';
  }

  constructor(
    private trucksService: TrucksService,
    private fb: FormBuilder,
    private router: Router,
    private dialog: MatDialog
  ) {
    this.filterForm = this.fb.group({
      id_empresa: [''],
      id_warehouse: [''],
      carrier: [''],
      customer_facility: [''],
      estatus: [''],
      ship_date_from: [''],
      ship_date_to: [''],
      deliv_date_from: [''],
      deliv_date_to: ['']
    });
  }

  ngOnInit(): void {
    this.loadColumnPreferences();
    this.loadTrucks();
    this.setupFilterListener();
  }

  // Método helper para acceder dinámicamente a las propiedades del objeto Truck
  getTruckValue(truck: Truck, key: string): any {
    return (truck as any)[key];
  }

  // Cargar preferencias de columnas desde localStorage
  loadColumnPreferences(): void {
    const savedColumns = localStorage.getItem('trucks-table-columns');
    if (savedColumns) {
      try {
        const parsedColumns = JSON.parse(savedColumns);
        this.columns = this.columns.map(col => ({
          ...col,
          visible: parsedColumns[col.key] !== undefined ? parsedColumns[col.key] : col.visible
        }));
      } catch (error) {
        console.error('Error cargando preferencias de columnas:', error);
      }
    }
  }

  // Guardar preferencias de columnas en localStorage
  saveColumnPreferences(): void {
    const columnPreferences = this.columns.reduce((acc, col) => {
      acc[col.key] = col.visible;
      return acc;
    }, {} as Record<string, boolean>);
    
    localStorage.setItem('trucks-table-columns', JSON.stringify(columnPreferences));
  }

  // Obtener columnas visibles
  get visibleColumns(): ColumnConfig[] {
    return this.columns.filter(col => col.visible);
  }

  // Abrir modal de selección de columnas
  openColumnSelector(): void {
    const dialogRef = this.dialog.open(ColumnSelectorDialogComponent, {
      width: '400px',
      data: { columns: [...this.columns] }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.columns = result;
        this.saveColumnPreferences();
      }
    });
  }

  loadTrucks(): void {
    this.loading = true;
    this.trucksService.getTrucks().subscribe({
      next: (trucks) => {
        this.trucks = trucks;
        this.applyFilters();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error cargando camiones:', error);
        this.loading = false;
      }
    });
  }

  setupFilterListener(): void {
    this.filterForm.valueChanges.subscribe(() => {
      this.currentPage = 1;
      this.applyFilters();
    });
  }

  applyFilters(): void {
    const filters = this.filterForm.value;
    this.filteredTrucks = this.trucks.filter(truck => {
      return (
        (!filters.id_empresa || truck.id_empresa?.toString().includes(filters.id_empresa)) &&
        (!filters.id_warehouse || truck.id_warehouse?.toString().includes(filters.id_warehouse)) &&
        (!filters.carrier || truck.carrier?.toLowerCase().includes(filters.carrier.toLowerCase())) &&
        (!filters.customer_facility || truck.customer_facility?.toLowerCase().includes(filters.customer_facility.toLowerCase())) &&
        (!filters.estatus || (truck.estatus?.toString() || '').toLowerCase().includes(filters.estatus.toLowerCase())) &&
        this.filterByDateRange(truck.ship_date, filters.ship_date_from, filters.ship_date_to) &&
        this.filterByDateRange(truck.deliv_date, filters.deliv_date_from, filters.deliv_date_to)
      );
    });
    this.totalItems = this.filteredTrucks.length;
  }

  filterByDateRange(date: string | undefined, fromDate: string, toDate: string): boolean {
    if (!date) return true;
    if (!fromDate && !toDate) return true;
    
    const truckDate = new Date(date);
    const from = fromDate ? new Date(fromDate) : null;
    const to = toDate ? new Date(toDate) : null;
    
    if (from && truckDate < from) return false;
    if (to && truckDate > to) return false;
    
    return true;
  }

  clearFilters(): void {
    this.filterForm.reset();
  }

  viewTruck(truck: Truck): void {
    this.router.navigate(['/trucks', truck.id]);
  }

  editTruck(truck: Truck): void {
    this.router.navigate(['/trucks', truck.id, 'edit']);
  }

  deleteTruck(truck: Truck): void {
    if (confirm('¿Está seguro de que desea eliminar este registro?')) {
      this.trucksService.deleteTruck(truck.id!).subscribe({
        next: () => {
          this.loadTrucks();
        },
        error: (error) => {
          console.error('Error eliminando camión:', error);
        }
      });
    }
  }

  createNewTruck(): void {
    this.openTruckControlDialog();
  }

  openTruckControlDialog(): void {
    const dialogRef = this.dialog.open(TruckControlFormComponent, {
      width: '98vw',
      maxWidth: '900px',
      maxHeight: '90vh',
      panelClass: 'truck-control-dialog',
      autoFocus: false
    });

    dialogRef.afterClosed().subscribe(result => {
      setTimeout(() => {
        if (this.newButton) {
          this.newButton.blur();
        }
      });
      if (result === true) {
        this.loadTrucks();
      }
    });
  }

  get paginatedTrucks(): Truck[] {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    return this.filteredTrucks.slice(startIndex, endIndex);
  }

  get totalPages(): number {
    return Math.ceil(this.totalItems / this.itemsPerPage);
  }

  changePage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  get pages(): number[] {
    const pages: number[] = [];
    const maxPages = Math.min(5, this.totalPages);
    const startPage = Math.max(1, this.currentPage - Math.floor(maxPages / 2));
    
    for (let i = 0; i < maxPages; i++) {
      pages.push(startPage + i);
    }
    
    return pages;
  }

  // Getters para los controles del formulario de filtros
  get idEmpresaFilterControl(): FormControl {
    return this.filterForm.get('id_empresa') as FormControl;
  }

  get idWarehouseFilterControl(): FormControl {
    return this.filterForm.get('id_warehouse') as FormControl;
  }

  get carrierFilterControl(): FormControl {
    return this.filterForm.get('carrier') as FormControl;
  }

  get customerFacilityFilterControl(): FormControl {
    return this.filterForm.get('customer_facility') as FormControl;
  }

  get estatusFilterControl(): FormControl {
    return this.filterForm.get('estatus') as FormControl;
  }

  get shipDateFromFilterControl(): FormControl {
    return this.filterForm.get('ship_date_from') as FormControl;
  }

  get shipDateToFilterControl(): FormControl {
    return this.filterForm.get('ship_date_to') as FormControl;
  }

  get delivDateFromFilterControl(): FormControl {
    return this.filterForm.get('deliv_date_from') as FormControl;
  }

  get delivDateToFilterControl(): FormControl {
    return this.filterForm.get('deliv_date_to') as FormControl;
  }

  getMaxItems(): number {
    return Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
  }
} 