# LOOPBITE

LoopBite is a food rescue platform prototype that helps merchants publish discounted surplus food and helps nearby users discover affordable items before they go to waste. The current repository contains a `FastAPI` backend, a `Streamlit` frontend, and `Supabase` as the data layer.

This project is built around a simple idea: food that is still safe and usable should not become waste just because it is close to its expiry window or has lower commercial value.

## Problem Statement

In urban areas, many convenience stores, mini markets, and small food sellers still have usable products at the end of the day, but these items are often discarded because demand drops too quickly, shelf life becomes short, or manual discounting is inefficient. At the same time, many students, low-income workers, and nearby consumers are looking for more affordable food options.

LoopBite addresses this mismatch by creating a lightweight rescue-food flow:

- Merchants can post food listings with price, quantity, and expiry timing.
- Users can search nearby stores and find matching food quickly.
- The system helps reduce waste while creating a low-cost purchase channel.


## What Problem Does LOOPBITE Solve?

LoopBite solves three connected problems:

1. Food waste from unsold inventory that is still safe to consume.
2. Lack of visibility between surplus food supply and nearby demand.
3. Manual coordination between merchants and buyers that is too slow for time-sensitive rescue items.

Instead of relying on ad hoc markdowns or offline clearance, LoopBite makes the inventory visible in one place and searchable by keyword and distance.

## Pain Points

- Merchants often do not have a fast way to publish surplus items before they expire.
- Buyers do not know which nearby stores still have discounted food available.
- Inventory changes quickly, so timing matters more than in normal e-commerce.
- Data about merchants, locations, and rescue items is fragmented and not always readily available.
- Small teams need a product that is fast to build, easy to demo, and still realistic enough to validate the idea.

## Current Solution in This Repo

The current prototype focuses on the merchant and search flow:

- Merchant dashboard for posting and reviewing food listings.
- Backend APIs for foods, merchants, and nearby search.
- Nearby search based on latitude/longitude and keyword matching.
- Supabase-backed storage for merchants and food data.
- Lightweight UI for demo and hackathon iteration.


## Tech Stack

- Frontend: `Streamlit`
- Backend: `FastAPI`, `Uvicorn`, `Pydantic`
- Database / BaaS: `Supabase`
- Environment management: `python-dotenv`
- Language: `Python`
- Search / geo logic: custom keyword normalization and Haversine distance calculation

## Project Structure

```text
backend/
  app.py
  main.py
  database/
  models/
  routers/
frontend/
  app.py
docs/
  architecture.md
  database.md
  use-cases.md
```

## Quick Start

### 1. Install dependencies

Backend:

```bash
cd backend
pip install -r requirements.txt
```

Frontend:

```bash
cd frontend
pip install -r requirements.txt
```

### 2. Configure environment

Add your Supabase credentials in `backend/.env`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Optional frontend environment:

```env
BACKEND_URL=http://127.0.0.1:8000
DEFAULT_USER_LAT=10.7769
DEFAULT_USER_LNG=106.7009
```

### 3. Run the backend

```bash
cd backend
python main.py
```

### 4. Run the frontend

```bash
cd frontend
streamlit run app.py
```

## Demo Scope

This prototype is mainly intended for MVP validation and hackathon-style demonstration. It focuses on:

- merchant listing creation
- nearby food discovery
- inventory visibility
- rescue-food workflow validation

It is not yet a production-ready marketplace and does not include full payment, delivery, or advanced user authentication flows.

## Technical Issues / Challenges

During development, our team faced several technical challenges:

- Limited data sources: The available dataset was not sufficient, so we needed to search for additional data and collect data from external APIs.
- Data crawling and API integration: Some required data had to be retrieved by calling or crawling external APIs, which required extra processing and cleaning before being stored in the database.
- New tech stack: Some technologies in our stack were new to the team, so we had to learn and implement them at the same time.
- Backend and frontend integration: Connecting the backend APIs with the frontend interface was challenging due to the limited development time.
- Geolocation and nearby search logic: Matching user intent with nearby merchants required both text normalization and distance calculation.
- Data consistency for live listings: Rescue-food data changes quickly, so quantity, status, and expiry handling had to stay simple but still usable for the prototype.

## Closing Note

LoopBite is a small but practical step toward reducing food waste with technology. The goal is not only to build an app, but to test whether a simple digital workflow can connect surplus food with nearby demand in time to make a real difference.

If this prototype proves useful, it can grow into a broader platform for low-waste retail, community access, and more sustainable consumption habits.
