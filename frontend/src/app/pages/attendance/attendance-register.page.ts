import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink, Router } from '@angular/router';
import { HospitalMockService } from '../../core/hospital-mock.service';

@Component({
  selector: 'app-attendance-register-page',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule],
  templateUrl: './attendance-register.page.html',
  styleUrl: './attendance-register.page.scss',
})
export class AttendanceRegisterPage implements OnInit {
  private readonly hospitalService = inject(HospitalMockService);
  private readonly formBuilder = inject(FormBuilder);
  private readonly router = inject(Router);

  protected form!: FormGroup;
  protected units: any[] = [];
  protected isLoading = false;
  protected isSaving = false;
  protected errorMessage: string | null = null;
  protected successMessage: string | null = null;
  protected currentStep: 'select-unit' | 'register-times' = 'select-unit';
  protected selectedUnit: any = null;

  ngOnInit(): void {
    this.loadUnits();
    this.initializeForm();
  }

  private loadUnits(): void {
    this.isLoading = true;
    this.hospitalService.getUnits().subscribe({
      next: (units) => {
        this.units = units;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load units:', error);
        this.errorMessage = 'Falha ao carregar unidades.';
        this.isLoading = false;
      },
    });
  }

  private initializeForm(): void {
    const now = new Date();
    const arrivalTime = new Date(now.getTime() - 60 * 60000); // 1 hour ago

    this.form = this.formBuilder.group({
      patientId: [1, Validators.required], // Mock patient ID
      unitId: ['', Validators.required],
      arrivalTime: [this.formatDateTime(arrivalTime), Validators.required],
      triageTime: ['', [Validators.required]],
      attendanceTime: [''],
    });
  }

  protected selectUnit(unit: any): void {
    this.selectedUnit = unit;
    this.form.patchValue({ unitId: unit.id });
    this.currentStep = 'register-times';
    this.errorMessage = null;
  }

  protected goBack(): void {
    this.currentStep = 'select-unit';
    this.selectedUnit = null;
    this.successMessage = null;
  }

  protected onSubmit(): void {
    if (this.form.invalid) {
      this.errorMessage = 'Por favor preencha todos os campos obrigatórios.';
      return;
    }

    this.isSaving = true;
    this.errorMessage = null;

    const formValue = this.form.value;
    const payload = {
      paciente_id: formValue.patientId,
      unidade_id: formValue.unitId,
      horario_chegada: new Date(formValue.arrivalTime).toISOString(),
      horario_triagem: formValue.triageTime
        ? new Date(formValue.triageTime).toISOString()
        : null,
      horario_atendimento: formValue.attendanceTime
        ? new Date(formValue.attendanceTime).toISOString()
        : null,
    };

    // Validate chronological order
    const arrivalTs = new Date(payload.horario_chegada).getTime();
    const triageTs = payload.horario_triagem
      ? new Date(payload.horario_triagem).getTime()
      : null;
    const attendanceTs = payload.horario_atendimento
      ? new Date(payload.horario_atendimento).getTime()
      : null;

    if (triageTs && triageTs <= arrivalTs) {
      this.errorMessage = 'Hora de triagem deve ser posterior à hora de chegada.';
      this.isSaving = false;
      return;
    }

    if (attendanceTs && triageTs && attendanceTs <= triageTs) {
      this.errorMessage = 'Hora de atendimento deve ser posterior à hora de triagem.';
      this.isSaving = false;
      return;
    }

    // Simulate API call
    setTimeout(() => {
      this.isSaving = false;
      this.successMessage =
        'Atendimento registrado com sucesso! Redirecionando...';
      setTimeout(() => {
        this.router.navigate(['/historico']);
      }, 2000);
    }, 1000);
  }

  protected clearForm(): void {
    this.initializeForm();
    this.errorMessage = null;
    this.successMessage = null;
  }

  private formatDateTime(date: Date): string {
    // Format as ISO string without milliseconds, suitable for datetime-local input
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  }
}
