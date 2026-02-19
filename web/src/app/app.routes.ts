import { Routes } from '@angular/router';

import { Home } from './pages/home/home';
import { CoursesComponent } from './pages/courses/courses';
import { Feed } from './pages/feed/feed';
import { Statistics } from './pages/statistics/statistics';

export const routes: Routes = [
  { path: '', component: Home, pathMatch: 'full' },
  { path: 'courses', component: CoursesComponent },
  { path: 'feed', component: Feed },
  { path: 'statistics', component: Statistics },
  { path: '**', redirectTo: '' }
];
