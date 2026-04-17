import { Injectable } from '@angular/core';

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

@Injectable({ providedIn: 'root' })
export class HospitalMockService {
  private readonly units: UnitCard[] = [
    {
      id: 1,
      name: 'Pronto Socorro - Jardim Silveira',
      distanceKm: 0.8,
      waitMinutes: 37,
      rating: 4.8,
      address: 'Via Paiaguás, 331-269 - Jardim Silveira, Barueri',
      open24h: true,
      imageLabel: 'Imagem da unidade',
      feedback: [
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
      feedback: [
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
      feedback: [
        {
          author: 'Pedro Santos',
          rating: 4,
          text: 'Boa organização e cadastro rápido.',
        },
      ],
    },
  ];

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

  getUnits(): UnitCard[] {
    return this.units;
  }

  getUnitById(id: number): UnitCard | undefined {
    return this.units.find((unit) => unit.id === id);
  }

  searchUnits(query: string): UnitCard[] {
    const normalized = query.trim().toLowerCase();

    if (!normalized) {
      return this.units;
    }

    return this.units.filter((unit) =>
      unit.name.toLowerCase().includes(normalized) ||
      unit.address.toLowerCase().includes(normalized)
    );
  }

  getAttendanceHistory(): AttendanceRecord[] {
    return this.attendanceRecords;
  }
}
