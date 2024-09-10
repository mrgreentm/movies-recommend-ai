import { Component, inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatSliderModule } from '@angular/material/slider';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { RecommendationService } from '../services/recommendation/recommendation.service';
import { take } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-user',
  standalone: true,
  imports: [
    MatCardModule,
    MatButtonToggleModule,
    MatSliderModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    CommonModule
  ],
  templateUrl: './search-user.component.html',
  styleUrl: './search-user.component.scss'
})
export class SearchUserComponent {
  recommendationService: RecommendationService = inject(RecommendationService);
  router: Router = inject(Router);

  disabled = false;
  max = 100;
  min = 0;
  showTicks = false;
  step = 1;
  thumbLabel = false;
  value = 1;
  recommendationType = 'collaborative';
  idResource = null;

  getRecommendation(): void {
    this.recommendationService
    .getRecommendations(this.idResource as any, this.value, this.recommendationType)
    .pipe(take(1))
    .subscribe((res)=>{
      this.recommendationService.recommendations.next(res);
      this.router.navigateByUrl('/recommendations')
    })
  }
}
