import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { TranslateModule } from '@ngx-translate/core';
import { ButtonComponent } from '../button/button.component';
import { CardComponent } from '../card/card.component';

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
    ButtonComponent,
    CardComponent
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
        
        <div class="columns-list">
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
        <app-button (click)="selectAll()" variant="secondary">
          {{ 'TRUCKS.LIST.COLUMN_SELECTOR.SELECT_ALL' | translate }}
        </app-button>
        <app-button (click)="deselectAll()" variant="secondary">
          {{ 'TRUCKS.LIST.COLUMN_SELECTOR.DESELECT_ALL' | translate }}
        </app-button>
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
      background: #1a1a2e;
      border-radius: 8px;
      overflow: hidden;
      max-height: 80vh;
      display: flex;
      flex-direction: column;
    }

    .dialog-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 1.5rem;
      background: #16213e;
      border-bottom: 1px solid #0f3460;
    }

    .dialog-header h2 {
      margin: 0;
      color: #fff;
      font-size: 1.25rem;
      font-weight: 600;
    }

    .close-btn {
      background: none;
      border: none;
      color: #545386;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 4px;
      transition: all 0.2s ease;
    }

    .close-btn:hover {
      background: #0f3460;
      color: #fff;
    }

    .dialog-content {
      padding: 1.5rem;
      flex: 1;
      overflow-y: auto;
    }

    .description {
      color: #a0a0a0;
      margin-bottom: 1.5rem;
      font-size: 0.9rem;
    }

    .columns-list {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .column-item {
      padding: 0.5rem 0;
    }

    .checkbox-label {
      display: flex;
      align-items: center;
      cursor: pointer;
      gap: 0.75rem;
      padding: 0.5rem;
      border-radius: 6px;
      transition: background-color 0.2s ease;
    }

    .checkbox-label:hover {
      background: #0f3460;
    }

    .checkbox-input {
      display: none;
    }

    .checkbox-custom {
      width: 18px;
      height: 18px;
      border: 2px solid #545386;
      border-radius: 4px;
      position: relative;
      transition: all 0.2s ease;
      flex-shrink: 0;
    }

    .checkbox-input:checked + .checkbox-custom {
      background: #545386;
      border-color: #545386;
    }

    .checkbox-input:checked + .checkbox-custom::after {
      content: '';
      position: absolute;
      left: 5px;
      top: 2px;
      width: 6px;
      height: 10px;
      border: solid white;
      border-width: 0 2px 2px 0;
      transform: rotate(45deg);
    }

    .column-label {
      color: #fff;
      font-size: 0.95rem;
    }

    .dialog-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 1.5rem;
      background: #16213e;
      border-top: 1px solid #0f3460;
      gap: 0.75rem;
    }

    .spacer {
      flex: 1;
    }

    .dialog-actions app-button {
      min-width: 80px;
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

  toggleColumn(column: ColumnConfig): void {
    column.visible = !column.visible;
  }

  selectAll(): void {
    this.columns.forEach(col => col.visible = true);
  }

  deselectAll(): void {
    this.columns.forEach(col => col.visible = false);
  }

  save(): void {
    this.dialogRef.close(this.columns);
  }

  close(): void {
    this.dialogRef.close();
  }
} 