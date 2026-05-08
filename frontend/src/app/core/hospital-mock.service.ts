import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, from } from 'rxjs';
import { map, catchError, switchMap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

/**
 * Represents a hospital unit from the backend API.
 * This matches the response structure from GET /unidades/
 */
export interface BackendUnit {
  id: number;
  nome: string;
  endereco: string;
  tempo_medio_triagem: number;
  tempo_medio_atendimento: number;
  tempo_medio_total: number;
  latitude: number;
  longitude: number;
  distancia_metros?: number; // Present only when geolocation filtering is used
}

/**
 * Frontend representation of a hospital unit.
 * Simplified for UI display without mock data.
 */
export interface UnitCard {
  id: number;
  name: string;
  address: string;
  waitMinutes: number; // tempo_medio_total from backend
  distanceKm: number;
  latitude: number;
  longitude: number;
  open24h: boolean;
  imageLabel: string;
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

@Injectable({ providedIn: 'root' })
export class HospitalMockService {
  private readonly apiUrl = environment.apiUrl;
  private cachedUnits: UnitCard[] | null = null;
  private userLocation: { latitude: number; longitude: number } | null = null;

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

  constructor(private http: HttpClient) {
    this.initializeGeolocation();
  }

  /**
   * Attempts to get user's geolocation for distance calculations.
   * Silently fails if permission denied.
   */
  private initializeGeolocation(): void {
    if (!navigator.geolocation) {
      console.warn('Geolocation not supported');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.userLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        // Clear cache to fetch new data with geolocation
        this.cachedUnits = null;
      },
      (error) => {
        console.warn('Geolocation permission denied or unavailable:', error);
      },
      { timeout: 5000, enableHighAccuracy: false }
    );
  }

  /**
   * Maps a backend unit to a frontend UnitCard.
   */
  private mapBackendUnit(backendUnit: BackendUnit): UnitCard {
    return {
      id: backendUnit.id,
      name: backendUnit.nome,
      address: backendUnit.endereco,
      waitMinutes: Math.round(backendUnit.tempo_medio_total),
      distanceKm: backendUnit.distancia_metros
        ? Math.round((backendUnit.distancia_metros / 1000) * 10) / 10
        : 0,
      latitude: backendUnit.latitude,
      longitude: backendUnit.longitude,
      open24h: true,
      imageLabel: 'Imagem da unidade',
    };
  }

  /**
   * Fetches units from the backend API.
   * If geolocation is available, includes it for distance calculation and ordering.
   */
  getUnits(): Observable<UnitCard[]> {
    // Return cached units if available
    if (this.cachedUnits) {
      return of(this.cachedUnits);
    }

    // Build query parameters with geolocation if available
    let url = `${this.apiUrl}/unidades/`;
    if (this.userLocation) {
      const params = new URLSearchParams({
        lat: this.userLocation.latitude.toString(),
        lon: this.userLocation.longitude.toString(),
        raio_km: '10.0',
      });
      url = `${url}?${params.toString()}`;
    }

    return this.http.get<BackendUnit[]>(url).pipe(
      map((backendUnits) => {
        const mapped = backendUnits.map((unit) => this.mapBackendUnit(unit));
        this.cachedUnits = mapped;
        return mapped;
      }),
      catchError((error) => {
        console.error('Error fetching units:', error);
        return of([]);
      })
    );
  }

  /**
   * Fetches a single unit by ID.
   */
  getUnitById(id: number): Observable<UnitCard | undefined> {
    return this.http.get<BackendUnit>(`${this.apiUrl}/unidades/${id}`).pipe(
      map((backendUnit) => this.mapBackendUnit(backendUnit)),
      catchError((error) => {
        console.error(`Error fetching unit ${id}:`, error);
        return of(undefined);
      })
    );
  }

  /**
   * Searches units by name or address.
   */
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

  /**
   * Refreshes units list, forcing new API call and attempting geolocation recheck.
   */
  refreshUnits(): Observable<UnitCard[]> {
    this.cachedUnits = null;
    this.initializeGeolocation();
    return this.getUnits();
  }

  /**
   * Returns attendance history (currently static mock data).
   * TODO: Replace with API call when endpoint is available.
   */
  getAttendanceHistory(): AttendanceRecord[] {
    return this.attendanceRecords;
  }
}


