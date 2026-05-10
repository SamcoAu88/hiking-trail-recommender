import os
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
st.write("Your personal hiking trail expert — find the perfect trail for any adventure!")

with st.sidebar:
    st.header("🎯 Your Preferences")
    
    location = st.text_input("📍 Location", placeholder="e.g. Brisbane, Queensland")
    
    difficulty = st.multiselect(
        "💪 Difficulty Level",
        ["Easy", "Medium", "Hard", "Expert"],
        default=["Easy", "Medium"]
    )
    
    min_dist, max_dist = st.slider(
        "📏 Distance Range (km)",
        min_value=1, max_value=100,
        value=(5, 20)
    )
    
    num_trails = st.selectbox("🔢 Number of Trails", [3, 5, 10], index=1)
    
    st.subheader("🌿 Trail Features")
    pet_friendly = st.checkbox("🐕 Pet Friendly")
    family_friendly = st.checkbox("👨‍👩‍👧 Family Friendly")
    wheelchair = st.checkbox("♿ Wheelchair Accessible")
    
    st.subheader("🏞️ Scenery Type")
    scenery = st.multiselect(
        "What do you want to see?",
        ["Ocean Views", "Waterfalls", "Forest", "Mountains", "Wildlife", "Lakes", "Canyons"],
        default=["Forest", "Wildlife"]
    )
    
    season = st.selectbox(
        "📅 Current Season",
        ["Summer", "Autumn", "Winter", "Spring"]
    )
    
    find_button = st.button("🔍 Find My Trails!", use_container_width=True)

if find_button:
    if not location:
        st.warning("Please enter a location!")
    elif not difficulty:
        st.warning("Please select at least one difficulty level!")
    else:
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
        
        filters = []
        if pet_friendly:
            filters.append("pet friendly")
        if family_friendly:
            filters.append("family friendly")
        if wheelchair:
            filters.append("wheelchair accessible")
        
        filters_text = ", ".join(filters) if filters else "no specific requirements"
        scenery_text = ", ".join(scenery) if scenery else "any scenery"
        difficulty_text = ", ".join(difficulty)
        
        prompt = ChatPromptTemplate.from_template("""
You are an expert hiking guide with deep knowledge of trails worldwide.
Recommend exactly {num_trails} hiking trails based on these preferences.

User Preferences:
- Location: {location}
- Difficulty: {difficulty}
- Distance: {min_dist}km to {max_dist}km
- Special requirements: {filters}
- Scenery preferences: {scenery}
- Current season: {season}

For EACH trail, provide ALL of the following in this exact format:

🏔️ TRAIL NAME: [name]
📍 LOCATION: [specific location with address if possible]
📏 DISTANCE: [X km]
⛰️ DIFFICULTY: [Easy/Medium/Hard/Expert]
⏱️ ESTIMATED TIME: [X-X hours]
📈 ELEVATION GAIN: [X meters]
🌟 RATING: [X/10]
🐕 PET FRIENDLY: [Yes/No]
👨‍👩‍👧 FAMILY FRIENDLY: [Yes/No]
♿ ACCESSIBLE: [Yes/No]
🌿 SCENERY: [what you'll see]
🦘 WILDLIFE: [animals you might spot]
📅 BEST SEASON: [best time to visit]
👟 WHAT TO BRING: [essential items list]
🅿️ PARKING: [parking information]
⚠️ WARNINGS: [any hazards or important notes]
🗺️ HOW TO GET THERE: [brief directions or landmark]
💡 PRO TIP: [one expert tip for this trail]

---

Make sure trails are real, accurate, and match the season {season}.
Be enthusiastic, detailed and helpful like a local expert!
""")
        
        chain = prompt | llm
        
        with st.spinner("🔍 Searching for the best trails..."):
            response = chain.invoke({
                "location": location,
                "difficulty": difficulty_text,
                "min_dist": min_dist,
                "max_dist": max_dist,
                "num_trails": num_trails,
                "filters": filters_text,
                "scenery": scenery_text,
                "season": season
            })
        
        st.success(f"Found {num_trails} amazing trails for you!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📍 Location", location)
        with col2:
            st.metric("📏 Distance Range", f"{min_dist}-{max_dist} km")
        with col3:
            st.metric("🔢 Trails Found", num_trails)
        
        st.divider()
        st.markdown(response.content)
        
        st.divider()
        st.subheader("⚠️ Safety Reminders")
        st.info("""
        - Always check weather before heading out
        - Tell someone where you're going
        - Bring more water than you think you need
        - Download offline maps
        - Charge your phone fully
        - First aid kit is always a good idea
        """)