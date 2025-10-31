# import os
# import time
# import json
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # --- Load .env and configure Gemini ---
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)

# # --- Initialize model ---
# model = genai.GenerativeModel("gemini-2.5-flash")

# # ---------------- STREAMLIT UI ----------------
# st.set_page_config(page_title="AI Travel Itinerary Planner", layout="centered")
# st.title("✈️ AI Travel Itinerary Planner")
# st.markdown("Plan your perfect trip powered by **Google Gemini** (CrewAI-style orchestration simulation).")

# with st.form("itinerary_form"):
#     destination = st.text_input("Destination (city, country)", "Tokyo, Japan")
#     start_date = st.date_input("Start Date")
#     end_date = st.date_input("End Date")
#     travelers = st.number_input("Number of Travelers", min_value=1, value=1)
#     style = st.selectbox("Travel Style", ["relaxation", "adventure", "culture"])
#     budget = st.selectbox("Budget Level", ["low", "medium", "high"])
#     must_see = st.text_area("Must-See Attractions (optional, comma-separated)")
#     submit_btn = st.form_submit_button("Generate Itinerary")

# if submit_btn:
#     must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []
#     st.info("Generating itinerary using Gemini... please wait.")
    
#     # --- Prompt construction ---
#     prompt = f"""
#     You are a multi-agent travel planner system.
#     Generate a complete {style}-style travel itinerary for {travelers} travelers visiting {destination}
#     from {start_date} to {end_date}, with a {budget} budget.
#     Include daily schedules, places to visit, transportation, and lodging suggestions.
#     Also provide estimated costs per day.
#     Must-see attractions: {', '.join(must_see_list) if must_see_list else 'none'}.
    
#     Respond in structured JSON:
#     {{
#       "itinerary": [
#         {{
#           "day": 1,
#           "activities": ["..."],
#           "meals": ["..."],
#           "lodging": "...",
#           "estimated_cost": "..."
#         }}
#       ],
#       "total_estimated_cost": "...",
#       "summary": "..."
#     }}
#     """

#     try:
#         response = model.generate_content(prompt)
#         result_text = response.text.strip()

#         # Try parsing JSON safely
#         try:
#             result = json.loads(result_text)
#         except json.JSONDecodeError:
#             # Fallback: extract JSON manually if mixed text
#             start_idx = result_text.find("{")
#             end_idx = result_text.rfind("}") + 1
#             json_str = result_text[start_idx:end_idx]
#             result = json.loads(json_str)

#         # --- Display results ---
#         st.success("✅ Itinerary Generated Successfully!")
#         st.subheader("Final Itinerary")
#         st.json(result)

#         # Download options
#         st.download_button(
#             label="Download JSON",
#             data=json.dumps(result, indent=2),
#             file_name="itinerary.json",
#             mime="application/json"
#         )

#         # Optional PDF export
#         try:
#             from fpdf import FPDF

#             def itinerary_to_pdf_bytes(destination, start, end, data):
#                 pdf = FPDF()
#                 pdf.add_page()
#                 pdf.set_font("Arial", "B", 16)
#                 pdf.cell(0, 10, f"Travel Itinerary for {destination}", ln=True)
#                 pdf.set_font("Arial", size=12)
#                 pdf.cell(0, 10, f"Dates: {start} to {end}", ln=True)
#                 pdf.cell(0, 10, "", ln=True)
#                 for day in data.get("itinerary", []):
#                     pdf.cell(0, 10, f"Day {day['day']}", ln=True)
#                     pdf.multi_cell(0, 10, f"Activities: {', '.join(day['activities'])}")
#                     pdf.multi_cell(0, 10, f"Lodging: {day['lodging']}")
#                     pdf.multi_cell(0, 10, f"Cost: {day['estimated_cost']}")
#                     pdf.cell(0, 10, "", ln=True)
#                 pdf.cell(0, 10, f"Total Estimated Cost: {data.get('total_estimated_cost')}", ln=True)
#                 pdf.cell(0, 10, f"Summary: {data.get('summary')}", ln=True)
#                 return bytes(pdf.output(dest="S").encode("latin-1"))

#             pdf_bytes = itinerary_to_pdf_bytes(destination, start_date, end_date, result)
#             st.download_button(
#                 label="Download PDF",
#                 data=pdf_bytes,
#                 file_name="itinerary.pdf",
#                 mime="application/pdf"
#             )
#         except Exception as e:
#             st.warning(f"PDF export unavailable: {e}")

#     except Exception as e:
#         st.error(f"Error generating itinerary: {e}")


## Version - 2

# import os
# import json
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai
# from fpdf import FPDF

# # --- Load .env and configure Gemini ---
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)

# # --- Initialize model ---
# model = genai.GenerativeModel("gemini-2.0-flash")  # or gemini-2.5-flash if supported

# # ---------------- STREAMLIT UI ----------------
# st.set_page_config(page_title="AI Travel Itinerary Planner", layout="centered")
# st.title("🌍 AI Travel Itinerary Planner")
# st.caption("Your personalized trip planner powered by **Google Gemini** 🧠")

# st.markdown("---")

# # ---------------- INPUT FORM ----------------
# with st.form("itinerary_form"):
#     destination = st.text_input("📍 Destination (city, country)", "Tokyo, Japan")
#     start_date = st.date_input("🗓️ Start Date")
#     end_date = st.date_input("🏁 End Date")
#     travelers = st.number_input("👨‍👩‍👧‍👦 Number of Travelers", min_value=1, value=1)
#     style = st.selectbox("🎯 Travel Style", ["relaxation", "adventure", "culture"])
#     budget = st.selectbox("💰 Budget Level", ["low", "medium", "high"])
#     must_see = st.text_area("🏖️ Must-See Attractions (optional, comma-separated)")
#     submit_btn = st.form_submit_button("✨ Generate Itinerary")

# # ---------------- ON SUBMIT ----------------
# if submit_btn:
#     must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []
#     st.info("✈️ Generating your travel itinerary... please wait.")
    
#     # --- Prompt construction ---
#     prompt = f"""
#     You are an expert multi-agent travel planner.
#     Plan a {style}-style trip for {travelers} travelers visiting {destination}
#     from {start_date} to {end_date} with a {budget} budget.
#     Include daily activities, meals, lodging, and approximate costs.
#     Must-see attractions: {', '.join(must_see_list) if must_see_list else 'none'}.

#     Respond in structured JSON:
#     {{
#       "itinerary": [
#         {{
#           "day": 1,
#           "activities": ["..."],
#           "meals": ["..."],
#           "lodging": "...",
#           "estimated_cost": "..."
#         }}
#       ],
#       "total_estimated_cost": "...",
#       "summary": "..."
#     }}
#     """

#     try:
#         response = model.generate_content(prompt)
#         result_text = response.text.strip()

#         # --- Try parsing JSON safely ---
#         try:
#             result = json.loads(result_text)
#         except json.JSONDecodeError:
#             start_idx = result_text.find("{")
#             end_idx = result_text.rfind("}") + 1
#             json_str = result_text[start_idx:end_idx]
#             result = json.loads(json_str)

#         itinerary = result.get("itinerary", [])
#         total_cost = result.get("total_estimated_cost", "N/A")
#         summary = result.get("summary", "No summary available.")

#         # ---------------- DISPLAY RESULTS ----------------
#         st.success("✅ Itinerary Generated Successfully!")
#         st.markdown("### 🗺️ Your Personalized Travel Itinerary")

#         for day in itinerary:
#             with st.expander(f"🌞 Day {day.get('day', '?')} — {day.get('lodging', 'Details')}"):
#                 st.markdown("#### 🏃 Activities")
#                 for activity in day.get("activities", []):
#                     st.markdown(f"- {activity}")
#                 st.markdown("#### 🍽️ Meals")
#                 for meal in day.get("meals", []):
#                     st.markdown(f"- {meal}")
#                 st.markdown(f"#### 🏨 Lodging: **{day.get('lodging', 'N/A')}**")
#                 st.markdown(f"#### 💸 Estimated Cost: **{day.get('estimated_cost', 'N/A')}**")

#         # Summary Section
#         st.markdown("---")
#         st.markdown("### 🧾 Trip Summary")
#         st.markdown(f"**Total Estimated Cost:** {total_cost}")
#         st.markdown(f"**Overview:** {summary}")

#         # ---------------- DOWNLOAD OPTIONS ----------------
#         st.markdown("---")
#         st.markdown("### 📂 Download Options")

#         # JSON Download
#         st.download_button(
#             label="💾 Download JSON",
#             data=json.dumps(result, indent=2),
#             file_name="itinerary.json",
#             mime="application/json"
#         )

#         # PDF Export
#         try:
#             def itinerary_to_pdf_bytes(destination, start, end, data):
#                 pdf = FPDF()
#                 pdf.add_page()
#                 pdf.set_font("Arial", "B", 16)
#                 pdf.cell(0, 10, f"Travel Itinerary for {destination}", ln=True)
#                 pdf.set_font("Arial", size=12)
#                 pdf.cell(0, 10, f"Dates: {start} to {end}", ln=True)
#                 pdf.cell(0, 10, "", ln=True)

#                 for day in data.get("itinerary", []):
#                     pdf.set_font("Arial", "B", 14)
#                     pdf.cell(0, 10, f"Day {day['day']}", ln=True)
#                     pdf.set_font("Arial", "", 12)
#                     pdf.multi_cell(0, 10, f"Activities: {', '.join(day['activities'])}")
#                     pdf.multi_cell(0, 10, f"Meals: {', '.join(day.get('meals', []))}")
#                     pdf.multi_cell(0, 10, f"Lodging: {day['lodging']}")
#                     pdf.multi_cell(0, 10, f"Cost: {day['estimated_cost']}")
#                     pdf.cell(0, 10, "", ln=True)

#                 pdf.set_font("Arial", "B", 12)
#                 pdf.cell(0, 10, f"Total Estimated Cost: {data.get('total_estimated_cost')}", ln=True)
#                 pdf.multi_cell(0, 10, f"Summary: {data.get('summary')}")
#                 return bytes(pdf.output(dest="S").encode("latin-1"))

#             pdf_bytes = itinerary_to_pdf_bytes(destination, start_date, end_date, result)
#             st.download_button(
#                 label="📄 Download PDF",
#                 data=pdf_bytes,
#                 file_name=f"itinerary_{destination}.pdf",
#                 mime="application/pdf"
#             )
#         except Exception as e:
#             st.warning(f"PDF export unavailable: {e}")

#     except Exception as e:
#         st.error(f"❌ Error generating itinerary: {e}")


## version - 3

# import os
# import json
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai
# from fpdf import FPDF

# # --- Load .env and configure Gemini ---
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GEMINI_API_KEY)

# # --- Initialize model with tuned parameters ---
# model = genai.GenerativeModel(
#     "gemini-2.0-flash",
#     generation_config={
#         "temperature": 0.8,          # More creative, detailed responses
#         "top_p": 0.9,
#         "top_k": 40,
#         "max_output_tokens": 3000,   # Allow longer, more complete itineraries
#     },
# )

# # ---------------- STREAMLIT UI ----------------
# st.set_page_config(page_title="AI Travel Itinerary Planner", layout="centered")
# st.title("🌍 AI Travel Itinerary Planner")
# st.caption("Your personalized trip planner powered by **Google Gemini** 🧠")

# st.markdown("---")

# # ---------------- INPUT FORM ----------------
# with st.form("itinerary_form"):
#     destination = st.text_input("📍 Destination (city, country)", "Tokyo, Japan")
#     start_date = st.date_input("🗓️ Start Date")
#     end_date = st.date_input("🏁 End Date")
#     travelers = st.number_input("👨‍👩‍👧‍👦 Number of Travelers", min_value=1, value=1)
#     style = st.selectbox("🎯 Travel Style", ["relaxation", "adventure", "culture"])
#     budget = st.selectbox("💰 Budget Level", ["low", "medium", "high"])
#     must_see = st.text_area("🏖️ Must-See Attractions (optional, comma-separated)")
#     submit_btn = st.form_submit_button("✨ Generate Itinerary")

# # ---------------- ON SUBMIT ----------------
# if submit_btn:
#     must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []
#     st.info("✈️ Generating your detailed travel itinerary... please wait ⏳")
    
#     # --- Strong, detailed prompt ---
#     prompt = f"""
#     You are acting as a full CrewAI-style multi-agent system made up of:
#     - Destination Researcher
#     - Transport Agent
#     - Lodging Agent
#     - Itinerary Planner
#     - Budget Analyst
#     - Validator Agent

#     Together, plan a **comprehensive and detailed** {style}-style trip for {travelers} travelers visiting **{destination}**
#     from **{start_date}** to **{end_date}**, with a **{budget}** budget level.
#     Include transportation options, lodging suggestions, must-visit attractions, meal recommendations,
#     and daily time-structured activities (morning/afternoon/evening).

#     Make sure the itinerary is **multi-day**, covering every day in that date range.
#     Provide estimated costs for each day and a total at the end.
#     Include a short summary paragraph at the end.

#     Must-see attractions: {', '.join(must_see_list) if must_see_list else 'none'}.

#     Respond in clean JSON format like this (ensure valid JSON, no markdown):
#     {{
#       "itinerary": [
#         {{
#           "day": 1,
#           "activities": ["...", "..."],
#           "meals": ["...", "..."],
#           "lodging": "...",
#           "estimated_cost": "..."
#         }},
#         {{
#           "day": 2,
#           "activities": ["...", "..."],
#           "meals": ["...", "..."],
#           "lodging": "...",
#           "estimated_cost": "..."
#         }}
#       ],
#       "total_estimated_cost": "...",
#       "summary": "..."
#     }}
#     """

#     try:
#         response = model.generate_content(prompt)
#         result_text = response.text.strip()

#         # --- Try parsing JSON safely ---
#         try:
#             result = json.loads(result_text)
#         except json.JSONDecodeError:
#             start_idx = result_text.find("{")
#             end_idx = result_text.rfind("}") + 1
#             json_str = result_text[start_idx:end_idx]
#             result = json.loads(json_str)

#         itinerary = result.get("itinerary", [])
#         total_cost = result.get("total_estimated_cost", "N/A")
#         summary = result.get("summary", "No summary available.")

#         # ---------------- DISPLAY RESULTS ----------------
#         st.success("✅ Itinerary Generated Successfully!")
#         st.markdown("### 🗺️ Your Personalized Travel Itinerary")

#         for day in itinerary:
#             with st.expander(f"🌞 Day {day.get('day', '?')} — {day.get('lodging', 'Details')}"):
#                 st.markdown("#### 🏃 Activities")
#                 for activity in day.get("activities", []):
#                     st.markdown(f"- {activity}")
#                 st.markdown("#### 🍽️ Meals")
#                 for meal in day.get("meals", []):
#                     st.markdown(f"- {meal}")
#                 st.markdown(f"#### 🏨 Lodging: **{day.get('lodging', 'N/A')}**")
#                 st.markdown(f"#### 💸 Estimated Cost: **{day.get('estimated_cost', 'N/A')}**")

#         # Summary Section
#         st.markdown("---")
#         st.markdown("### 🧾 Trip Summary")
#         st.markdown(f"**Total Estimated Cost:** {total_cost}")
#         st.markdown(f"**Overview:** {summary}")

#         # ---------------- DOWNLOAD OPTIONS ----------------
#         st.markdown("---")
#         st.markdown("### 📂 Download Options")

#         # JSON Download
#         st.download_button(
#             label="💾 Download JSON",
#             data=json.dumps(result, indent=2),
#             file_name="itinerary.json",
#             mime="application/json"
#         )

#         # PDF Export
#         try:
#             def itinerary_to_pdf_bytes(destination, start, end, data):
#                 pdf = FPDF()
#                 pdf.add_page()
#                 pdf.set_font("Arial", "B", 16)
#                 pdf.cell(0, 10, f"Travel Itinerary for {destination}", ln=True)
#                 pdf.set_font("Arial", size=12)
#                 pdf.cell(0, 10, f"Dates: {start} to {end}", ln=True)
#                 pdf.cell(0, 10, "", ln=True)

#                 for day in data.get("itinerary", []):
#                     pdf.set_font("Arial", "B", 14)
#                     pdf.cell(0, 10, f"Day {day['day']}", ln=True)
#                     pdf.set_font("Arial", "", 12)
#                     pdf.multi_cell(0, 10, f"Activities: {', '.join(day['activities'])}")
#                     pdf.multi_cell(0, 10, f"Meals: {', '.join(day.get('meals', []))}")
#                     pdf.multi_cell(0, 10, f"Lodging: {day['lodging']}")
#                     pdf.multi_cell(0, 10, f"Cost: {day['estimated_cost']}")
#                     pdf.cell(0, 10, "", ln=True)

#                 pdf.set_font("Arial", "B", 12)
#                 pdf.cell(0, 10, f"Total Estimated Cost: {data.get('total_estimated_cost')}", ln=True)
#                 pdf.multi_cell(0, 10, f"Summary: {data.get('summary')}")
#                 return bytes(pdf.output(dest="S").encode("latin-1"))

#             pdf_bytes = itinerary_to_pdf_bytes(destination, start_date, end_date, result)
#             st.download_button(
#                 label="📄 Download PDF",
#                 data=pdf_bytes,
#                 file_name=f"itinerary_{destination}.pdf",
#                 mime="application/pdf"
#             )
#         except Exception as e:
#             st.warning(f"PDF export unavailable: {e}")

#     except Exception as e:
#         st.error(f"❌ Error generating itinerary: {e}")


############# version - 4 ##################################

# import os
# import streamlit as st
# from ai_travel_itinerary_planner.crew import AiTravelItineraryPlannerCrew

# from dotenv import load_dotenv
# import sys

# load_dotenv()
# sys.path.append(os.getenv("PYTHONPATH", "."))



# # ---------------- Streamlit UI ----------------
# st.set_page_config(page_title="CrewAI Travel Itinerary Planner", layout="centered")
# st.title("🧭 CrewAI-Powered Travel Itinerary Planner")
# st.caption("Generate personalized travel itineraries using your local CrewAI automation.")

# st.markdown("---")

# with st.form("travel_form"):
#     destination = st.text_input("Destination (City, Country)", "Tokyo, Japan")
#     start_date = st.date_input("Start Date")
#     end_date = st.date_input("End Date")
#     travelers = st.number_input("Number of Travelers", min_value=1, value=2)
#     travel_style = st.selectbox("Travel Style", ["relaxation", "adventure", "culture"])
#     budget_band = st.selectbox("Budget Level", ["low", "medium", "high"])
#     must_see = st.text_area("Must-See Attractions (optional, comma-separated)")
#     trip_duration = (end_date - start_date).days
#     if trip_duration <= 0:
#         st.warning("⚠️ End date must be after the start date.")
#         trip_duration = 0
#     else:
#         st.info(f"📅 Trip Duration: **{trip_duration} days**")
#     submit_btn = st.form_submit_button("Generate Itinerary 🚀")

# # ---------------- Execution ----------------
# if submit_btn:
#     st.info("🧠 Running CrewAI agents... please wait ⏳")

#     try:
#         # Initialize Crew
#         crew = AiTravelItineraryPlannerCrew().crew()

#         # Define input payload for Crew
#         must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []
#         inputs = {
#             "destination": destination,
#             "start_date": str(start_date),
#             "end_date": str(end_date),
#             "trip_duration": trip_duration,
#             "travelers": travelers,
#             "style": travel_style,
#             "budget_range": budget_band,
#             "must_sees": must_see_list
#         }

#         # Kick off CrewAI workflow
#         result = crew.kickoff(inputs=inputs)

#         # Display results
#         st.success("✅ Itinerary generated successfully!")
#         st.markdown("### 🗺️ Final Itinerary")
#         st.write(result)

#     except Exception as e:
#         st.error(f"❌ Error running CrewAI automation: {e}")


################## Version - 5 #######################

# import os
# import sys
# import streamlit as st
# from dotenv import load_dotenv
# from datetime import date
# from ai_travel_itinerary_planner.crew import AiTravelItineraryPlannerCrew

# # ----------------------------------------------------------------
# #  Load environment and ensure local module path is added
# # ----------------------------------------------------------------
# load_dotenv(override=True)
# sys.path.append(os.getenv("PYTHONPATH", "."))

# # ----------------------------------------------------------------
# #  Streamlit Page Config
# # ----------------------------------------------------------------
# st.set_page_config(page_title="CrewAI Travel Itinerary Planner", layout="centered")
# st.title("🧭 CrewAI-Powered Travel Itinerary Planner")
# st.caption("Generate personalized travel itineraries using **CrewAI multi-agent system.**")
# st.markdown("---")

# # ----------------------------------------------------------------
# #  User Input Form
# # ----------------------------------------------------------------
# with st.form("travel_form"):
#     destination = st.text_input("📍 Destination (City, Country)", "Tokyo, Japan")
#     start_date = st.date_input("🗓️ Start Date")
#     end_date = st.date_input("🏁 End Date")
#     travelers = st.number_input("👥 Number of Travelers", min_value=1, value=2)
#     travel_style = st.selectbox("🎯 Travel Style", ["relaxation", "adventure", "culture"])
#     budget_band = st.selectbox("💰 Budget Level", ["low", "medium", "high"])
#     must_see = st.text_area("🏖️ Must-See Attractions (optional, comma-separated)")

#     # Extra optional fields for future-proofing
#     traveler_preferences = st.text_input(
#         "💡 Traveler Preferences", "Flexible and open to local experiences"
#     )
#     preferred_transport = st.selectbox(
#         "🚗 Preferred Transport Mode",
#         ["public transport", "car rental", "walking", "mixed"],
#         index=0,
#     )

#     # Auto-calculate trip duration
#     trip_duration = (end_date - start_date).days
#     if trip_duration <= 0:
#         st.warning("⚠️ End date must be after start date.")
#         trip_duration = 0
#     else:
#         st.info(f"📅 Trip Duration: **{trip_duration} days**")

#     submit_btn = st.form_submit_button("🚀 Generate Itinerary")

# # ----------------------------------------------------------------
# #  Execution
# # ----------------------------------------------------------------
# if submit_btn:
#     if trip_duration <= 0:
#         st.stop()

#     st.info("🧠 Running CrewAI agents... please wait ⏳")

#     try:
#         # Initialize Crew
#         crew = AiTravelItineraryPlannerCrew().crew()

#         # Clean & prepare input list
#         must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []

#         # ---------------- Inputs for CrewAI ----------------
#         inputs = {
#             "destination": destination,
#             "start_date": str(start_date),
#             "end_date": str(end_date),
#             "trip_duration": trip_duration,
#             "travelers": travelers,
#             "style": travel_style,
#             "budget_range": budget_band,
#             "must_sees": must_see_list,
#             "traveler_preferences": traveler_preferences,
#             "preferred_transport": preferred_transport,
#         }

#         # ---- Safe Defaults for all optional Crew template vars ----
#         DEFAULTS = {
#             "currency": "USD",
#             "language": "English",
#             "group_type": "friends",
#             "pacing": "moderate",
#             "weather_preference": "mild",
#             "accommodation_type": "mid-range hotels",
#         }
#         for k, v in DEFAULTS.items():
#             inputs.setdefault(k, v)

#         # ----------------------------------------------------------------
#         #  Run CrewAI Orchestration
#         # ----------------------------------------------------------------
#         result = crew.kickoff(inputs=inputs)

#         # ----------------------------------------------------------------
#         #  Display Results Beautifully
#         # ----------------------------------------------------------------
#         st.success("✅ Itinerary generated successfully!")
#         st.markdown("### 🗺️ Your Personalized Travel Itinerary")

#         if isinstance(result, dict) and "itinerary" in result:
#             for day in result["itinerary"]:
#                 with st.expander(f"🌞 Day {day.get('day', '?')} — {day.get('lodging', 'Details')}"):
#                     st.markdown("#### 🏃 Activities")
#                     for activity in day.get("activities", []):
#                         st.markdown(f"- {activity}")
#                     st.markdown("#### 🍽️ Meals")
#                     for meal in day.get("meals", []):
#                         st.markdown(f"- {meal}")
#                     st.markdown(f"#### 🏨 Lodging: **{day.get('lodging', 'N/A')}**")
#                     st.markdown(f"#### 💸 Estimated Cost: **{day.get('estimated_cost', 'N/A')}**")

#             st.markdown("---")
#             st.markdown("### 🧾 Trip Summary")
#             st.markdown(f"**Total Estimated Cost:** {result.get('total_estimated_cost', 'N/A')}")
#             st.markdown(f"**Overview:** {result.get('summary', 'No summary available.')}")
#         else:
#             st.json(result)

#     except Exception as e:
#         st.error(f"❌ Error running CrewAI automation: {e}")



############# Version - 6  #################################

# import os
# import sys
# import streamlit as st
# from dotenv import load_dotenv
# from datetime import date
# from ai_travel_itinerary_planner.crew import AiTravelItineraryPlannerCrew

# # ----------------------------------------------------------------
# #  Load environment and ensure local module path is added
# # ----------------------------------------------------------------
# load_dotenv(override=True)
# sys.path.append(os.getenv("PYTHONPATH", "."))

# # ----------------------------------------------------------------
# #  Streamlit Page Config
# # ----------------------------------------------------------------
# st.set_page_config(page_title="CrewAI Travel Itinerary Planner", layout="centered")
# st.title("🧭 CrewAI-Powered Travel Itinerary Planner")
# st.caption("Generate personalized travel itineraries using **CrewAI multi-agent system.**")
# st.markdown("---")

# # ----------------------------------------------------------------
# #  User Input Form
# # ----------------------------------------------------------------
# with st.form("travel_form"):
#     destination = st.text_input("📍 Destination (City, Country)", "Tokyo, Japan")
#     start_date = st.date_input("🗓️ Start Date")
#     end_date = st.date_input("🏁 End Date")
#     travelers = st.number_input("👥 Number of Travelers", min_value=1, value=2)
#     travel_style = st.selectbox("🎯 Travel Style", ["relaxation", "adventure", "culture"])
#     budget_band = st.selectbox("💰 Budget Level", ["low", "medium", "high"])
#     must_see = st.text_area("🏖️ Must-See Attractions (optional, comma-separated)")

#     # Extra optional fields for future-proofing
#     traveler_preferences = st.text_input(
#         "💡 Traveler Preferences", "Flexible and open to local experiences"
#     )
#     preferred_transport = st.selectbox(
#         "🚗 Preferred Transport Mode",
#         ["public transport", "car rental", "walking", "mixed"],
#         index=0,
#     )

#     # Auto-calculate trip duration
#     trip_duration = (end_date - start_date).days
#     if trip_duration <= 0:
#         st.warning("⚠️ End date must be after start date.")
#         trip_duration = 0
#     else:
#         st.info(f"📅 Trip Duration: **{trip_duration} days**")

#     submit_btn = st.form_submit_button("🚀 Generate Itinerary")

# # ----------------------------------------------------------------
# #  Execution
# # ----------------------------------------------------------------
# if submit_btn:
#     if trip_duration <= 0:
#         st.stop()

#     st.info("🧠 Running CrewAI agents... please wait ⏳")

#     try:
#         # Initialize Crew
#         crew = AiTravelItineraryPlannerCrew().crew()

#         # Clean & prepare input list
#         must_see_list = [x.strip() for x in must_see.split(",")] if must_see else []

#         # ---------------- Inputs for CrewAI ----------------
#         inputs = {
#             "destination": destination,
#             "start_date": str(start_date),
#             "end_date": str(end_date),
#             "trip_duration": trip_duration,
#             "travelers": travelers,
#             "style": travel_style,
#             "budget_range": budget_band,
#             "must_sees": must_see_list,
#             "traveler_preferences": traveler_preferences,
#             "preferred_transport": preferred_transport,
#         }

#         # ---- Safe Defaults for all optional Crew template vars ----
#         DEFAULTS = {
#             "currency": "USD",
#             "language": "English",
#             "group_type": "friends",
#             "pacing": "moderate",
#             "weather_preference": "mild",
#             "accommodation_type": "mid-range hotels",
#         }
#         for k, v in DEFAULTS.items():
#             inputs.setdefault(k, v)

#         # ----------------------------------------------------------------
#         #  Run CrewAI Orchestration
#         # ----------------------------------------------------------------
#         result = crew.kickoff(inputs=inputs)

#         # ----------------------------------------------------------------
#         #  Display Results Beautifully
#         # ----------------------------------------------------------------
#         from fpdf import FPDF
#         import textwrap

#         st.success("✅ Itinerary generated successfully!")
#         st.markdown("### 🗺️ Your Personalized Travel Itinerary")

#         # Handle both JSON and raw Markdown-style output
#         # if isinstance(result, dict) and "itinerary" in result:
#         #     itinerary = result["itinerary"]
#         #     total_cost = result.get("total_estimated_cost", "N/A")
#         #     summary = result.get("summary", "No summary available.")
#         # else:
#         #     # Extract markdown-like text and display as formatted sections
#         #     st.markdown(result.get("raw", "No structured data found."), unsafe_allow_html=True)
#         #     itinerary, total_cost, summary = [], "N/A", "No structured itinerary available."
        
#         if hasattr(result, "raw"):
#             raw_output = result.raw
#         else:
#             raw_output = str(result)
            
#         # Try parsing JSON safely if possible
#         import json
#         try:
#             parsed = json.loads(raw_output)
#             itinerary = parsed.get("itinerary", [])
#             total_cost = parsed.get("total_estimated_cost", "N/A")
#             summary = parsed.get("summary", "No summary available.")
#         except Exception:
#             itinerary, total_cost, summary = [], "N/A", "No structured itinerary available."
#             st.markdown(raw_output, unsafe_allow_html=True)

#         # -------------------------- Streamlit Display --------------------------
#         if itinerary or raw_output.strip():
#             for day in itinerary:
#                 with st.expander(f"🌞 Day {day.get('day', '?')} — {day.get('lodging', 'Details')}"):
#                     st.markdown("#### 🏃 Activities")
#                     for activity in day.get("activities", []):
#                         st.markdown(f"- {activity}")
#                     st.markdown("#### 🍽️ Meals")
#                     for meal in day.get("meals", []):
#                         st.markdown(f"- {meal}")
#                     st.markdown(f"#### 🏨 Lodging: **{day.get('lodging', 'N/A')}**")
#                     st.markdown(f"#### 💸 Estimated Cost: **{day.get('estimated_cost', 'N/A')}**")

#         # st.markdown("---")
#         # st.markdown("### 🧾 Trip Summary")
#         # st.markdown(f"**Total Estimated Cost:** {total_cost}")
#         # st.markdown(f"**Overview:** {summary}")

#         # ----------------------------------------------------------------
#         #  Generate Beautiful PDF
#         # ----------------------------------------------------------------
#         def create_pdf(destination, start_date, end_date, itinerary, total_cost, summary):
#             pdf = FPDF()
#             pdf.add_page()
#             pdf.set_auto_page_break(auto=True, margin=15)

#             # --- Title ---
#             pdf.set_fill_color(33, 150, 243)
#             pdf.set_text_color(255, 255, 255)
#             pdf.set_font("Arial", "B", 20)
#             pdf.cell(0, 15, f"Travel Itinerary for {destination}", ln=True, align="C", fill=True)
#             pdf.ln(5)

#             # --- Dates & Trip Info ---
#             pdf.set_text_color(0, 0, 0)
#             pdf.set_font("Arial", "", 12)
#             pdf.multi_cell(0, 10, f"Dates: {start_date} to {end_date}")
#             pdf.multi_cell(0, 10, f"Total Estimated Cost: {total_cost}")
#             pdf.ln(5)

#             # --- Day-by-Day ---
#             for day in itinerary:
#                 pdf.set_fill_color(240, 240, 240)
#                 pdf.set_font("Arial", "B", 14)
#                 pdf.cell(0, 10, f"Day {day.get('day', '?')}", ln=True, fill=True)
#                 pdf.set_font("Arial", "", 12)
#                 pdf.multi_cell(0, 8, f"Lodging: {day.get('lodging', 'N/A')}")
#                 pdf.multi_cell(0, 8, f"Estimated Cost: {day.get('estimated_cost', 'N/A')}")
#                 pdf.ln(2)

#                 pdf.set_font("Arial", "B", 12)
#                 pdf.cell(0, 8, "Activities:", ln=True)
#                 pdf.set_font("Arial", "", 12)
#                 for activity in day.get("activities", []):
#                     pdf.multi_cell(0, 8, f"• {activity}")
#                 pdf.ln(2)

#                 pdf.set_font("Arial", "B", 12)
#                 pdf.cell(0, 8, "Meals:", ln=True)
#                 pdf.set_font("Arial", "", 12)
#                 for meal in day.get("meals", []):
#                     pdf.multi_cell(0, 8, f"• {meal}")
#                 pdf.ln(5)

#             # --- Summary Section ---
#             pdf.set_fill_color(33, 150, 243)
#             pdf.set_text_color(255, 255, 255)
#             pdf.set_font("Arial", "B", 14)
#             pdf.cell(0, 10, "Trip Summary", ln=True, fill=True)
#             pdf.set_text_color(0, 0, 0)
#             pdf.set_font("Arial", "", 12)
#             for line in textwrap.wrap(summary, width=100):
#                 pdf.multi_cell(0, 8, line)
#             pdf.ln(10)

#             # Return bytes
#             return bytes(pdf.output(dest="S").encode("latin-1"))

#         # # Only generate a PDF if itinerary exists
#         # if itinerary:
#         #     pdf_bytes = create_pdf(destination, start_date, end_date, itinerary, total_cost, summary)
#         #     st.download_button(
#         #         label="📄 Download Itinerary as PDF",
#         #         data=pdf_bytes,
#         #         file_name=f"itinerary_{destination.replace(' ', '_')}.pdf",
#         #         mime="application/pdf",
#         #     )
        
#         # Only generate a PDF if itinerary or raw output exists
#         if itinerary or raw_output.strip():
#             pdf_bytes = create_pdf(destination, start_date, end_date, itinerary, total_cost, summary)
#             st.download_button(
#                 label="📄 Download Itinerary as PDF",
#                 data=pdf_bytes,
#                 file_name=f"itinerary_{destination.replace(' ', '_')}.pdf",
#                 mime="application/pdf",
#             )

#     except Exception as e:
#         st.error(f"❌ Error running CrewAI automation: {e}")
        
        
####################### Version - 7 ############################

import os
import sys
import streamlit as st
from dotenv import load_dotenv
from datetime import date
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



