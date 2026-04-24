import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface UnitCard {
  id: number;
  name: string;
  distanceKm: number;
  waitMinutes: number;
  rating: number;
  address: string;
  open24h: boolean;
  imageLabel: string;
  feedback: Array<{
    author: string;
    rating: number;
    text: string;
  }>;
}

export interface AttendanceRecord {
  id: number;
  unitName: string;
  doctor: string;
  specialty: string;
  status: 'Concluído' | 'Em aberto';
  waitLabel: string;
  date: string;
  rating?: number;
  actionLabel?: string;
}

interface BackendUnit {
  id: number;
  nome: string;
  endereco: string;
  tempo_medio_minutos: number;
  localizacao?: { type: string; coordinates: [number, number] };
  imagem?: string;
}

@Injectable({ providedIn: 'root' })
export class HospitalMockService {
  private readonly apiUrl = environment.apiUrl;
  private cachedUnits: UnitCard[] | null = null;

  private readonly mockFeedback = {
    1: [
      {
        author: 'Marina Silva',
        rating: 5,
        text: 'Atendimento excelente e rápido. Equipe muito atenciosa e profissional.',
      },
      {
        author: 'João Santos',
        rating: 4,
        text: 'Boa infraestrutura e médicos competentes. Apenas a espera foi um pouco longa.',
      },
      {
        author: 'Ana Costa',
        rating: 4,
        text: 'Ambiente organizado e fluxo claro de atendimento.',
      },
    ],
    2: [
      {
        author: 'Lucas Almeida',
        rating: 4,
        text: 'Atendimento bom e bem sinalizado.',
      },
      {
        author: 'Bianca Nunes',
        rating: 5,
        text: 'Estrutura confortável e equipe prestativa.',
      },
    ],
    3: [
      {
        author: 'Pedro Santos',
        rating: 4,
        text: 'Boa organização e cadastro rápido.',
      },
    ],
  } as Record<number, Array<{ author: string; rating: number; text: string }>>;

  private readonly attendanceRecords: AttendanceRecord[] = [
    {
      id: 1,
      unitName: 'Pronto Socorro - Jardim Silveira',
      doctor: 'Dr. Roberto Silva',
      specialty: 'Clínico Geral',
      status: 'Concluído',
      waitLabel: 'Esperou: 42 min',
      date: '13 Mar 2026',
      rating: 4,
    },
    {
      id: 2,
      unitName: 'Pronto Socorro - São Camilo',
      doctor: 'Dr. Rogério Nirim',
      specialty: 'Clínico Geral',
      status: 'Em aberto',
      waitLabel: 'Esperou: 68 min',
      date: '06 Fev 2026',
      actionLabel: 'Avaliar Atendimento',
    },
    {
      id: 3,
      unitName: 'UPA Central',
      doctor: 'Dra. Laura Mendes',
      specialty: 'Ortopedia',
      status: 'Concluído',
      waitLabel: 'Esperou: 29 min',
      date: '01 Fev 2026',
      rating: 5,
    },
  ];

  constructor(private http: HttpClient) {}

  private mapBackendUnit(backendUnit: BackendUnit, index: number): UnitCard {
    // Mock distance calculation - in a real app, this would come from the backend or be calculated with geolocation
    const mockDistances = [0.8, 2.1, 3.7];
    const mockRatings = [4.8, 4.4, 4.6];

    return {
      id: backendUnit.id,
      name: backendUnit.nome,
      address: backendUnit.endereco,
      waitMinutes: backendUnit.tempo_medio_minutos,
      rating: mockRatings[index] || 4.5,
      distanceKm: mockDistances[index] || Math.random() * 5 + 0.5,
      open24h: true,
      imageLabel: 'Imagem da unidade',
      feedback: this.mockFeedback[backendUnit.id] || [],
    };
  }

  getUnits(): Observable<UnitCard[]> {
    // If we have cached units, return them to avoid multiple API calls
    if (this.cachedUnits) {
      return of(this.cachedUnits);
    }

    return this.http.get<BackendUnit[]>(`${this.apiUrl}/unidades/`).pipe(
      map((backendUnits) => {
        const mapped = backendUnits.map((unit, index) => this.mapBackendUnit(unit, index));
        this.cachedUnits = mapped;
        return mapped;
      }),
      catchError((error) => {
        console.error('Error fetching units:', error);
        // Fallback to mock data if API fails
        return this.getMockUnits();
      })
    );
  }

  getUnitById(id: number): Observable<UnitCard | undefined> {
    return this.http.get<BackendUnit>(`${this.apiUrl}/unidades/${id}`).pipe(
      map((backendUnit) => this.mapBackendUnit(backendUnit, 0)),
      catchError((error) => {
        console.error(`Error fetching unit ${id}:`, error);
        // Fallback to mock data
        return of(this.getMockUnitById(id));
      })
    );
  }

  searchUnits(query: string): Observable<UnitCard[]> {
    return this.getUnits().pipe(
      map((units) => {
        const normalized = query.trim().toLowerCase();

        if (!normalized) {
          return units;
        }

        return units.filter(
          (unit) =>
            unit.name.toLowerCase().includes(normalized) ||
            unit.address.toLowerCase().includes(normalized)
        );
      })
    );
  }

  getAttendanceHistory(): AttendanceRecord[] {
    return this.attendanceRecords;
  }

  // Fallback mock data methods
  private getMockUnits(): Observable<UnitCard[]> {
    return of([
      {
        id: 1,
        name: 'Pronto Socorro - Jardim Silveira',
        distanceKm: 0.8,
        waitMinutes: 37,
        rating: 4.8,
        address: 'Via Paiaguás, 331-269 - Jardim Silveira, Barueri',
        open24h: true,
        imageLabel: 'Imagem da unidade',
        feedback: this.mockFeedback[1] || [],
      },
      {
        id: 2,
        name: 'Pronto Socorro - São Camilo',
        distanceKm: 2.1,
        waitMinutes: 53,
        rating: 4.4,
        address: 'Rua São Camilo, 120 - Centro',
        open24h: true,
        imageLabel: 'Imagem da unidade',
        feedback: this.mockFeedback[2] || [],
      },
      {
        id: 3,
        name: 'UPA Central',
        distanceKm: 3.7,
        waitMinutes: 42,
        rating: 4.6,
        address: 'Av. Central, 880 - Centro',
        open24h: true,
        imageLabel: 'Imagem da unidade',
        feedback: this.mockFeedback[3] || [],
      },
    ]);
  }

  private getMockUnitById(id: number): UnitCard | undefined {
    return [
      {
        id: 1,
        name: 'Pronto Socorro - Jardim Silveira',
        distanceKm: 0.8,
        waitMinutes: 37,
        rating: 4.8,
        address: 'Via Paiaguás, 331-269 - Jardim Silveira, Barueri',
        open24h: true,
        imageLabel: 'Imagem da unidade',
        feedback: this.mockFeedback[1] || [],
      },
      {
        id: 2,
        name: 'Pronto Socorro - São Camilo',
        distanceKm: 2.1,
        waitMinutes: 53,
        rating: 4.4,
        address: 'Rua São Camilo, 120 - Centro',
        open24h: true,
        imageLabel: 'Imagem da unidade',
        feedback: this.mockFeedback[2] || [],
      },
      {
        id: 3,
        name: 'UPA Central',
        distanceKm: 3.7,
        waitMinutes: 42,
        rating: 4.6,
        address: 'Av. Central, 880 - Centro',
        open24h: true,
        imageLabel: 'Imagem da unidade',
        feedback: this.mockFeedback[3] || [],
      },
    ].find((unit) => unit.id === id);
  }
}

