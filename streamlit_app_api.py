import streamlit as st
import requests
import pandas as pd
from datetime import date

# -------- Streamlit UI --------
st.title("⛳ Chronogolf Tee Time Finder (API Version)")

selected_date = st.date_input("Select Date", min_value=date.today())
holes = st.multiselect("Select Holes", ["9", "18"], default=["9", "18"])

search = st.button("Find Tee Times")

# Chronogolf Marketplace API Endpoint
base_url = "https://www.chronogolf.com/marketplace/v2/teetimes"

# Static course UUIDs for now
course_ids = [
    "026599af-6569-4b0f-aaf9-aefedc607e3c",  # South Mountain SLCO
    "79c03256-be52-4e3d-aba8-9c64df6e12b2",  # Riverbend SLCO
]

# Simulated headers (can be enhanced with real session handling if needed)
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Cookie": st.secrets["CHRONO_COOKIE"]
}

def fetch_tee_times(date_str, holes_selected):
    params = {
        "start_date": date_str,
        "course_ids": ",".join(course_ids),
        "holes": ",".join(holes_selected),
        "page": 1
    }

    r = requests.get(base_url, headers=headers, params=params)

    if r.status_code != 200:
        st.error(f"Error fetching tee times: {r.status_code}")
        return []

    data = r.json()
    return data.get("data", [])

if search:
    if not holes:
        st.warning("Please select at least one hole type.")
    else:
        st.info("Fetching tee times...")
        tee_times = fetch_tee_times(str(selected_date), holes)

        if tee_times:
            # Parse and display results
            parsed = []
            for tee in tee_times:
                parsed.append({
                    "Date": tee.get("date"),
                    "Time": tee.get("time"),
                    "Course": tee.get("course", {}).get("name"),
                    "Holes": tee.get("holes"),
                    "Price": tee.get("green_fee", {}).get("price")
                })

            df = pd.DataFrame(parsed)
            st.success(f"Found {len(df)} tee times.")
            st.dataframe(df)
        else:
            st.info("No tee times found.")
