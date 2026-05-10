import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, from } from 'rxjs';
import { map, catchError, switchMap, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

/**
 * Representa uma unidade hospitalar da API backend.
 * Corresponde à estrutura de resposta de GET /unidades/
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
  distancia_metros?: number; // Presente apenas quando filtro geográfico é usado
}

/**
 * Representação frontend de uma unidade hospitalar.
 * Simplificada para exibição na UI sem dados mockados.
 */
export interface UnitCard {
  id: number;
  name: string;
  address: string;
  waitMinutes: number; // tempo_medio_total do backend
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
    // Temporarily disabled - geolocation initialization might be causing issues
    // this.initializeGeolocation();
  }

  /**
   * Tenta obter a geolocalização do usuário para cálculos de distância.
   * Falha silenciosamente se a permissão for negada.
   */
  private initializeGeolocation(): void {
    if (!navigator.geolocation) {
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        this.userLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
      },
      () => {
        // Geolocation permission denied or unavailable
      },
      { timeout: 5000, enableHighAccuracy: false }
    );
  }

  /**
   * Mapeia uma unidade backend para um UnitCard frontend.
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
   * Busca unidades da API backend.
   * Se geolocalização estiver disponível, inclui para cálculo e ordenação de distância.
   */
  getUnits(): Observable<UnitCard[]> {
    // Construir parâmetros de query com geolocalização se disponível
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
      tap((data: BackendUnit[]) => {
        this.cachedUnits = data.map((unit) => this.mapBackendUnit(unit));
      }),
      map((backendUnits: BackendUnit[]) => {
        return backendUnits.map((unit) => this.mapBackendUnit(unit));
      }),
      catchError(() => {
        return of([]);
      })
    );
  }

  /**
   * Busca uma unidade única por ID.
   */
  getUnitById(id: number): Observable<UnitCard | undefined> {
    return this.http.get<BackendUnit>(`${this.apiUrl}/unidades/${id}`).pipe(
      map((backendUnit) => this.mapBackendUnit(backendUnit)),
      catchError(() => {
        return of(undefined);
      })
    );
  }

  /**
   * Busca unidades por nome ou endereço.
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
   * Atualiza lista de unidades, forçando nova chamada de API e tentando recheck de geolocalização.
   */
  refreshUnits(): Observable<UnitCard[]> {
    this.cachedUnits = null;
    this.initializeGeolocation();
    return this.getUnits();
  }

  /**
   * Retorna histórico de atendimentos (atualmente dados estáticos mockados).
   * TODO: Substituir com chamada de API quando endpoint estiver disponível.
   */
  getAttendanceHistory(): AttendanceRecord[] {
    return this.attendanceRecords;
  }
}


