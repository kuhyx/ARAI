import { EventEmitter, Injectable } from '@angular/core';
import { GenericRequest, GenericResponse, RecommendedMediatorsResponse, StatisticsOutputResponse, UserInputRequest } from './requests-responses';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  address = "http://localhost:5000";

  public genericResponsesArray: GenericResponse[] = [];
  public userInputArray: UserInputRequest[] = [];
  public recommendedMediatorsResponsesArray: RecommendedMediatorsResponse[] = [];
  public recommendedMediatorsResponsesArrayEvent = new EventEmitter<RecommendedMediatorsResponse>();
  public statisticsOutputResponseArray: StatisticsOutputResponse[] = [];
  public statisticsOutputResponseArrayEvent = new EventEmitter<StatisticsOutputResponse>();
  


  constructor(private http: HttpClient) {
  }

  private filterMessages(message: GenericResponse) {
    this.genericResponsesArray.push(message);
    if(message.response_type === "recommended_mediators") {
      this.recommendedMediatorsResponsesArray.push(message as RecommendedMediatorsResponse);
      this.recommendedMediatorsResponsesArrayEvent.next(message as RecommendedMediatorsResponse);
    }
    if(message.response_type === "statistics_output") {
      this.statisticsOutputResponseArray.push(message as StatisticsOutputResponse);
      this.statisticsOutputResponseArrayEvent.next(message as StatisticsOutputResponse);
    }
  }

  public sendMessage(message: GenericRequest): Promise<GenericResponse> {
    return new Promise((resolve, reject) => {
      if (message.request_type === "user_input") {
        this.userInputArray.push(message as UserInputRequest);
      }
      const headers = new HttpHeaders().set("Content-Type", "application/json");
  
      console.log(`request: `, JSON.stringify(message));
  
      this.http.post<GenericResponse>(this.address, JSON.stringify(message), { headers }).subscribe({
        next: (response) => {
          console.log(`response: `, response);
          resolve(response);
        },
        error: (error) => {
          console.error(`backendService, sendMessage, error: `, error);
          reject(error);
        }
      });
    });
  }

  private serializeToQueryParams(message: GenericRequest): HttpParams {
    let params = new HttpParams();
    // Use a type assertion here to let TypeScript know the real type of the keys
    (Object.keys(message) as Array<keyof GenericRequest>).forEach(key => {
      const value = message[key];
      if (value !== undefined) {
        // Assuming all values are either string or can be converted to string
        params = params.append(key, String(value));
      }
    });
    return params;
  }
  
  
}
