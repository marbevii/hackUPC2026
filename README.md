# Travel AI  
### HackUPC 2026 · 10th Anniversary Edition  
### Challenge by Skyscanner: *Be the Future of Travel*

---

## Overview

Travel AI is an intelligent trip discovery platform built during **HackUPC 2026** for the **Skyscanner Challenge**.

The challenge invited participants to rethink how people discover and book travel in a world full of endless options, growing complexity, and decision fatigue.

Our solution uses **Artificial Intelligence + Real Flight Data** to understand what travellers truly want, then transforms vague intentions into clear, personalized and bookable travel options.

Instead of forcing users to manually compare dozens of tabs, websites and filters, Travel AI creates a smarter and more intuitive travel planning experience.

---

# The Challenge

> There have never been more ways to travel.  
> New routes, hidden gems, seasonal escapes… the list keeps growing.

But more choice often creates more confusion:

- Where should I go?
- What fits my budget?
- Which option is actually best for me?
- What if I do not know where I want to go yet?

Skyscanner asked us to create a next-generation AI-powered travel experience that:

- Understands traveller intent  
- Reduces complexity  
- Gives relevant recommendations  
- Preserves user freedom and control  

---

# Our Solution

## Travel AI reimagines travel search with 3 intelligent modes:

---

## 1. Standard Mode

Users simply describe the trip they want in natural language.

Examples:

- “I want a 5-day trip from Barcelona with nature and good food.”
- “Cheap city break in March with culture.”
- “Warm destination under €400.”

Our AI interprets the request and finds matching destinations with real flight options.

---

## 2. Mood Mode

Users upload inspirational images.

Examples:

- Beaches  
- Cafés  
- Mountains  
- Night city lights  
- Tropical places  

Travel AI analyses the visual mood and suggests destinations that match the style and feeling the user wants.

This allows people to search by emotion and aesthetics, not only keywords.

---

## 3. Budget Mode

Users specify a budget.

Example:

> “I have €700 total for flights, hotel and food.”

Travel AI builds complete travel packages including:

- Flights  
- Accommodation  
- Food options  
- Extra activities  

Each destination dynamically calculates totals so travellers stay within budget.

---

# Key Features

## Real Flight Search

Integrated with **Skyscanner APIs** for live or dynamic flight options.

## AI Intent Understanding

Uses language models to transform human prompts into structured travel requests.

## Smart Bundles

Each destination includes:

- 3 flight options  
- 3 accommodation options  
- 3 food options  
- 3 extra experiences  

## Interactive Basket

Users can add selected combinations to their basket and compare multiple trips instantly.

## Session Persistence

Selections remain saved while browsing during the session.

## Traveller Control First

AI recommends — users decide.

---

# Why This Matters

Current travel platforms are excellent for searching known destinations.

But many travellers begin with:

- A feeling  
- A budget  
- A vibe  
- A need for escape  

Travel AI bridges that gap.

Instead of asking:

> “Where do you want to go?”

We ask:

> “What kind of trip do you want?”

---

# Tech Stack

## Backend

- Python  
- Flask  

## APIs

- Skyscanner APIs  
- Google Generative AI / Gemma Models  

## Frontend

- HTML  
- CSS  
- JavaScript  

## Data Handling

- Session Storage  
- Dynamic pricing logic  
- Real-time UI updates  

---

# Installation

## 1. Clone the repository
```bash
git clone <your-repository-url>
cd travel-ai

## 2. Install dependencies
pip install -r requirements.txt

## 3. Create a .env file
GEMINI_API_KEY=your_api_key
SKYSCANNER_API_KEY=your_api_key

## 4. Run the project
python app.py

## 5. Open in browser
http://127.0.0.1:5050