import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormControl } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { CardComponent } from '@shared/components/card/card.component';
import { InputComponent } from '@shared/components/input/input.component';
import { ButtonComponent } from '@shared/components/button/button.component';

@Component({
  selector: 'app-truck-control-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TranslateModule,
    CardComponent,
    InputComponent,
    ButtonComponent
  ],
  templateUrl: './truck-control-form.component.html',
  styleUrls: ['./truck-control-form.component.scss']
})
export class TruckControlFormComponent implements OnInit {
  truckForm!: FormGroup;

  get warehouseControl(): FormControl { return this.truckForm.get('warehouse') as FormControl; }
  get shipDateControl(): FormControl { return this.truckForm.get('shipDate') as FormControl; }
  get delivDateControl(): FormControl { return this.truckForm.get('delivDate') as FormControl; }
  get customerControl(): FormControl { return this.truckForm.get('customer') as FormControl; }
  get carrierControl(): FormControl { return this.truckForm.get('carrier') as FormControl; }
  get customerFacilityControl(): FormControl { return this.truckForm.get('customerFacility') as FormControl; }
  get loadNumberControl(): FormControl { return this.truckForm.get('loadNumber') as FormControl; }
  get pickupLocationControl(): FormControl { return this.truckForm.get('pickupLocation') as FormControl; }
  get poControl(): FormControl { return this.truckForm.get('po') as FormControl; }
  get timeInControl(): FormControl { return this.truckForm.get('timeIn') as FormControl; }
  get statusControl(): FormControl { return this.truckForm.get('status') as FormControl; }
  get commentsControl(): FormControl { return this.truckForm.get('comments') as FormControl; }
  get numberOfCopiesControl(): FormControl { return this.truckForm.get('numberOfCopies') as FormControl; }

  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
    this.truckForm = this.fb.group({
      warehouse: ['', Validators.required],
      shipDate: [null, Validators.required],
      delivDate: [null, Validators.required],
      customer: ['NO APLICA', Validators.required],
      carrier: ['', Validators.required],
      customerFacility: [''],
      loadNumber: [''],
      pickupLocation: [''],
      po: [''],
      timeIn: [''],
      status: ['Planned', Validators.required],
      comments: [''],
      numberOfCopies: [1, [Validators.required, Validators.min(1)]]
    });
  }

  onSubmit() {
    if (this.truckForm.valid) {
      console.log('Form Submitted!', this.truckForm.value);
    }
  }
} 