export enum REQUESTS_TYPES {
    "user_input" = 0,
    "registering_mediator" = 1,
}

export enum RESPONSE_TYPES {
    "statistics_output" = 0,
    "recommended_mediators" = 1
}

export class GenericRequest {
    readonly "request_type": string;
    readonly "request_data": unknown;
    constructor(setType: string, setData: unknown) {
        this.request_type = setType;
        this.request_data = setData;
    } 
}

export interface Mediator {
    "name": string,
    "specialization": string,
    "localization": string,
    "street": string,
    "online": string,
    "ai_rating": number,
    "user_rating": number,
    "number_of_opinions": number,
    "price": number
}

export interface userInput {
    "generic_input": string, 
    "trial_cost": number,
    "location": string,
    "experts_called": boolean,
    "witnesses_called": boolean
}

export class UserInputRequest extends GenericRequest {
    override "request_type" = "user_input";
    override "request_data": userInput

    constructor(setRequest: userInput) {
        super("user_input", setRequest);
        this.request_data = setRequest;
    }
}

export class GenericResponse {
    readonly "response_type": string;
    readonly "response_data": unknown;
    constructor(setType: string, setData: unknown) {
        this.response_type = setType;
        this.response_data = setData;
    } 
}

export interface RecommendedMediatorsInterface {
    "name": string,
    "specialization": string, 
    "localization": string, 
    "ai_rating": number, 
    "user_rating": number,
    "number_of_opinions": number
}

export class RecommendedMediatorsResponse extends GenericResponse {
    override "response_type" = "recommended_mediators";
    override "response_data": RecommendedMediatorsInterface;

    constructor(setResponseData: RecommendedMediatorsInterface) {
        super("recommended_mediators", setResponseData);
        this.response_data = setResponseData;
    }
}

interface response {
    first: {
        cost_of_trial: number,
        time_of_trial: number
    },
    second: Mediator[];
}

export class ReturnResponse {
    "response_type" = "recommended_mediators";
    "response_data": response
}

export interface StatisticsOutputInterface {
    "cost_of_trial": number,
    "time_of_trial": number
}

export class StatisticsOutputResponse extends GenericResponse {
    override "response_type" = "statistics_output";
    override "response_data": StatisticsOutputInterface;

    constructor(setResponseData: StatisticsOutputInterface) {
        super("statistics_output", setResponseData);
        this.response_data = setResponseData;
    }
}
