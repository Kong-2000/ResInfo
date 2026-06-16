# ResInfo – Sweden Travel Information

A reverse engineering project built as part of an APL placement assignment. The original application was a Python terminal client for the Swedavia FlightInfo API, showing live flight arrivals and departures at Swedish airports. This project recreates the same concept using the ResRobot API for all public transport in Sweden.

---

## What It Does

ResInfo lets you look up real-time departures and arrivals for any public transport stop in Sweden. It covers trains, metro, trams, buses, commuter rail, and ferries.

Two versions were built:

- `resinfo.py` — A Python terminal app
- `resinfo.html` — A web app that runs in the browser

---

## Phase 1: Research

The original Swedavia app was studied by looking at screenshots and video recordings. The key patterns observed were:

- A menu loop that kept running until the user typed `q`
- Input validation loops that kept asking until valid input was given
- API calls with pagination using a `continuationToken`
- Structured output printed to the terminal

**Questions asked during research:**
- What kind of data does the app work with?
- What inputs does the user give?
- What logic runs between input and output?
- What API endpoints does it use?

**Tools chosen:**
- Python 3 for the terminal app
- HTML, CSS, and JavaScript for the web app
- ResRobot API v2.1 from Trafiklab for live transport data

---

## Phase 2: Implementation

**Terminal app (resinfo.py)**

Built first to mirror the structure of the original Swedavia app as closely as possible.

Functions created:
- `main()` — Menu loop with `while True` and `break` on quit
- `_find_stop(name)` — Searches for a station by name via the API
- `_choose_station()` — Validates user input in a loop until a valid station is chosen
- `_transport_type(entry)` — Detects transport type from API product data
- `get_departures()` — Fetches and prints departures
- `get_arrivals()` — Fetches and prints arrivals

**Web app (resinfo.html)**

Built as a single HTML file with embedded CSS and JavaScript. Uses the same ResRobot API directly from the browser via `fetch()`.

Features added:
- Dark and light mode toggle with localStorage persistence
- Color-coded transport type badges (Metro, Bus, Train, etc.)
- Stockholm line colors (blue for T10/T11, red for T13/T14, green for T17/T18/T19, etc.)
- Real-time delay detection and display
- Full-width results table
- Station picker when multiple results are found

---

## Phase 3: Finishing

- Tested with multiple stations including Stockholm C, T-Centralen, and Märsta
- Fixed transport type mismatches (e.g. Airport Transfer showing as Tram)
- Fixed Swedish character issues in the browser by using lowercase matching
- Translated all Swedish terms in line names to English
- Removed debug console logs before final version

---

## Phase 4: Problems and Solutions

**Problem:** The API returned 403 Forbidden when called from the development server.
**Solution:** The API key needed to be activated via "Hämta nyckel" on Trafiklab. Once activated, calls worked correctly.

**Problem:** Opening the HTML file directly from disk blocked API calls.
**Solution:** Used VS Code Live Server extension to serve the file over `http://localhost`, which browsers allow.

**Problem:** Swedish characters like `å`, `ä`, `ö` did not match reliably when using `.toUpperCase()` in the browser.
**Solution:** Switched all string matching to lowercase using `.toLowerCase()`.

**Problem:** Transport types were incorrectly detected. Airport Transfer Bus showed as Tram, InterCity showed as Commuter.
**Solution:** Added entry name checking before product type checking, so the line name overrides the product classification when it clearly indicates a different type.

**Problem:** Line colors only worked for Metro, not for trams or commuter trains.
**Solution:** Used the browser console to log raw API names and discovered the exact format (e.g. `Länstrafik - Spårväg 7` not `Spårvagn`). Updated matching logic accordingly.

---

## Conclusion

This project showed how to reverse engineer an application by studying its outputs and working backwards to understand the inputs and logic. The result is a working terminal app and web app that follow the same patterns as the original Swedavia client, applied to a different API and domain.

Key things learned:
- How to read and understand someone else's code structure
- How to work with real REST APIs and handle pagination
- How to debug browser issues using the developer console
- How to translate a terminal app into a web interface

What could be improved:
- Add a search history feature
- Show a map of the selected station
- Add auto-refresh so the board updates every minute

---

## How to Run

**Terminal app:**
```
python resinfo.py
```

**Web app:**
Open `resinfo.html` with VS Code Live Server or any local web server.

---

## API

This project uses the [ResRobot v2.1 API](https://www.trafiklab.se/api/our-apis/resrobot-v21/) from Trafiklab.

Endpoints used:
- `location.name` — Search for a stop by name
- `departureBoard` — Get departures from a stop
- `arrivalBoard` — Get arrivals to a stop


