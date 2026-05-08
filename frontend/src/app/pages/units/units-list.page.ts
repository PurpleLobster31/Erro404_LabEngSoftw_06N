import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { RouterLink } from '@angular/router';
import { HospitalMockService, UnitCard } from '../../core/hospital-mock.service';

@Component({
  selector: 'app-units-list-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './units-list.page.html',
  styleUrl: './units-list.page.scss',
})
export class UnitsListPage implements OnInit {
  private readonly hospitalMockService = inject(HospitalMockService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected search = '';
  protected filteredUnits: UnitCard[] = [];
  protected isLoading = true;
  protected errorMessage: string | null = null;
  protected hasGeolocation = false;

  ngOnInit(): void {
    this.loadUnits();
  }

  private loadUnits(): void {
    console.error('[MEDTIME-DEBUG] loadUnits() called');
    this.isLoading = true;
    this.errorMessage = null;
    this.hospitalMockService.getUnits().subscribe({
      next: (units) => {
        console.error('[MEDTIME-DEBUG] Subscription received', units.length, 'units');
        this.filteredUnits = units;
        this.hasGeolocation = units.length > 0 && units.some((u) => u.distanceKm > 0);
        this.isLoading = false;
        this.changeDetectorRef.markForCheck(); // Explicitly trigger change detection
      },
      error: (error) => {
        console.error('[MEDTIME-DEBUG] Subscription error:', error);
        console.error('Falha ao carregar unidades:', error);
        this.errorMessage = 'Falha ao carregar unidades. Tente novamente.';
        this.isLoading = false;
        this.changeDetectorRef.markForCheck();
      },
    });
  }

  onSearch(value: string): void {
    this.search = value;
    this.hospitalMockService.searchUnits(value).subscribe({
      next: (units) => {
        this.filteredUnits = units;
        this.changeDetectorRef.markForCheck();
      },
      error: (error) => {
        console.error('Falha ao buscar unidades:', error);
        this.errorMessage = 'Falha ao buscar unidades.';
      },
    });
  }

  onRefresh(): void {
    this.loadUnits();
  }
}


