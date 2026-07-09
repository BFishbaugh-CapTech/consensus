# Consensus Frontend

React frontend for the Consensus AI News Analysis platform.

---

## Technologies

- React
- Vite
- JavaScript
- CSS

---

## Running

Install dependencies

```bash
npm install
```

Start the development server

```bash
npm run dev
```

The application will be available at

```
http://localhost:5173
```

---

## Backend

The frontend expects the FastAPI backend to be running on

```
http://localhost:8000
```

The backend exposes the following endpoints:

- GET `/analysis`
- GET `/articles`
- POST `/pipeline/run`

---

## Project Structure

```
src/
│
├── components/
│   ├── AnalysisCard.jsx
│   ├── Header.jsx
│   ├── LoadingSpinner.jsx
│   └── Stats.jsx
│
├── services/
│   └── api.js
│
├── styles/
│   ├── App.css
│   └── Card.css
│
├── App.jsx
├── main.jsx
└── index.css
```

---

## Purpose

This frontend provides a simple interface for displaying AI-generated news analyses produced by the Consensus backend.
