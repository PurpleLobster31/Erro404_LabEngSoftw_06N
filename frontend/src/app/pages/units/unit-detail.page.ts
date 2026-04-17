import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HospitalMockService } from '../../core/hospital-mock.service';

@Component({
  selector: 'app-unit-detail-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './unit-detail.page.html',
  styleUrl: './unit-detail.page.scss',
})
export class UnitDetailPage {
  private readonly activatedRoute = inject(ActivatedRoute);
  private readonly hospitalMockService = inject(HospitalMockService);

  protected readonly unit = this.getCurrentUnit();

  protected ratingText = this.unit.rating.toFixed(1);

  private getCurrentUnit() {
    const unitId = Number(this.activatedRoute.snapshot.paramMap.get('id') ?? '1');
    return this.hospitalMockService.getUnitById(unitId) ?? this.hospitalMockService.getUnits()[0];
  }

  ratingStars(rating: number): string {
    const fullStars = Math.max(0, Math.min(5, Math.round(rating)));
    return '★'.repeat(fullStars) + '☆'.repeat(5 - fullStars);
  }
}
