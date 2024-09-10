import { Component, inject } from '@angular/core';
import { RecommendationService } from '../services/recommendation/recommendation.service';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-recommendation',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule],
  templateUrl: './recommendation.component.html',
  styleUrl: './recommendation.component.scss'
})
export class RecommendationComponent {
  recommendationsService: RecommendationService = inject(RecommendationService);
  recommendations$: Observable<any> = this.recommendationsService.recommendations.asObservable();

}
