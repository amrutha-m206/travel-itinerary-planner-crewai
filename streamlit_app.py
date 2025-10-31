import os
import sys
import streamlit as st
from dotenv import load_dotenv
from datetime import date
from fpdf import FPDF
import markdown
from bs4 import BeautifulSoup
import urllib.request
import json

# ----------------------------------------------------------------
#  Path Setup and Imports
# ----------------------------------------------------------------
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
        st.success("✅ Itinerary generated successfully!")
        st.markdown("### 🗺️ Your Personalized Travel Itinerary")

        # Handle both JSON and raw Markdown-style output
        if hasattr(result, "raw"):
            raw_output = result.raw
        else:
            raw_output = str(result)

        # Try parsing JSON safely if possible
        try:
            parsed = json.loads(raw_output)
            itinerary = parsed.get("itinerary", [])
            total_cost = parsed.get("total_estimated_cost", "N/A")
            summary = parsed.get("summary", "No summary available.")
        except Exception:
            itinerary, total_cost, summary = [], "N/A", "No structured itinerary available."
            markdown_output = raw_output
        else:
            # Construct markdown view from JSON if structured
            markdown_output = f"### {destination} Itinerary\n\n"
            for day in itinerary:
                markdown_output += f"**Day {day.get('day','?')} — {day.get('lodging','Details')}**\n\n"
                markdown_output += "**Activities:**\n" + "\n".join(f"- {a}" for a in day.get("activities", [])) + "\n\n"
                markdown_output += "**Meals:**\n" + "\n".join(f"- {m}" for m in day.get("meals", [])) + "\n\n"
                markdown_output += f"**Estimated Cost:** {day.get('estimated_cost','N/A')}\n\n---\n"
            markdown_output += f"\n### Summary\n{summary}\n\n**Total Estimated Cost:** {total_cost}"

        st.session_state["markdown_output"] = markdown_output

    except Exception as e:
        st.error(f"❌ Error running CrewAI automation: {e}")

# ----------------------------------------------------------------
#  Display Section (Independent of Form Submit)
# ----------------------------------------------------------------
if "markdown_output" in st.session_state:
    markdown_output = st.session_state["markdown_output"]
    st.markdown(markdown_output)

    # ----------------------------------------------------------------
    #  Unicode-safe PDF Generation with Verified Font
    # ----------------------------------------------------------------
    if st.button("📄 Download Itinerary as PDF"):
        html = markdown.markdown(markdown_output)
        soup = BeautifulSoup(html, "html.parser")

        # Ensure fonts directory
        font_dir = "fonts"
        os.makedirs(font_dir, exist_ok=True)
        font_path = os.path.join(font_dir, "DejaVuSans.ttf")

        def ensure_font():
            """Download and validate the DejaVuSans.ttf font for Unicode support."""
            if not os.path.exists(font_path):
                st.warning("⚠️ Missing 'DejaVuSans.ttf'. Downloading font for Unicode PDF support...")
                try:
                    url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf"
                    urllib.request.urlretrieve(url, font_path)
                    if not os.path.getsize(font_path) > 100000:
                        raise ValueError("Downloaded file too small to be a valid TTF.")
                    st.success("✅ Font downloaded successfully.")
                except Exception as e:
                    st.error(f"❌ Font download failed: {e}")
                    return None
            return font_path

        font_file = ensure_font()

        class PDF(FPDF):
            def __init__(self):
                super().__init__()
                self.set_auto_page_break(auto=True, margin=15)

        pdf = PDF()
        pdf.add_page()

        if font_file:
            try:
                pdf.add_font("DejaVu", "", font_file, uni=True)
                pdf.set_font("DejaVu", "", 12)
            except Exception as e:
                st.error(f"⚠️ Failed to load DejaVu font: {e}. Falling back to Helvetica.")
                pdf.set_font("Helvetica", "", 12)
        else:
            pdf.set_font("Helvetica", "", 12)

        # Write PDF content
        for elem in soup.find_all(["h1", "h2", "h3", "p", "ul", "strong", "b"]):
            if elem.name in ["h1", "h2", "h3"]:
                pdf.set_font("DejaVu", "B", 14)
                pdf.multi_cell(0, 10, elem.get_text().upper())
                pdf.ln(2)
            elif elem.name == "p":
                pdf.set_font("DejaVu", "", 12)
                pdf.multi_cell(0, 8, elem.get_text())
                pdf.ln(2)
            elif elem.name == "ul":
                pdf.set_font("DejaVu", "", 12)
                for li in elem.find_all("li"):
                    pdf.multi_cell(0, 8, f"• {li.get_text()}")
                pdf.ln(2)
            elif elem.name in ["strong", "b"]:
                pdf.set_font("DejaVu", "B", 12)
                pdf.multi_cell(0, 8, elem.get_text())

        # Output PDF bytes safely (Unicode friendly)
        pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")

        st.download_button(
            label="⬇️ Save PDF",
            data=pdf_bytes,
            file_name=f"itinerary_{destination.replace(' ', '_')}.pdf",
            mime="application/pdf",
        )
