import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { CardComponent } from '@shared/components/card/card.component';
import { ButtonComponent } from '@shared/components/button/button.component';
import { TrucksService } from '../../trucks.service';
import { Truck } from '../../truck.model';

@Component({
  selector: 'app-truck-detail',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule,
    CardComponent,
    ButtonComponent
  ],
  templateUrl: './truck-detail.component.html',
  styleUrls: ['./truck-detail.component.scss']
})
export class TruckDetailComponent implements OnInit {
  truck?: Truck;
  loading = false;
  error = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private trucksService: TrucksService
  ) { }

  ngOnInit(): void {
    this.loadTruck();
  }

  loadTruck(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.error = true;
      return;
    }

    this.loading = true;
    this.trucksService.getTruck(parseInt(id)).subscribe({
      next: (truck: Truck) => {
        this.truck = truck;
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error cargando camión:', error);
        this.error = true;
        this.loading = false;
      }
    });
  }

  editTruck(): void {
    if (this.truck?.id) {
      this.router.navigate(['/trucks', this.truck.id, 'edit']);
    }
  }

  goBack(): void {
    this.router.navigate(['/trucks']);
  }

  deleteTruck(): void {
    if (!this.truck?.id) return;

    if (confirm('¿Está seguro de que desea eliminar este registro?')) {
      this.trucksService.deleteTruck(this.truck.id).subscribe({
        next: () => {
          this.router.navigate(['/trucks']);
        },
        error: (error) => {
          console.error('Error eliminando camión:', error);
        }
      });
    }
  }

  formatDate(date: string | undefined): string {
    if (!date) return '-';
    return new Date(date).toLocaleDateString('es-ES');
  }

  formatTime(time: string | undefined): string {
    if (!time) return '-';
    return time;
  }
} 