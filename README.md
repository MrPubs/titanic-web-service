# Titanic Web Service

Simple FastAPI service exposing Titanic passenger data via REST.  
Supports querying by passenger ID, selective field access, percentile-based fare histograms, and backend config flexibility (CSV / SQLite).

---

## Features

- `/passengers`: Full passenger list
- `/passenger/{id}`: Get all data for a specific passenger
- `/passenger/{id}/attributes?attrs=...`: Filtered attribute list for a specific passenger
- `/histogram/fare`: Percentile-based fare distribution
- Supports Swagger UI (`/docs`)
- Data source abstraction (CSV or SQLite)
- Async I/O throughout (non-blocking)
- Dockerized

---

## Quick Start

### 1. Clone the repo

```bash
git clone 
cd titanic-web-service
docker-compose up --build
