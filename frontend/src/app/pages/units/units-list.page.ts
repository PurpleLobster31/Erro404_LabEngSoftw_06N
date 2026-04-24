import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
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

  protected search = '';
  protected filteredUnits: UnitCard[] = [];
  protected isLoading = true;
  protected errorMessage: string | null = null;

  ngOnInit(): void {
    this.loadUnits();
  }

  private loadUnits(): void {
    this.isLoading = true;
    this.errorMessage = null;
    this.hospitalMockService.getUnits().subscribe({
      next: (units) => {
        this.filteredUnits = units;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load units:', error);
        this.errorMessage = 'Falha ao carregar unidades. Tente novamente.';
        this.isLoading = false;
      },
    });
  }

  onSearch(value: string): void {
    this.search = value;
    this.hospitalMockService.searchUnits(value).subscribe({
      next: (units) => {
        this.filteredUnits = units;
      },
      error: (error) => {
        console.error('Failed to search units:', error);
        this.errorMessage = 'Falha ao buscar unidades.';
      },
    });
  }
}

