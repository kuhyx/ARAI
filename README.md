# ARAI — AI-Powered Legal Mediation Assistant

> Full-stack web application that leverages **GPT-4** to help Polish citizens resolve legal disputes through mediation instead of costly court proceedings. Built in **48 hours** at a legal-tech hackathon.

[![Angular](https://img.shields.io/badge/Angular-17-DD0031?logo=angular)](https://angular.io/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?logo=flask)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

Navigating the Polish legal system is complex and expensive. **ARAI** simplifies the process by allowing users to describe their dispute in plain language, then automatically:

1. **Classifies the case** into 20+ legal categories (civil, labour, commercial, IP, family, etc.) using GPT-4
2. **Estimates court costs and duration** based on real statistical data from Polish district and regional courts
3. **Recommends and ranks mediators** best suited for the case using a custom AI scoring algorithm
4. **Enables direct contact** with chosen mediators through the platform

The goal is to reduce the burden on courts by directing eligible disputes toward mediation — a faster, cheaper, and less adversarial resolution path.

---

## Key Features

| Feature | Description |
|---|---|
| **Natural Language Case Input** | Users describe their legal problem in free-form Polish text — no legal knowledge required |
| **AI Case Categorization** | GPT-4 classifies the dispute across 20+ legal domains (IP, labour, family, real estate, etc.) |
| **Court Cost Estimation** | Calculates expected court fees, attorney costs, and expert witness expenses using official Polish fee schedules |
| **Trial Duration Prediction** | Estimates case length in months using real court statistics (district vs. regional courts) |
| **Mediator Matching** | Ranks mediators by specialization overlap, AI compatibility score, user ratings, and price |
| **Multi-Step Wizard UI** | Guided 3-screen flow: Case Input → Cost Overview → Mediator Recommendations |

---

## Architecture

```
┌──────────────────────┐       HTTP/JSON        ┌──────────────────────┐
│                      │ ──────────────────────► │                      │
│   Angular 17 SPA     │                         │   Flask REST API     │
│   (Material Design)  │ ◄────────────────────── │   (Python)           │
│                      │                         │                      │
└──────────────────────┘                         └──────┬───────────────┘
   Port 4200                                            │
   • Case input form                                    ├── GPT-4 API
   • Cost visualization                                 │   (case classification
   • Mediator cards                                     │    & scoring)
   • Email contact modal                                │
                                                        ├── pandas
┌──────────────────────┐                                │   (court statistics
│  WebSocket Relay     │                                │    from Excel data)
│  (Node.js)           │                                │
│  Port 8080           │                                └── Mediator DB
└──────────────────────┘                                    (scoring engine)
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Angular 17, Angular Material, RxJS, SCSS, TypeScript |
| **Backend** | Python 3, Flask, Flask-CORS, pandas, openpyxl |
| **AI / NLP** | OpenAI GPT-4 (case categorization, legal classification, mediator relevance scoring) |
| **Real-time** | WebSocket relay server (Node.js, `ws` library) |
| **Data** | Polish court statistics (Excel), official court fee schedules |
| **Build Tools** | Angular CLI, pnpm, pip |

---

## Project Structure

```
ARAI/
├── arai-frontend/          # Angular 17 SPA — form wizard, results display, Material UI
│   └── src/app/
│       ├── case-input/     # Main form: case description, trial value, location, toggles
│       ├── cost-view/      # Court cost and duration estimate display
│       ├── mediators-list/ # Ranked mediator cards with ratings and contact
│       ├── email-input/    # Modal dialog for contacting a mediator
│       ├── backend.service # HTTP client for Flask API communication
│       ├── koszta.service  # Shared state for cost/duration data between views
│       └── mediatorzy.service # Shared state for mediator list between views
│
├── Backend_correct/        # Flask REST API — orchestrates the full pipeline
│   └── app.py              # POST / → categorize → estimate costs → score mediators
│
├── simple-ws/              # Lightweight WebSocket relay server (Node.js)
│   └── ws.js
│
├── statystyki/             # Court statistics data pipeline (pandas + Excel)
│   └── load_data.py        # CLI tool for cost estimation from court data
│
├── franek/                 # ML experimentation — scoring prototypes and iteration
│   ├── scoring_final_final_2.py
│   ├── kategoryzacja_spraw.py
│   └── scoring.py
│
└── example_input.txt       # Sample case description for testing
```

---

## How It Works

### 1. User Submits a Case

The Angular frontend presents a form where the user provides:
- **Case description** in plain Polish (e.g., *"pracodawca nie wypłacił mi wynagrodzenia za ostatnie 2 miesiące i mnie zwolnił"*)
- **Dispute value** (PLN) — used to calculate court fees
- **Location** — for mediator proximity matching
- **Toggles** — whether expert witnesses or regular witnesses are involved

### 2. AI Categorizes the Dispute

The backend sends the case description to GPT-4, which classifies it across **20+ legal categories**:

> Copyright & IP, Banking, Child Custody, Inheritance, Property Division, Civil Contracts, Employment, Business, Tenancy, Real Estate, Personal Rights, Civil Law, Labour Law, Commercial Law, Health & Safety, Debt Collection, Damages, Consumer Protection, Mobbing, Traffic Accidents, and more.

Each category receives a binary relevance score (0 or 1), forming a **category vector** for the case.

### 3. Court Cost Estimation

Using official Polish fee schedules and real court statistics, the system calculates:
- **Court filing fees** — based on dispute value brackets (30 PLN – 20,000 PLN)
- **Attorney fees** — statutory rates based on dispute value
- **Expert witness costs** — average expert fee (~1,789 PLN) if applicable
- **Expected duration** — average case length in months from court statistical data

### 4. Mediator Ranking

Each mediator in the database has a profile with:
- Legal specializations (matching the 20+ category vector)
- Location and availability (in-person / online)
- User ratings and number of opinions
- Price per session

The scoring engine computes a **composite score** by comparing the case's category vector against each mediator's expertise vector, weighted by AI confidence and user ratings. The top matches are returned as ranked recommendations.

### 5. Results & Contact

The user sees the estimated cost/duration and a ranked list of mediator cards. Each card shows the mediator's specialization, rating, price, and location. A **"Schedule Appointment"** button opens a contact dialog.

---

## Getting Started

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with pnpm
- **OpenAI API access** (or compatible endpoint)

### Backend

```bash
cd Backend_correct
pip install flask flask-cors pandas openpyxl openai requests
python app.py                # starts on http://localhost:5000
```

### Frontend

```bash
cd arai-frontend
pnpm install
pnpm start                   # serves on http://localhost:4200
```

The frontend proxies API requests to the Flask backend via `proxy.conf.json`.

### WebSocket Server (optional)

```bash
cd simple-ws
pnpm install
node ws.js                   # runs on ws://localhost:8080
```

---

## API

### `POST /`

Accepts a case description and returns cost estimates + ranked mediators.

**Request:**
```json
{
  "request_type": "user_input",
  "request_data": {
    "generic_input": "pracodawca nie wypłacił mi wynagrodzenia...",
    "trial_value": 1000,
    "location": "Warszawa",
    "experts_called": false,
    "witnesses_called": false
  }
}
```

**Response:**
```json
{
  "response_type": "recommended_mediators",
  "response_data": {
    "first": {
      "cost_of_trial": 390,
      "time_of_trial": 8
    },
    "second": [
      {
        "name": "Emilia Borek",
        "specialization": "Prawo cywilne",
        "localization": "Warszawa",
        "street": "ul. Chmielna",
        "online": "Tak",
        "ai_rating": 0.62,
        "user_rating": 1,
        "number_of_opinions": 35,
        "price": 100
      }
    ]
  }
}
```

---

## Skills Demonstrated

- **Full-Stack Development** — Angular 17 SPA with TypeScript + Python Flask REST API
- **AI/LLM Integration** — GPT-4 prompt engineering for multi-label legal classification
- **Data Engineering** — pandas pipelines processing real court statistics from Excel sources
- **Algorithm Design** — Custom scoring engine combining AI classification vectors with mediator expertise profiles
- **UI/UX Design** — Multi-step wizard with Angular Material, responsive layout, dialog modals
- **API Design** — RESTful JSON API with structured request/response contracts and TypeScript interfaces
- **Rapid Prototyping** — Complete working product delivered in 48 hours with a 5-person team
