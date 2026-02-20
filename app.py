import streamlit as st
import pandas as pd
import datetime
import time
import random

# ==========================================
# 1. CONFIGURATION & MOCK API LAYER
# ==========================================

st.set_page_config(page_title="Autonomous Travel Concierge", page_icon="✈️")

# --- SIDEBAR: API KEYS ---
st.sidebar.title("🔑 API Configuration")
st.sidebar.info("In a real production app, you would enter keys for Amadeus, Skyscanner, or Booking.com here.")

api_mode = st.sidebar.radio("Simulation Mode", ["Mock (Demo)", "Real API"])

# --- MOCK API FUNCTIONS (Replace these with real requests) ---

def search_flights_api(destination, date):
    """
    SIMULATION: In a real app, use requests.get to Amadeus/Google Flights API
    """
    # Simulating network delay
    time.sleep(1) 
    return pd.DataFrame({
        "Airline": ["Air France", "Delta", "British Airways", "Emirates"],
        "Price": [random.randint(400, 800), random.randint(450, 900), random.randint(500, 1000), random.randint(600, 1200)],
        "Duration": ["7h 20m", "8h 10m", "6h 45m", "10h 30m"],
        "Type": ["Direct", "1 Stop", "Direct", "2 Stops"]
    })

def book_flight_api(flight_index, flight_data):
    """
    SIMULATION: Autonomous booking logic
    """
    time.sleep(1.5)
    # In reality, this sends a POST request to the payment gateway
    confirmation_number = f"CONF-{random.randint(10000, 99999)}"
    return confirmation_number

def search_hotels_api(destination):
    """
    SIMULATION: In a real app, use Booking.com API or RapidAPI
    """
    time.sleep(1)
    return pd.DataFrame({
        "Hotel Name": [f"{destination} Grand Hotel", f"{destination} Inn", f"{destination} Suites", "Airbnb Private Villa"],
        "Price/Night": [random.randint(150, 300), random.randint(80, 150), random.randint(200, 400), random.randint(100, 250)],
        "Rating": [4.8, 4.2, 4.5, 4.9],
        "Location": ["City Center", "Airport Rd", "Old Town", "Suburbs"]
    })

# ==========================================
# 2. STATE MANAGEMENT
# ==========================================

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'step' not in st.session_state:
    # Steps: 0=Start, 1=Get Dest, 2=Get Date, 3=Search, 4=Select, 5=Booked
    st.session_state['step'] = 0 

if 'prefs' not in st.session_state:
    st.session_state['prefs'] = {
        "destination": None,
        "date": None,
        "budget": None,
        "flights": None,
        "hotels": None
    }

# ==========================================
# 3. CHATBOT LOGIC
# ==========================================

def add_message(role, content):
    st.session_state['history'].append({"role": role, "content": content})

def process_user_input(user_input):
    step = st.session_state['step']
    prefs = st.session_state['prefs']

    # --- STATE 0/1: DESTINATION ---
    if step == 0 or step == 1:
        prefs['destination'] = user_input
        st.session_state['step'] = 2
        return f"Great choice! When do you want to fly to {user_input}? (Format: YYYY-MM-DD)"

    # --- STATE 2: DATE ---
    elif step == 2:
        try:
            # Simple date validation
            datetime.datetime.strptime(user_input, '%Y-%m-%d')
            prefs['date'] = user_input
            
            # AUTONOMOUS ACTION: Searching APIs
            with st.spinner('Searching global databases for best flights and hotels...'):
                prefs['flights'] = search_flights_api(prefs['destination'], prefs['date'])
                prefs['hotels'] = search_hotels_api(prefs['destination'])
            
            st.session_state['step'] = 3
            return "I found some options. Do you want to see Flights or Hotels first?"
        except ValueError:
            return "Please use the format YYYY-MM-DD (e.g., 2024-06-15)."

    # --- STATE 3: PRESENTING OPTIONS ---
    elif step == 3:
        user_input_lower = user_input.lower()
        if "flight" in user_input_lower:
            st.session_state['step'] = 4
            return "display_flights"
        elif "hotel" in user_input_lower:
            st.session_state['step'] = 4
            return "display_hotels"
        else:
            return "Just say 'Flights' or 'Hotels' to see options."

    # --- STATE 4: SELECTION & BOOKING ---
    elif step == 4:
        # Simple selection logic (choosing first option for demo)
        # In a real app, we would parse "I want option 2"
        
        # AUTONOMOUS BOOKING EXECUTION
        with st.spinner(f"Authorizing payment and booking your flight to {prefs['destination']}..."):
            conf_num = book_flight_api(1, prefs['flights'])
        
        st.session_state['step'] = 5
        return f"✅ **Booking Confirmed!** \n\nYour flight is booked. Confirmation Code: **{conf_num}**.\n\nAnything else I can help you with?"

    # --- STATE 5: RESET ---
    elif step == 5:
        if "yes" in user_input_lower or "another" in user_input_lower:
            st.session_state['step'] = 0
            st.session_state['prefs'] = {"destination": None, "date": None, "budget": None, "flights": None, "hotels": None}
            return "Where would you like to go next?"
        else:
            return "Have a great trip!"

    return "I'm not sure how to handle that. Let's start over. Where do you want to go?"

# ==========================================
# 4. UI LAYOUT
# ==========================================

st.title("✈️ Autonomous Travel Concierge")
st.markdown("Tell me where you want to go, and I will search and book it for you autonomously.")

# Display Chat History
for msg in st.session_state['history']:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle specific display logic (Dataframes) separately from history
# This is a trick to display dataframes in the chat stream without adding them to text history
if st.session_state['step'] == 4:
    prefs = st.session_state['prefs']
    
    # Determine what to show based on previous user intent (simplified for demo)
    # Ideally, we store 'last_intent' in session state
    with st.chat_message("assistant"):
        st.subheader("Available Flights")
        st.dataframe(prefs['flights'], hide_index=True)
        st.info("Say 'Book the first one' or similar to confirm.")

# User Input
if prompt := st.chat_input("Type your message..."):
    add_message("user", prompt)
    
    # Get Bot Response
    response = process_user_input(prompt)
    
    # Handle special display returns
    if response == "display_flights":
        with st.chat_message("assistant"):
            st.subheader(f"✈️ Flights to {st.session_state['prefs']['destination']}")
            st.dataframe(st.session_state['prefs']['flights'], hide_index=True)
            st.write("Which one would you like to book?")
    elif response == "display_hotels":
        with st.chat_message("assistant"):
            st.subheader(f"🏨 Hotels in {st.session_state['prefs']['destination']}")
            st.dataframe(st.session_state['prefs']['hotels'], hide_index=True)
            st.write("Which one would you like to book?")
    else:
        add_message("assistant", response)
