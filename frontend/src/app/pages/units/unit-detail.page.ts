import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HospitalMockService, UnitCard } from '../../core/hospital-mock.service';

@Component({
  selector: 'app-unit-detail-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './unit-detail.page.html',
  styleUrl: './unit-detail.page.scss',
})
export class UnitDetailPage implements OnInit {
  private readonly activatedRoute = inject(ActivatedRoute);
  private readonly hospitalMockService = inject(HospitalMockService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected unit: UnitCard | null = null;
  protected isLoading = true;
  protected errorMessage: string | null = null;

  ngOnInit(): void {
    this.loadUnit();
  }

  private loadUnit(): void {
    const unitId = Number(this.activatedRoute.snapshot.paramMap.get('id') ?? '1');
    console.error('[MEDTIME-DEBUG] loadUnit() called for ID:', unitId);
    this.isLoading = true;
    this.errorMessage = null;

    this.hospitalMockService.getUnitById(unitId).subscribe({
      next: (unit) => {
        console.error('[MEDTIME-DEBUG] Got unit:', unit);
        if (unit) {
          this.unit = unit;
        } else {
          this.errorMessage = 'Unidade não encontrada.';
        }
        this.isLoading = false;
        this.changeDetectorRef.markForCheck(); // Explicitly trigger change detection
      },
      error: (error) => {
        console.error('[MEDTIME-DEBUG] Error loading unit:', error);
        console.error('Falha ao carregar unidade:', error);
        this.errorMessage = 'Falha ao carregar unidade. Tente novamente.';
        this.isLoading = false;
        this.changeDetectorRef.markForCheck();
      },
    });
  }
}

