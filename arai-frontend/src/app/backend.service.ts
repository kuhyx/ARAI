import { EventEmitter, Injectable } from '@angular/core';
import { GenericRequest, GenericResponse, RecommendedMediatorsResponse, StatisticsOutputResponse, UserInputRequest } from './requests-responses';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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

  public sendMessage(message: GenericRequest): void {
    if(message.request_type === "user_input") {
      this.userInputArray.push(message as UserInputRequest);
    }
    const headers = new HttpHeaders().set(
      "Content-Type",
      "application/json"
    );
    console.log(`request: `, JSON.stringify(message));
    this.http.post(this.address, JSON.stringify(message), {headers}).subscribe((response) => {
      console.log(`response: `, response);
    })
  }
}
