import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
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

  protected unit: UnitCard | null = null;
  protected ratingText = '';
  protected isLoading = true;
  protected errorMessage: string | null = null;

  ngOnInit(): void {
    this.loadUnit();
  }

  private loadUnit(): void {
    const unitId = Number(this.activatedRoute.snapshot.paramMap.get('id') ?? '1');
    this.isLoading = true;
    this.errorMessage = null;

    this.hospitalMockService.getUnitById(unitId).subscribe({
      next: (unit) => {
        if (unit) {
          this.unit = unit;
          this.ratingText = unit.rating.toFixed(1);
        } else {
          this.errorMessage = 'Unidade não encontrada.';
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load unit:', error);
        this.errorMessage = 'Falha ao carregar unidade. Tente novamente.';
        this.isLoading = false;
      },
    });
  }

  ratingStars(rating: number): string {
    const fullStars = Math.max(0, Math.min(5, Math.round(rating)));
    return '★'.repeat(fullStars) + '☆'.repeat(5 - fullStars);
  }
}
