import { Routes } from '@angular/router';
import { AttendanceHistoryPage } from './pages/attendance/attendance-history.page';
import { ProfilePage } from './pages/profile/profile.page';
import { UnitDetailPage } from './pages/units/unit-detail.page';
import { UnitsListPage } from './pages/units/units-list.page';

export const routes: Routes = [
	{
		path: '',
		pathMatch: 'full',
		redirectTo: 'unidades',
	},
	{
		path: 'unidades',
		component: UnitsListPage,
	},
	{
		path: 'unidades/:id',
		component: UnitDetailPage,
	},
	{
		path: 'historico',
		component: AttendanceHistoryPage,
	},
	{
		path: 'perfil',
		component: ProfilePage,
	},
	{
		path: '**',
		redirectTo: 'unidades',
	},
];
