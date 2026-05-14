import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { HospitalMockService, UnitCard } from '../../core/hospital-mock.service';
import { GeolocationService } from '../../core/geolocation.service';
import { AttendanceService, AttendanceStatusResponse } from '../../core/attendance.service';

// User ID para testes (sem login implementado)
const MOCK_USER_ID = 999;

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
  private readonly geolocationService = inject(GeolocationService);
  private readonly attendanceService = inject(AttendanceService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected unit: UnitCard | null = null;
  protected isLoading = true;
  protected errorMessage: string | null = null;
  
  // Attendance registration state
  protected attendanceButtonLabel: string = 'Registrar Entrada';
  protected isWithinRadius: boolean | null = null;
  protected isRegistering = false;
  protected attendanceMessage: string | null = null;
  protected attendanceError: string | null = null;
  protected currentAttendanceId: number | null = null;

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
          this.validateUserProximity();
          this.checkAttendanceStatus();
        } else {
          this.errorMessage = 'Unidade não encontrada.';
        }
        this.isLoading = false;
        this.changeDetectorRef.markForCheck();
      },
      error: () => {
        this.errorMessage = 'Falha ao carregar unidade. Tente novamente.';
        this.isLoading = false;
        this.changeDetectorRef.markForCheck();
      },
    });
  }

  private validateUserProximity(): void {
    if (!this.unit) return;

    this.geolocationService.getCurrentPosition().subscribe({
      next: (userCoords) => {
        const unitCoords = {
          latitude: this.unit!.latitude,
          longitude: this.unit!.longitude,
        };

        // Em modo mock, sempre habilitar o botão para demonstração
        if (userCoords.isMocked) {
          this.isWithinRadius = true;
          console.log('[DEMO MODE] Botão habilitado para demonstração');
        } else {
          // Modo real: validar distância
          this.isWithinRadius = this.geolocationService.isWithinRadius(
            userCoords,
            unitCoords,
            2000 // 2km como definido no backend
          );
        }

        this.changeDetectorRef.markForCheck();
      },
      error: (err) => {
        console.warn('Erro ao obter geolocalização:', err);
        this.isWithinRadius = false;
        this.changeDetectorRef.markForCheck();
      },
    });
  }

  private checkAttendanceStatus(): void {
    if (!this.unit) return;
    
    this.attendanceService
      .getActiveAttendanceStatus(MOCK_USER_ID, this.unit.id)
      .subscribe({
        next: (status: AttendanceStatusResponse) => {
          this.attendanceButtonLabel = status.label_botao;
          this.currentAttendanceId = status.atendimento_id ?? null;
          this.changeDetectorRef.markForCheck();
        },
        error: (err) => {
          console.warn('Erro ao verificar status de atendimento:', err);
        },
      });
  }

  protected registerAttendance(): void {
    if (!this.unit || this.isWithinRadius === false || this.isRegistering) {
      return;
    }

    this.isRegistering = true;
    this.attendanceMessage = null;
    this.attendanceError = null;

    this.geolocationService.getCurrentPosition().subscribe({
      next: (coords) => {
        if (!this.currentAttendanceId) {
          // Registrar entrada (primeira etapa)
          this.attendanceService
            .registerEntry({
              paciente_id: MOCK_USER_ID,
              unidade_id: this.unit!.id,
              latitude: coords.latitude,
              longitude: coords.longitude,
            })
            .subscribe({
              next: (response) => {
                this.currentAttendanceId = response.id;
                this.attendanceMessage = 'Entrada registrada com sucesso!';
                this.attendanceButtonLabel = 'Registrar Triagem';
                this.isRegistering = false;
                this.changeDetectorRef.markForCheck();
                setTimeout(() => (this.attendanceMessage = null), 3000);
              },
              error: (err) => {
                this.attendanceError =
                  err.error?.detail || 'Erro ao registrar entrada.';
                this.isRegistering = false;
                this.changeDetectorRef.markForCheck();
              },
            });
        } else {
          // Avançar para próxima etapa (triagem ou atendimento)
          this.attendanceService
            .advanceStage(this.currentAttendanceId, {
              latitude: coords.latitude,
              longitude: coords.longitude,
            })
            .subscribe({
              next: (response) => {
                const stageLabel =
                  response.horario_atendimento !== null
                    ? 'Atendimento concluído!'
                    : 'Triagem registrada!';
                this.attendanceMessage = stageLabel;

                // Atualiza botão para próxima etapa
                if (response.status === 'concluido') {
                  this.attendanceButtonLabel = 'Atendimento Concluído';
                } else if (response.horario_triagem !== null) {
                  this.attendanceButtonLabel = 'Registrar Atendimento Médico';
                }

                this.isRegistering = false;
                this.changeDetectorRef.markForCheck();
                setTimeout(() => (this.attendanceMessage = null), 3000);
              },
              error: (err) => {
                this.attendanceError =
                  err.error?.detail || 'Erro ao avançar etapa.';
                this.isRegistering = false;
                this.changeDetectorRef.markForCheck();
              },
            });
        }
      },
      error: (err) => {
        this.attendanceError =
          'Erro ao obter localização. Ative o GPS e tente novamente.';
        this.isRegistering = false;
        this.changeDetectorRef.markForCheck();
      },
    });
  }
}

