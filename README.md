# ARAI — Legal Mediation Assistant

A web application built in **48 hours** at a legal-tech hackathon that helps users resolve disputes through mediation instead of court.

Describe your case in plain language, and the app will:

1. **Categorise** the dispute (civil, labour, commercial, etc.)
2. **Estimate** the likely court cost and duration based on real court statistics
3. **Score and recommend** mediators suited to the case

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Angular 17, Angular Material, SCSS |
| Backend | Python, Flask, pandas |
| AI | OpenAI API (case categorisation & mediator scoring) |
| Real-time | WebSocket relay (Node.js) |

## Project Structure

```
arai-frontend/    Angular SPA — form wizard, results display, Material UI
Backend_correct/  Flask API  — categorisation, cost estimation, mediator scoring
simple-ws/        Lightweight WebSocket relay server (Node.js)
statystyki/       Court statistics data pipeline (pandas + Excel)
franek/           ML experiments — case scoring prototypes
```

## Quick Start

### Backend

```bash
cd Backend_correct
pip install flask flask-cors pandas openpyxl openai
python app.py
```

### Frontend

```bash
cd arai-frontend
pnpm install
pnpm start          # serves on http://localhost:4200
```

The frontend proxies API requests to the Flask backend via `proxy.conf.json`.

## Team

Built by 5 contributors during the hackathon:

- Krzysztof Rudnicki — frontend & integration
- Franciszek Michalowski — ML & scoring
- Jakub Jarzembowski — backend
- Mateusz Szpyruk — data & statistics
- + 1 contributor
