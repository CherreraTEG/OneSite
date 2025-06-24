import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormControl } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { CardComponent } from '@shared/components/card/card.component';
import { InputComponent } from '@shared/components/input/input.component';
import { ButtonComponent } from '@shared/components/button/button.component';
import { TrucksService } from '../../trucks.service';
import { Truck } from '../../truck.model';

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
  @Input() truck?: Truck; // Para edición
  truckForm!: FormGroup;
  isEditMode = false;
  // Campos de auditoría
  updateDate?: string;
  updateUser?: string;

  constructor(private fb: FormBuilder, private trucksService: TrucksService) { }

  ngOnInit(): void {
    this.truckForm = this.fb.group({
      id_empresa: [this.truck?.id_empresa || '', Validators.required],
      id_warehouse: [this.truck?.id_warehouse || '', Validators.required],
      ship_date: [this.truck?.ship_date || '', Validators.required],
      deliv_date: [this.truck?.deliv_date || ''],
      carrier: [this.truck?.carrier || '', Validators.required],
      customer_facility: [this.truck?.customer_facility || ''],
      po: [this.truck?.po || ''],
      qty: [this.truck?.qty || ''],
      estatus: [this.truck?.estatus || ''],
      time_in: [this.truck?.time_in || ''],
      door: [this.truck?.door || ''],
      time_out: [this.truck?.time_out || ''],
      comments: [this.truck?.comments || ''],
      pickup_location: [this.truck?.pickup_location || ''],
      load_number: [this.truck?.load_number || ''],
      id_customer: [this.truck?.id_customer || ''],
      estado_cargue: [this.truck?.estado_cargue || ''],
      file_name: [this.truck?.file_name || '']
    });
    if (this.truck) {
      this.isEditMode = true;
      this.updateDate = this.truck.update_date;
      this.updateUser = this.truck.update_user;
    }
  }

  // Getters para cada control del formulario
  get idEmpresaControl(): FormControl {
    return this.truckForm.get('id_empresa') as FormControl;
  }

  get idWarehouseControl(): FormControl {
    return this.truckForm.get('id_warehouse') as FormControl;
  }

  get shipDateControl(): FormControl {
    return this.truckForm.get('ship_date') as FormControl;
  }

  get delivDateControl(): FormControl {
    return this.truckForm.get('deliv_date') as FormControl;
  }

  get carrierControl(): FormControl {
    return this.truckForm.get('carrier') as FormControl;
  }

  get customerFacilityControl(): FormControl {
    return this.truckForm.get('customer_facility') as FormControl;
  }

  get poControl(): FormControl {
    return this.truckForm.get('po') as FormControl;
  }

  get qtyControl(): FormControl {
    return this.truckForm.get('qty') as FormControl;
  }

  get estatusControl(): FormControl {
    return this.truckForm.get('estatus') as FormControl;
  }

  get timeInControl(): FormControl {
    return this.truckForm.get('time_in') as FormControl;
  }

  get doorControl(): FormControl {
    return this.truckForm.get('door') as FormControl;
  }

  get timeOutControl(): FormControl {
    return this.truckForm.get('time_out') as FormControl;
  }

  get commentsControl(): FormControl {
    return this.truckForm.get('comments') as FormControl;
  }

  get pickupLocationControl(): FormControl {
    return this.truckForm.get('pickup_location') as FormControl;
  }

  get loadNumberControl(): FormControl {
    return this.truckForm.get('load_number') as FormControl;
  }

  get idCustomerControl(): FormControl {
    return this.truckForm.get('id_customer') as FormControl;
  }

  get estadoCargueControl(): FormControl {
    return this.truckForm.get('estado_cargue') as FormControl;
  }

  get fileNameControl(): FormControl {
    return this.truckForm.get('file_name') as FormControl;
  }

  onSubmit() {
    if (this.truckForm.valid) {
      const truckData: Truck = this.truckForm.value;
      if (this.isEditMode && this.truck?.id) {
        this.trucksService.updateTruck(this.truck.id, truckData).subscribe();
      } else {
        this.trucksService.createTruck(truckData).subscribe();
      }
    }
  }
} 