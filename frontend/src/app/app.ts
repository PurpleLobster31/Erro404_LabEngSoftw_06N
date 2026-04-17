import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './shell.html',
  styleUrl: './shell.scss'
})
export class App {
  protected readonly navItems = [
    { label: 'Hospitais', path: '/unidades', icon: 'H' },
    { label: 'Histórico', path: '/historico', icon: 'T' },
    { label: 'Perfil', path: '/perfil', icon: 'P' },
  ];
}
