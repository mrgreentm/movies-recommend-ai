import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: ()=>import('./pages/search-user/search-user.component').then((c)=>c.SearchUserComponent)
  },
  {
    path: 'recommendations',
    loadComponent: ()=>import('./pages/recommendation/recommendation.component').then((c)=>c.RecommendationComponent)
  }
];
