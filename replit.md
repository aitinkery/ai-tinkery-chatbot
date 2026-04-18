# AI Tinkery Chatbot

## Overview
An interactive chatbot for the Stanford Graduate School of Education's AI Tinkery space. It helps users explore AI learning activities, recommends hands-on tasks, and guides educators on launching their own AI Tinkery community.

## Architecture
- **Frontend**: Single-page HTML app (`index.html`) using vanilla JavaScript, HTML5, CSS3
- **Backend**: Python Flask server (`server.py`) that:
  - Serves `index.html` and static assets
  - Proxies Claude API requests to Google Apps Script backend
  - Optionally syncs activity images from Airtable (requires `AIRTABLE_PAT` env var)
- **AI**: Anthropic Claude via Google Apps Script proxy (`claude-backend.gs`)

## Running Locally
The Flask server starts automatically via the "Start application" workflow on port 5000.

## Environment Variables
- `AIRTABLE_PAT`: Airtable Personal Access Token (optional) — used to refresh activity images from Airtable

## Key Files
- `index.html` — Main chatbot app (activities data, UI, state management)
- `server.py` — Flask server (serves files, proxies Claude API, Airtable sync)
- `activity-images/` — Local JPG images for 38 activities
- `images/` — Branding assets (Stanford logo, robot logo, icons)
- `claude-backend.gs` — Google Apps Script backend for Claude API
- `manifest.json` / `sw.js` — PWA support files

## Deployment
Configured for autoscale deployment running `python server.py`.
