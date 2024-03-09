import { EventEmitter, Injectable } from '@angular/core';
import { GenericRequest, GenericResponse, RecommendedMediatorsResponse, StatisticsOutputResponse, UserInputRequest, userInput } from './requests-responses';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  address = "localhost:8080";

  public genericResponsesArray: GenericResponse[] = [];
  public userInputArray: UserInputRequest[] = [];
  public recommendedMediatorsResponsesArray: RecommendedMediatorsResponse[] = [];
  public recommendedMediatorsResponsesArrayEvent = new EventEmitter<RecommendedMediatorsResponse>();
  public statisticsOutputResponseArray: StatisticsOutputResponse[] = [];
  public statisticsOutputResponseArrayEvent = new EventEmitter<StatisticsOutputResponse>();
  

  private websocket: WebSocket | null = null;

  constructor() {
    this.connect();
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

  private connect(): void {
    this.websocket = new WebSocket(`http://${this.address}`);
    this.websocket.onmessage = (event: MessageEvent) => {
      this.filterMessages(event as unknown as GenericResponse);
    };
    // Listen for messages
    this.websocket.on('message', (message: GenericResponse) => {
      this.filterMessages(message);
    });
  }

  public sendMessage(message: GenericRequest): void {
    if(message.request_type === "user_input") {
      this.userInputArray.push(message as UserInputRequest);
    }
    this.socket.emit('message', message);
  }
}
