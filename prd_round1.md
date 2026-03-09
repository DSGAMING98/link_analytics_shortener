# Round 1 PRD - Link Analytics Shortener

## Overview
This project is a deployed Streamlit web application that converts long URLs into unique short URLs, redirects users to the original destination, tracks click counts, and stores analytics persistently using SQLite.

## Features Implemented
- Accepts long URLs
- Generates a unique short URL
- Redirects users from the short URL to the original URL
- Tracks click count for each short URL
- Displays original URL, short URL, and click count in a dashboard
- Persists data after refresh using SQLite
- Rejects empty and invalid URLs

## Tech Stack
- Python
- Streamlit
- SQLite
- Pandas

## Redirect Format
Short URLs are generated in this format:
`https://<deployed-app-url>/?code=<short_code>`

## Persistence
All links and their click analytics are stored in SQLite and remain available after refresh or app reload.

## Deployment
The application is deployed using Streamlit Community Cloud.