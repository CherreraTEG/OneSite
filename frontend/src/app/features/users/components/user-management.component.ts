import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-user-management',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TranslateModule
  ],
  templateUrl: './user-management.component.html',
  styleUrls: ['./user-management.component.scss']
})
export class UserManagementComponent implements OnInit {
  // Formularios
  userForm!: FormGroup;
  searchForm!: FormGroup;

  // Datos
  users: any[] = [];
  companies: any[] = [];
  permissionTypes = ['read', 'write', 'admin'];

  // Estados
  isLoading = false;
  isCreating = false;
  selectedUser: any = null;
  editMode = false;

  // Tabla
  displayedColumns: string[] = ['username', 'email', 'full_name', 'companies', 'is_active', 'actions'];

  constructor(
    private fb: FormBuilder,
    private translate: TranslateService
  ) {
    this.initializeForms();
  }

  ngOnInit(): void {
    // Datos de ejemplo para pruebas
    this.users = [
      {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        full_name: 'Administrador',
        is_active: true,
        is_superuser: true,
        companies: []
      }
    ];
    
    this.companies = [
      {
        id: '1',
        Company: 'Empresa de Prueba'
      }
    ];
  }

  initializeForms(): void {
    this.userForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(50)]],
      email: ['', [Validators.required, Validators.email]],
      full_name: [''],
      password: ['', [Validators.required, Validators.minLength(6)]],
      is_active: [true],
      is_superuser: [false],
      company_permissions: this.fb.array([])
    });

    this.searchForm = this.fb.group({
      search: [''],
      active_only: [true]
    });
  }

  get companyPermissionsArray(): FormArray {
    return this.userForm.get('company_permissions') as FormArray;
  }

  loadUsers(): void {
    // Implementación simplificada para pruebas
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
    }, 1000);
  }

  loadCompanies(): void {
    // Implementación simplificada para pruebas
    console.log('Empresas cargadas');
  }

  onSearch(): void {
    this.loadUsers();
  }

  createUser(): void {
    this.editMode = false;
    this.selectedUser = null;
    this.resetForm();
    this.addCompanyPermission(); // Agregar al menos una empresa por defecto
  }

  editUser(user: any): void {
    this.editMode = true;
    this.selectedUser = user;
    this.loadUserIntoForm(user);
  }

  loadUserIntoForm(user: any): void {
    // Limpiar array de permisos
    while (this.companyPermissionsArray.length !== 0) {
      this.companyPermissionsArray.removeAt(0);
    }

    // Cargar datos del usuario
    this.userForm.patchValue({
      username: user.username,
      email: user.email,
      full_name: user.full_name,
      password: '', // No mostrar la contraseña
      is_active: user.is_active,
      is_superuser: user.is_superuser
    });

    // Cargar permisos de empresa
    user.companies.forEach((company: any) => {
      this.addCompanyPermission(company.company_code, company.permission_type);
    });

    // Si no hay empresas, agregar una vacía
    if (user.companies.length === 0) {
      this.addCompanyPermission();
    }

    // Hacer la contraseña opcional en modo edición
    this.userForm.get('password')?.clearValidators();
    this.userForm.get('password')?.updateValueAndValidity();
  }

  addCompanyPermission(companyCode: string = '', permissionType: string = 'read'): void {
    const permissionGroup = this.fb.group({
      company_code: [companyCode, Validators.required],
      permission_type: [permissionType, Validators.required]
    });

    this.companyPermissionsArray.push(permissionGroup);
  }

  removeCompanyPermission(index: number): void {
    this.companyPermissionsArray.removeAt(index);
  }

  onSubmit(): void {
    if (this.userForm.invalid) {
      this.markFormGroupTouched(this.userForm);
      return;
    }

    const formData = this.userForm.value;
    
    // Si es edición y no se proporcionó contraseña, no enviarla
    if (this.editMode && !formData.password) {
      delete formData.password;
    }

    this.isCreating = true;

    // Simulación de guardado
    setTimeout(() => {
      this.isCreating = false;
      const message = this.editMode ? 'Usuario actualizado exitosamente' : 'Usuario creado exitosamente';
      this.showSuccess(message);
      this.loadUsers();
      this.resetForm();
      this.selectedUser = null;
      this.editMode = false;
    }, 1000);
  }

  deleteUser(user: any): void {
    if (confirm(`¿Estás seguro de que quieres desactivar al usuario ${user.username}?`)) {
      this.showSuccess('Usuario desactivado exitosamente');
      this.loadUsers();
    }
  }

  resetForm(): void {
    this.userForm.reset({
      is_active: true,
      is_superuser: false
    });
    
    // Limpiar array de permisos
    while (this.companyPermissionsArray.length !== 0) {
      this.companyPermissionsArray.removeAt(0);
    }

    // Restaurar validadores de contraseña
    this.userForm.get('password')?.setValidators([Validators.required, Validators.minLength(6)]);
    this.userForm.get('password')?.updateValueAndValidity();
  }

  getCompanyName(companyCode: string): string {
    const company = this.companies.find(c => c.id.toString() === companyCode);
    return company ? company.Company : companyCode;
  }

  getUserCompaniesDisplay(user: any): string {
    if (user.companies.length === 0) return 'Sin empresas';
    return user.companies.map((c: any) => `${this.getCompanyName(c.company_code)} (${c.permission_type})`).join(', ');
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.keys(formGroup.controls).forEach(key => {
      const control = formGroup.get(key);
      control?.markAsTouched();

      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  private showSuccess(message: string): void {
    console.log('SUCCESS:', message);
    // TODO: Implementar notificación
  }

  private showError(message: string): void {
    console.error('ERROR:', message);
    // TODO: Implementar notificación
  }
}