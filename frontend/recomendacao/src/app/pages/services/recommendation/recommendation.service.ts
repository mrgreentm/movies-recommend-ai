import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {
  private httpClient = inject(HttpClient);
  recommendations = new BehaviorSubject(null);
  getRecommendations(resource: string, recommendations: number, recommendationType: string): Observable<any> {
    const params = new HttpParams();
    params.append('user_id', resource);
    params.append('movie_id', resource);
    params.append('n', recommendations)

    return this.httpClient.get(`http://127.0.0.1:5000/${recommendationType}`, {params});
  }
}
