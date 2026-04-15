import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { HospitalMockService, UnitCard } from '../../core/hospital-mock.service';

@Component({
  selector: 'app-units-list-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './units-list.page.html',
  styleUrl: './units-list.page.scss',
})
export class UnitsListPage {
  private readonly hospitalMockService = inject(HospitalMockService);

  protected search = '';
  protected filteredUnits: UnitCard[] = this.hospitalMockService.getUnits();

  onSearch(value: string): void {
    this.search = value;
    this.filteredUnits = this.hospitalMockService.searchUnits(value);
  }
}
