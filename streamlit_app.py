
import os
import sys
import streamlit as st
from dotenv import load_dotenv
from datetime import date
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from ai_travel_itinerary_planner.crew import AiTravelItineraryPlannerCrew

# ----------------------------------------------------------------
#  Load environment and ensure local module path is added
# ----------------------------------------------------------------
load_dotenv(override=True)
sys.path.append(os.getenv("PYTHONPATH", "."))

# ----------------------------------------------------------------
#  Streamlit Page Config
# ----------------------------------------------------------------
st.set_page_config(page_title="CrewAI Travel Itinerary Planner", layout="centered")
st.title("🧭 CrewAI-Powered Travel Itinerary Planner")
st.caption("Generate personalized travel itineraries using **CrewAI multi-agent system.**")
st.markdown("---")

# ----------------------------------------------------------------
#  User Input Form
# ----------------------------------------------------------------
with st.form("travel_form"):
    destination = st.text_input("📍 Destination (City, Country)", "Tokyo, Japan")
    start_date = st.date_input("🗓️ Start Date")
    end_date = st.date_input("🏁 End Date")
    travelers = st.number_input("👥 Number of Travelers", min_value=1, value=2)
    travel_style = st.selectbox("🎯 Travel Style", ["relaxation", "adventure", "culture"])
    budget_band = st.selectbox("💰 Budget Level", ["low", "medium", "high"])
    must_see = st.text_area("🏖️ Must-See Attractions (optional, comma-separated)")

    # Extra optional fields for future-proofing
    traveler_preferences = st.text_input(
        "💡 Traveler Preferences", "Flexible and open to local experiences"
    )
    preferred_transport = st.selectbox(
        "🚗 Preferred Transport Mode",
        ["public transport", "car rental", "walking", "mixed"],
        index=0,
    )

    # Auto-calculate trip duration
    trip_duration = (end_date - start_date).days
    if trip_duration <= 0:
        st.warning("⚠️ End date must be after start date.")
        trip_duration = 0
    else:
        st.info(f"📅 Trip Duration: **{trip_duration} days**")

    submit_btn = st.form_submit_button("🚀 Generate Itinerary")

# ----------------------------------------------------------------
#  Execution
# ----------------------------------------------------------------
if submit_btn:
    if trip_duration <= 0:
        st.stop()

    st.info("🧠 Running CrewAI agents... please wait ⏳")

    try:
        # Initialize Crew
        crew = AiTravelItineraryPlannerCrew().crew()

        # Clean & prepare input list
        must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []

        # ---------------- Inputs for CrewAI ----------------
        inputs = {
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "trip_duration": trip_duration,
            "travelers": travelers,
            "style": travel_style,
            "budget_range": budget_band,
            "must_sees": must_see_list,
            "traveler_preferences": traveler_preferences,
            "preferred_transport": preferred_transport,
        }

        # ---- Safe Defaults for all optional Crew template vars ----
        DEFAULTS = {
            "currency": "USD",
            "language": "English",
            "group_type": "friends",
            "pacing": "moderate",
            "weather_preference": "mild",
            "accommodation_type": "mid-range hotels",
        }
        for k, v in DEFAULTS.items():
            inputs.setdefault(k, v)

        # ----------------------------------------------------------------
        #  Run CrewAI Orchestration
        # ----------------------------------------------------------------
        result = crew.kickoff(inputs=inputs)

        # ----------------------------------------------------------------
        #  Display Results Beautifully
        # ----------------------------------------------------------------
        from fpdf import FPDF
        import textwrap

        st.success("✅ Itinerary generated successfully!")
        st.markdown("### 🗺️ Your Personalized Travel Itinerary")

        # Handle both JSON and raw Markdown-style output
        # if isinstance(result, dict) and "itinerary" in result:
        #     itinerary = result["itinerary"]
        #     total_cost = result.get("total_estimated_cost", "N/A")
        #     summary = result.get("summary", "No summary available.")
        # else:
        #     # Extract markdown-like text and display as formatted sections
        #     st.markdown(result.get("raw", "No structured data found."), unsafe_allow_html=True)
        #     itinerary, total_cost, summary = [], "N/A", "No structured itinerary available."
        
        if hasattr(result, "raw"):
            raw_output = result.raw
        else:
            raw_output = str(result)
            
        # Try parsing JSON safely if possible
        import json
        try:
            parsed = json.loads(raw_output)
            itinerary = parsed.get("itinerary", [])
            total_cost = parsed.get("total_estimated_cost", "N/A")
            summary = parsed.get("summary", "No summary available.")
        except Exception:
            itinerary, total_cost, summary = [], "N/A", "No structured itinerary available."
            st.markdown(raw_output, unsafe_allow_html=True)

        # -------------------------- Streamlit Display --------------------------
        if itinerary:
            for day in itinerary:
                with st.expander(f"🌞 Day {day.get('day', '?')} — {day.get('lodging', 'Details')}"):
                    st.markdown("#### 🏃 Activities")
                    for activity in day.get("activities", []):
                        st.markdown(f"- {activity}")
                    st.markdown("#### 🍽️ Meals")
                    for meal in day.get("meals", []):
                        st.markdown(f"- {meal}")
                    st.markdown(f"#### 🏨 Lodging: **{day.get('lodging', 'N/A')}**")
                    st.markdown(f"#### 💸 Estimated Cost: **{day.get('estimated_cost', 'N/A')}**")

        # st.markdown("---")
        # st.markdown("### 🧾 Trip Summary")
        # st.markdown(f"**Total Estimated Cost:** {total_cost}")
        # st.markdown(f"**Overview:** {summary}")

        # ----------------------------------------------------------------
        #  Generate Beautiful PDF
        # ----------------------------------------------------------------
        def create_pdf(destination, start_date, end_date, itinerary, total_cost, summary):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # --- Title ---
            pdf.set_fill_color(33, 150, 243)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 15, f"Travel Itinerary for {destination}", ln=True, align="C", fill=True)
            pdf.ln(5)

            # --- Dates & Trip Info ---
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, f"Dates: {start_date} to {end_date}")
            pdf.multi_cell(0, 10, f"Total Estimated Cost: {total_cost}")
            pdf.ln(5)

            # --- Day-by-Day ---
            for day in itinerary:
                pdf.set_fill_color(240, 240, 240)
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, f"Day {day.get('day', '?')}", ln=True, fill=True)
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 8, f"Lodging: {day.get('lodging', 'N/A')}")
                pdf.multi_cell(0, 8, f"Estimated Cost: {day.get('estimated_cost', 'N/A')}")
                pdf.ln(2)

                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Activities:", ln=True)
                pdf.set_font("Arial", "", 12)
                for activity in day.get("activities", []):
                    pdf.multi_cell(0, 8, f"• {activity}")
                pdf.ln(2)

                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, "Meals:", ln=True)
                pdf.set_font("Arial", "", 12)
                for meal in day.get("meals", []):
                    pdf.multi_cell(0, 8, f"• {meal}")
                pdf.ln(5)

            # --- Summary Section ---
            pdf.set_fill_color(33, 150, 243)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Trip Summary", ln=True, fill=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 12)
            for line in textwrap.wrap(summary, width=100):
                pdf.multi_cell(0, 8, line)
            pdf.ln(10)

            # Return bytes
            return bytes(pdf.output(dest="S").encode("latin-1"))

        # Only generate a PDF if itinerary exists
        # if itinerary:
        #     pdf_bytes = create_pdf(destination, start_date, end_date, itinerary, total_cost, summary)
        #     st.download_button(
        #         label="📄 Download Itinerary as PDF",
        #         data=pdf_bytes,
        #         file_name=f"itinerary_{destination.replace(' ', '_')}.pdf",
        #         mime="application/pdf",
        #     )

    except Exception as e:
        st.error(f"❌ Error running CrewAI automation: {e}")




