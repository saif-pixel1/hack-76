✈️ Autonomous Travel Concierge

A Streamlit-based AI chatbot that autonomously searches and books travel arrangements based on natural language conversation. The bot simulates a full travel agency workflow—understanding user intent, querying flight/hotel databases, and executing bookings.

⚠️ Disclaimer: This is a Proof of Concept (PoC). The "booking" and "search" functions currently use mock data. See the "Production Setup" section to connect real APIs (Amadeus, Skyscanner, Booking.com).

🚀 Features
Conversational Interface: Natural chat UI powered by Streamlit.
Stateful Logic: Remembers conversation history and user preferences (Destination, Date).
Autonomous Action: Automatically searches APIs when parameters are met, rather than just recommending.
Mock API Layer: Ready-to-test simulation of booking engines.
Data Visualization: Displays flight and hotel options in interactive tables.
🛠️ Prerequisites
Python 3.8+ installed.
pip package manager.
📦 Installation
Clone the Repository (or create the file): If you have the code in a file named app.py:

Install Dependencies: Open your terminal/command prompt and run:

bash

Copy code
pip install streamlit pandas requests
▶️ How to Run
Navigate to the folder containing app.py.

Run the application:

bash

Copy code
streamlit run app.py
A local web server will start (usually at http://localhost:8501), opening the chatbot in your browser.

📖 User Guide (How to Talk to the Bot)
The bot follows a specific conversation flow:

Start: The bot asks for your destination.
You: "I want to go to Tokyo"
Date: The bot asks for the travel date.
You: "2024-12-25"
Search: The bot autonomously searches its database and tells you it found options.
You: "Show me flights"
Select: The bot displays a table of flights.
You: "Book the first one"
Booking: The bot confirms the booking with a simulated confirmation code.
🏗️ Architecture
1. State Machine (process_user_input)
The core logic is a finite state machine stored in st.session_state. It ensures the bot only asks for relevant information in the correct order (Destination -> Date -> Booking).

2. Mock API Layer
Located in the top functions (search_flights_api, book_flight_api). These return fake data to demonstrate functionality without needing external API keys immediately.

3. Session Storage
Uses st.session_state to persist:

Chat History
Current Step (0–5)
User Preferences
🔌 Moving to Production (Real APIs)
To make this real, you need to replace the Mock API functions with real HTTP requests.

1. Flight API (Amadeus)
Amadeus for Developers offers a free tier.

Replace search_flights_api:
