import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export enum AttendanceStatus {
  OPEN = 'em_aberto',
  COMPLETED = 'concluido',
}

/**
 * Resposta ao registrar uma etapa de atendimento.
 */
export interface AttendanceResponse {
  id: number;
  paciente_id: number;
  unidade_id: number;
  horario_chegada: string; // ISO datetime
  horario_triagem: string | null;
  horario_atendimento: string | null;
  status: AttendanceStatus;
}

/**
 * Status do atendimento ativo para controle de UI (qual botão exibir).
 */
export interface AttendanceStatusResponse {
  ativo: boolean;
  atendimento_id?: number;
  label_botao: string;
}

/**
 * Coordenadas para validação de proximidade.
 */
export interface CoordinatesPayload {
  latitude: number;
  longitude: number;
}

/**
 * Payload para registrar novo atendimento (entrada).
 */
export interface CreateAttendancePayload extends CoordinatesPayload {
  paciente_id: number;
  unidade_id: number;
}

/**
 * Payload para avançar etapa do atendimento (triagem, atendimento médico).
 */
export interface AdvanceAttendancePayload extends CoordinatesPayload {}

/**
 * Serviço para gerenciar atendimentos via API backend.
 */
@Injectable({ providedIn: 'root' })
export class AttendanceService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /**
   * Obtém o status do atendimento ativo de um paciente em uma unidade.
   * Retorna qual botão exibir (Registrar Entrada, Triagem, Atendimento Médico).
   */
  getActiveAttendanceStatus(
    pacienteId: number,
    unidadeId: number
  ): Observable<AttendanceStatusResponse> {
    return this.http.get<AttendanceStatusResponse>(
      `${this.apiUrl}/atendimentos/ativo`,
      {
        params: {
          paciente_id: pacienteId.toString(),
          unidade_id: unidadeId.toString(),
        },
      }
    );
  }

  /**
   * Registra a entrada do paciente na unidade (primeira etapa).
   * Validação de proximidade é feita no backend.
   */
  registerEntry(
    payload: CreateAttendancePayload
  ): Observable<AttendanceResponse> {
    return this.http.post<AttendanceResponse>(
      `${this.apiUrl}/atendimentos/`,
      payload
    );
  }

  /**
   * Avança para a próxima etapa do atendimento (triagem ou atendimento médico).
   * Validação de proximidade é feita no backend.
   */
  advanceStage(
    attendanceId: number,
    payload: AdvanceAttendancePayload
  ): Observable<AttendanceResponse> {
    return this.http.patch<AttendanceResponse>(
      `${this.apiUrl}/atendimentos/${attendanceId}/avancar-etapa`,
      payload
    );
  }

  /**
   * Lista todos os atendimentos de um paciente.
   */
  getPatientAttendances(pacienteId: number): Observable<AttendanceResponse[]> {
    return this.http.get<AttendanceResponse[]>(
      `${this.apiUrl}/atendimentos/paciente/${pacienteId}`
    );
  }
}
