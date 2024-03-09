import { EventEmitter, Injectable } from '@angular/core';
import { io, Socket } from 'socket.io-client';
import { GenericRequest, GenericResponse, RecommendedMediatorsResponse, StatisticsOutputResponse, UserInput, UserInputRequest } from './requests-responses';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  address = "localhost:1227";

  public genericResponsesArray: GenericResponse[] = [];
  public userInputArray: UserInputRequest[] = [];
  public recommendedMediatorsResponsesArray: RecommendedMediatorsResponse[] = [];
  public recommendedMediatorsResponsesArrayEvent = new EventEmitter<RecommendedMediatorsResponse>();
  public statisticsOutputResponseArray: StatisticsOutputResponse[] = [];
  public statisticsOutputResponseArrayEvent = new EventEmitter<StatisticsOutputResponse>();
  

  private socket: Socket =  io(`http://${this.address}`);

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
    this.socket = io(`http://${this.address}`);
    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    // Listen for messages
    this.socket.on('message', (message: GenericResponse) => {
      this.filterMessages(message);
    });
  }

  public sendMessage(message: GenericRequest): void {
    if(message.request_type === "user_input") {
      this.userInputArray.push(message as UserInput);
    }
    this.socket.emit('message', message);
  }
}
