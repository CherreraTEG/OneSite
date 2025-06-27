import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonComponent } from '../button/button.component';

interface ColumnConfig {
  key: string;
  label: string;
  visible: boolean;
}

@Component({
  selector: 'app-column-selector-dialog',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TranslateModule,
    MatDialogModule,
    ButtonComponent
  ],
  template: `
    <div class="column-selector-dialog">
      <div class="dialog-header">
        <h2>{{ 'TRUCKS.LIST.COLUMN_SELECTOR.TITLE' | translate }}</h2>
        <button class="close-btn" (click)="close()" title="{{ 'COMMON.CLOSE' | translate }}">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20" height="20">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="dialog-content">
        <p class="description">{{ 'TRUCKS.LIST.COLUMN_SELECTOR.DESCRIPTION' | translate }}</p>
        
        <div class="quick-actions">
          <app-button (click)="selectAll()" variant="secondary" size="small">
            {{ 'TRUCKS.LIST.COLUMN_SELECTOR.SELECT_ALL' | translate }}
          </app-button>
          <app-button (click)="deselectAll()" variant="secondary" size="small">
            {{ 'TRUCKS.LIST.COLUMN_SELECTOR.DESELECT_ALL' | translate }}
          </app-button>
          <app-button (click)="selectCommon()" variant="secondary" size="small">
            {{ 'TRUCKS.LIST.COLUMN_SELECTOR.SELECT_COMMON' | translate }}
          </app-button>
        </div>
        
        <div class="columns-grid">
          <div class="column-item" *ngFor="let column of columns">
            <label class="checkbox-label">
              <input 
                type="checkbox" 
                [checked]="column.visible"
                (change)="toggleColumn(column)"
                class="checkbox-input"
              >
              <span class="checkbox-custom"></span>
              <span class="column-label">{{ column.label | translate }}</span>
            </label>
          </div>
        </div>
      </div>
      
      <div class="dialog-actions">
        <div class="selected-count">
          {{ 'TRUCKS.LIST.COLUMN_SELECTOR.SELECTED' | translate }}: {{ visibleColumnsCount }}
        </div>
        <div class="spacer"></div>
        <app-button (click)="close()" variant="secondary">
          {{ 'COMMON.CANCEL' | translate }}
        </app-button>
        <app-button (click)="save()" variant="primary">
          {{ 'COMMON.SAVE' | translate }}
        </app-button>
      </div>
    </div>
  `,
  styles: [`
    .column-selector-dialog {
      background: #fff;
      border-radius: 14px;
      overflow: hidden;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      max-width: 95vw;
      box-shadow: 0 8px 32px rgba(60,60,60,0.18);
      border: 1px solid var(--color-secondary);
      box-sizing: border-box;
      overflow-x: hidden;
    }

    .dialog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      background: var(--color-secondary);
      border-bottom: 1px solid var(--color-secondary);
      flex-shrink: 0;
    }

    .dialog-header h2 {
      margin: 0;
      color: var(--color-primary);
      font-size: 1.1rem;
      font-weight: 600;
    }

    .close-btn {
      background: none;
      border: none;
      color: var(--color-primary);
      cursor: pointer;
      padding: 0.25rem;
      border-radius: 4px;
      transition: all 0.2s ease;
    }

    .close-btn:hover {
      background: var(--color-tertiary);
      color: var(--color-primary);
    }

    .dialog-content {
      padding: 1rem;
      flex: 1;
      overflow-y: auto;
      min-height: 0;
      background: #fff;
    }

    .description {
      color: var(--color-primary);
      margin-bottom: 1rem;
      font-size: 0.95rem;
    }

    .quick-actions {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }

    .quick-actions app-button {
      flex: 1;
      min-width: 100px;
      font-size: 0.8rem;
      padding: 0.5rem;
    }

    .columns-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 0.5rem;
      max-height: 50vh;
      overflow-y: auto;
      overflow-x: hidden;
      max-width: 100%;
      box-sizing: border-box;
    }

    .column-item {
      padding: 0.25rem;
      border-radius: 4px;
      background: #fff;
      border: 1px solid var(--color-secondary);
    }

    .checkbox-label {
      display: flex;
      align-items: center;
      cursor: pointer;
      gap: 0.5rem;
      padding: 0.25rem;
      border-radius: 3px;
      transition: background-color 0.2s ease;
    }

    .checkbox-label:hover {
      background: var(--color-tertiary);
    }

    .checkbox-input {
      display: none;
    }

    .checkbox-custom {
      width: 16px;
      height: 16px;
      border: 2px solid var(--color-primary);
      border-radius: 3px;
      position: relative;
      transition: all 0.2s ease;
      flex-shrink: 0;
      background: #fff;
    }

    .checkbox-input:checked + .checkbox-custom {
      background: var(--color-primary);
      border-color: var(--color-primary);
    }

    .checkbox-input:checked + .checkbox-custom::after {
      content: '';
      position: absolute;
      left: 4px;
      top: 1px;
      width: 5px;
      height: 8px;
      border: solid #fff;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
    }

    .column-label {
      color: var(--color-primary);
      font-size: 0.95rem;
      line-height: 1.2;
    }

    .dialog-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.75rem 1rem;
      background: #fff;
      border-top: 1px solid var(--color-secondary);
      gap: 0.75rem;
      flex-shrink: 0;
    }

    .selected-count {
      color: var(--color-primary);
      font-size: 0.95rem;
    }

    .spacer {
      flex: 1;
    }

    .dialog-actions app-button {
      min-width: 70px;
      font-size: 0.95rem;
      padding: 0.5rem 1rem;
    }
  `]
})
export class ColumnSelectorDialogComponent {
  columns: ColumnConfig[];

  constructor(
    public dialogRef: MatDialogRef<ColumnSelectorDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { columns: ColumnConfig[] }
  ) {
    this.columns = data.columns.map(col => ({ ...col }));
  }

  get visibleColumnsCount(): number {
    return this.columns.filter(col => col.visible).length;
  }

  toggleColumn(column: ColumnConfig): void {
    column.visible = !column.visible;
  }

  selectAll(): void {
    this.columns.forEach(col => col.visible = true);
  }

  deselectAll(): void {
    this.columns.forEach(col => col.visible = false);
  }

  selectCommon(): void {
    // Columnas comúnmente usadas
    const commonColumns = ['id_empresa', 'id_warehouse', 'ship_date', 'carrier', 'customer_facility', 'estatus'];
    this.columns.forEach(col => {
      col.visible = commonColumns.includes(col.key);
    });
  }

  save(): void {
    this.dialogRef.close(this.columns);
  }

  close(): void {
    this.dialogRef.close();
  }
} 