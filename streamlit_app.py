import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Ultimate Hiking Guide",
    page_icon="🏔️",
    layout="wide"
)

st.title("🏔️ Ultimate Hiking Guide")
st.caption("Your AI-powered personal hiking expert")
st.divider()

with st.sidebar:
    st.header("🎯 Your Preferences")
    location = st.text_input("📍 Location", placeholder="e.g. Brisbane, Queensland")
    difficulty = st.multiselect("💪 Difficulty", ["Easy", "Medium", "Hard", "Expert"], default=["Easy", "Medium"])
    min_dist, max_dist = st.slider("📏 Distance (km)", 1, 100, (5, 20))
    num_trails = st.selectbox("🔢 Number of Trails", [3, 5, 10], index=1)
    st.divider()
    st.subheader("🌿 Features")
    pet_friendly = st.checkbox("🐕 Pet Friendly")
    family_friendly = st.checkbox("👨‍👩‍👧 Family Friendly")
    wheelchair = st.checkbox("♿ Wheelchair Accessible")
    st.divider()
    st.subheader("🏞️ Scenery")
    scenery = st.multiselect("What do you want to see?", ["Ocean Views", "Waterfalls", "Forest", "Mountains", "Wildlife", "Lakes", "Canyons"], default=["Forest", "Wildlife"])
    season = st.selectbox("📅 Season", ["Summer", "Autumn", "Winter", "Spring"])
    st.divider()
    find_button = st.button("🔍 Find My Perfect Trails!", use_container_width=True)

def render_trail_card(trail, index):
    difficulty = trail.get("difficulty", "Easy")
    color_map = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴", "Expert": "🟣"}
    icon = color_map.get(difficulty, "🟢")

    with st.container(border=True):
        st.subheader(f"#{index} {trail.get('name', 'Unknown Trail')}")
        
        badges = f"{icon} **{difficulty}**"
        if trail.get("pet_friendly") == "Yes": badges += " · 🐕 Pet Friendly"
        if trail.get("family_friendly") == "Yes": badges += " · 👨‍👩‍👧 Family Friendly"
        if trail.get("accessible") == "Yes": badges += " · ♿ Accessible"
        st.markdown(badges)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📏 Distance", trail.get("distance", "N/A"))
            st.metric("⏱️ Time", trail.get("time", "N/A"))
        with col2:
            st.metric("📈 Elevation", trail.get("elevation", "N/A"))
            st.metric("🌟 Rating", trail.get("rating", "N/A"))
        with col3:
            st.metric("📅 Best Season", trail.get("best_season", "N/A"))
            st.metric("📍 Location", trail.get("location", "N/A"))
        
        st.divider()
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"🌿 **Scenery:** {trail.get('scenery', 'N/A')}")
            st.markdown(f"🦘 **Wildlife:** {trail.get('wildlife', 'N/A')}")
            st.markdown(f"👟 **What to Bring:** {trail.get('what_to_bring', 'N/A')}")
            st.markdown(f"🅿️ **Parking:** {trail.get('parking', 'N/A')}")
        with col_b:
            st.markdown(f"⚠️ **Warnings:** {trail.get('warnings', 'N/A')}")
            st.markdown(f"🗺️ **How to Get There:** {trail.get('how_to_get_there', 'N/A')}")
        
        st.info(f"💡 **Pro Tip:** {trail.get('pro_tip', 'N/A')}")

if find_button:
    if not location:
        st.warning("⚠️ Please enter a location!")
    elif not difficulty:
        st.warning("⚠️ Please select at least one difficulty level!")
    else:
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
        
        filters = []
        if pet_friendly: filters.append("pet friendly")
        if family_friendly: filters.append("family friendly")
        if wheelchair: filters.append("wheelchair accessible")
        
        prompt = ChatPromptTemplate.from_template("""
You are an expert hiking guide. Recommend exactly {num_trails} real hiking trails.

User Preferences:
- Location: {location}
- Difficulty: {difficulty}
- Distance: {min_dist}km to {max_dist}km
- Requirements: {filters}
- Scenery: {scenery}
- Season: {season}

Return ONLY a valid JSON array, no other text, no markdown, no explanation.
Format exactly like this:
[
  {{
    "name": "Trail Name",
    "location": "Specific location",
    "distance": "X km",
    "difficulty": "Easy/Medium/Hard/Expert",
    "time": "X-X hours",
    "elevation": "X meters",
    "rating": "X/10",
    "pet_friendly": "Yes/No",
    "family_friendly": "Yes/No",
    "accessible": "Yes/No",
    "scenery": "description",
    "wildlife": "animals you might see",
    "best_season": "season",
    "what_to_bring": "items list",
    "parking": "parking info",
    "warnings": "hazards",
    "how_to_get_there": "directions",
    "pro_tip": "expert tip"
  }}
]
""")
        
        chain = prompt | llm
        
        with st.spinner("🔍 Finding the best trails for you..."):
            response = chain.invoke({
                "location": location,
                "difficulty": ", ".join(difficulty),
                "min_dist": min_dist,
                "max_dist": max_dist,
                "num_trails": num_trails,
                "filters": ", ".join(filters) if filters else "none",
                "scenery": ", ".join(scenery) if scenery else "any",
                "season": season
            })
        
        try:
            text = response.content.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            trails = json.loads(text)
            
            st.success(f"✅ Found {len(trails)} amazing trails in {location}!")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📍 Location", location)
            col2.metric("📏 Distance", f"{min_dist}-{max_dist} km")
            col3.metric("💪 Difficulty", ", ".join(difficulty))
            col4.metric("🔢 Trails", len(trails))
            
            st.divider()
            
            for i, trail in enumerate(trails, 1):
                render_trail_card(trail, i)
            
            st.divider()
            with st.expander("⚠️ Safety Reminders"):
                st.markdown("""
                - Always check weather before heading out
                - Tell someone where you're going and when you'll be back
                - Bring more water than you think you need
                - Download offline maps before your hike
                - Fully charge your phone and bring a power bank
                - Always carry a basic first aid kit
                """)
        
        except json.JSONDecodeError:
            st.error("Something went wrong, please try again!")