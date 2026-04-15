import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { HospitalMockService, AttendanceRecord } from '../../core/hospital-mock.service';

@Component({
  selector: 'app-attendance-history-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './attendance-history.page.html',
  styleUrl: './attendance-history.page.scss',
})
export class AttendanceHistoryPage {
  private readonly hospitalMockService = inject(HospitalMockService);

  protected readonly records: AttendanceRecord[] = this.hospitalMockService.getAttendanceHistory();

  ratingStars(rating: number): string {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
  }
}
