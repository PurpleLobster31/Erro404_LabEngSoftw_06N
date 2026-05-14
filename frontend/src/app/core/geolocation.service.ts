import { Injectable, inject } from '@angular/core';
import { Observable, from, of } from 'rxjs';
import { map, switchMap, catchError } from 'rxjs/operators';

export interface GeolocationCoordinates {
  latitude: number;
  longitude: number;
  accuracy?: number;
  isMocked?: boolean;
}

/**
 * Serviço para gerenciar geolocalização do usuário.
 * Fornece método para obter coordenadas atuais com tratamento de erros.
 * 
 * MODO MOCK: Para demonstração em sala sem GPS real, use ?geoloc-mock=true na URL
 */
@Injectable({ providedIn: 'root' })
export class GeolocationService {
  // Coordenadas default (São Paulo center) - usadas para mock com pequena variação
  private readonly DEFAULT_LAT = -23.5574;
  private readonly DEFAULT_LNG = -46.6678;

  private detectMockMode(): boolean {
    if (typeof window === 'undefined') return true;
    
    const params = new URLSearchParams(window.location.search);
    // Use mock mode if:
    // 1. Explicitly requested: ?geoloc-mock=true
    // 2. OR if geolocation is not available in browser
    const explicitMock = params.get('geoloc-mock') === 'true';
    const noGeolocation = !navigator.geolocation;
    
    return explicitMock || noGeolocation;
  }

  /**
   * Obtém as coordenadas geográficas atuais do usuário.
   * Em modo mock, retorna coordenadas fixas perto de São Paulo.
   * 
   * @returns Observable que emite coordenadas ou erro se não autorizado/indisponível
   */
  getCurrentPosition(): Observable<GeolocationCoordinates> {
    // Modo mock para demonstração sem GPS real (verificado dinamicamente)
    const isMockMode = this.detectMockMode();
    
    if (isMockMode) {
      console.log('[MOCK MODE] Retornando coordenadas mockadas de São Paulo');
      return of({
        latitude: this.DEFAULT_LAT + (Math.random() - 0.5) * 0.0005, // ±25 metros
        longitude: this.DEFAULT_LNG + (Math.random() - 0.5) * 0.0005,
        accuracy: 20,
        isMocked: true,
      });
    }

    if (!navigator.geolocation) {
      return from(Promise.reject('Geolocalização não disponível neste navegador'));
    }

    return from(
      new Promise<GeolocationCoordinates>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            resolve({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              accuracy: position.coords.accuracy,
              isMocked: false,
            });
          },
          (error) => {
            reject(`Erro de geolocalização: ${error.message}`);
          },
          {
            timeout: 10000,
            enableHighAccuracy: true,
            maximumAge: 0,
          }
        );
      })
    );
  }

  /**
   * Verifica se o usuário está dentro do raio permitido da unidade.
   * 
   * @param userCoords Coordenadas do usuário
   * @param unitCoords Coordenadas da unidade
   * @param radiusMeters Raio permitido em metros (padrão: 2000m = 2km)
   * @returns true se dentro do raio, false caso contrário
   */
  isWithinRadius(
    userCoords: GeolocationCoordinates,
    unitCoords: GeolocationCoordinates,
    radiusMeters: number = 2000
  ): boolean {
    const distance = this.calculateDistance(userCoords, unitCoords);
    return distance <= radiusMeters;
  }

  /**
   * Calcula a distância em metros entre dois pontos (fórmula de Haversine).
   */
  private calculateDistance(
    coords1: GeolocationCoordinates,
    coords2: GeolocationCoordinates
  ): number {
    const R = 6371000; // Raio da Terra em metros
    const lat1Rad = (coords1.latitude * Math.PI) / 180;
    const lat2Rad = (coords2.latitude * Math.PI) / 180;
    const deltaLat = ((coords2.latitude - coords1.latitude) * Math.PI) / 180;
    const deltaLon = ((coords2.longitude - coords1.longitude) * Math.PI) / 180;

    const a =
      Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
      Math.cos(lat1Rad) *
        Math.cos(lat2Rad) *
        Math.sin(deltaLon / 2) *
        Math.sin(deltaLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
  }
}
