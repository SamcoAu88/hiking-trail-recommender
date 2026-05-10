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

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f1117 0%, #1a2332 100%); }
    h1 { color: #4CAF50 !important; text-align: center; font-size: 3rem !important; }
    .subtitle { text-align: center; color: #a0aec0; font-size: 1.2rem; margin-bottom: 2rem; }
    
    .trail-card {
        background: linear-gradient(135deg, #1e2d3d, #2d3748);
        border: 1px solid #4CAF50;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.2);
    }
    .trail-title {
        color: #4CAF50;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 1px solid #4CAF50;
        padding-bottom: 10px;
    }
    .trail-detail {
        color: #e2e8f0;
        margin: 8px 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        margin: 3px;
    }
    .badge-easy { background: #276749; color: #9ae6b4; }
    .badge-medium { background: #744210; color: #fbd38d; }
    .badge-hard { background: #742a2a; color: #feb2b2; }
    .badge-expert { background: #44337a; color: #d6bcfa; }
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #2d8a32) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2332, #0f1117) !important;
        border-right: 1px solid #4CAF50 !important;
    }
    .metric-box {
        background: #2d3748;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #4a5568;
        height: 150px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏔️ Ultimate Hiking Guide</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI-powered personal hiking expert</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎯 Trail Preferences")
    st.markdown("---")
    location = st.text_input("📍 Where do you want to hike?", placeholder="e.g. Brisbane, Queensland")
    difficulty = st.multiselect("💪 Difficulty Level", ["Easy", "Medium", "Hard", "Expert"], default=["Easy", "Medium"])
    min_dist, max_dist = st.slider("📏 Distance Range (km)", 1, 100, (5, 20))
    num_trails = st.selectbox("🔢 Number of Trails", [3, 5, 10], index=1)
    st.markdown("---")
    st.markdown("### 🌿 Features")
    pet_friendly = st.checkbox("🐕 Pet Friendly")
    family_friendly = st.checkbox("👨‍👩‍👧 Family Friendly")
    wheelchair = st.checkbox("♿ Wheelchair Accessible")
    st.markdown("---")
    st.markdown("### 🏞️ Scenery")
    scenery = st.multiselect("What do you want to see?", ["Ocean Views", "Waterfalls", "Forest", "Mountains", "Wildlife", "Lakes", "Canyons"], default=["Forest", "Wildlife"])
    season = st.selectbox("📅 Season", ["Summer", "Autumn", "Winter", "Spring"])
    st.markdown("---")
    find_button = st.button("🔍 Find My Perfect Trails!")

def get_difficulty_badge(difficulty):
    d = difficulty.lower()
    if d == "easy":
        return '<span class="badge badge-easy">🟢 Easy</span>'
    elif d == "medium":
        return '<span class="badge badge-medium">🟡 Medium</span>'
    elif d == "hard":
        return '<span class="badge badge-hard">🔴 Hard</span>'
    else:
        return '<span class="badge badge-expert">🟣 Expert</span>'

def render_trail_card(trail, index):
    difficulty_badge = get_difficulty_badge(trail.get("difficulty", ""))
    
    card_html = f"""
    <div class="trail-card">
        <div class="trail-title">#{index} 🏔️ {trail.get("name", "Unknown Trail")}</div>
        
        <div style="margin-bottom: 15px;">
            {difficulty_badge}
            {"🐕 Pet Friendly" if trail.get("pet_friendly") == "Yes" else ""}
            {"👨‍👩‍👧 Family Friendly" if trail.get("family_friendly") == "Yes" else ""}
            {"♿ Accessible" if trail.get("accessible") == "Yes" else ""}
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;">
            <div class="trail-detail">📍 <b>Location:</b> {trail.get("location", "N/A")}</div>
            <div class="trail-detail">📏 <b>Distance:</b> {trail.get("distance", "N/A")}</div>
            <div class="trail-detail">⏱️ <b>Time:</b> {trail.get("time", "N/A")}</div>
            <div class="trail-detail">📈 <b>Elevation:</b> {trail.get("elevation", "N/A")}</div>
            <div class="trail-detail">🌟 <b>Rating:</b> {trail.get("rating", "N/A")}</div>
            <div class="trail-detail">📅 <b>Best Season:</b> {trail.get("best_season", "N/A")}</div>
        </div>
        
        <div class="trail-detail">🌿 <b>Scenery:</b> {trail.get("scenery", "N/A")}</div>
        <div class="trail-detail">🦘 <b>Wildlife:</b> {trail.get("wildlife", "N/A")}</div>
        <div class="trail-detail">👟 <b>What to Bring:</b> {trail.get("what_to_bring", "N/A")}</div>
        <div class="trail-detail">🅿️ <b>Parking:</b> {trail.get("parking", "N/A")}</div>
        <div class="trail-detail">⚠️ <b>Warnings:</b> {trail.get("warnings", "N/A")}</div>
        <div class="trail-detail">🗺️ <b>How to Get There:</b> {trail.get("how_to_get_there", "N/A")}</div>
        <div style="margin-top: 15px; padding: 10px; background: #1a3a1a; border-radius: 8px; border-left: 3px solid #4CAF50;">
            💡 <b>Pro Tip:</b> {trail.get("pro_tip", "N/A")}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

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
            with col1:
                st.metric("📍 Location", location)
            with col2:
                st.metric("📏 Distance", f"{min_dist}-{max_dist} km")
            with col3:
                st.metric("💪 Difficulty", ", ".join(difficulty))
            with col4:
                st.metric("🔢 Trails", len(trails))
            
            st.markdown("---")
            
            for i, trail in enumerate(trails, 1):
                render_trail_card(trail, i)
            
            st.markdown("---")
            st.markdown("""
            <div style="background: #1a2332; border-left: 4px solid #f6ad55; border-radius: 10px; padding: 20px; margin-top: 20px;">
                <h3 style="color: #f6ad55;">⚠️ Safety Reminders</h3>
                <ul style="color: #e2e8f0;">
                    <li>Always check weather before heading out</li>
                    <li>Tell someone where you're going and when you'll be back</li>
                    <li>Bring more water than you think you need</li>
                    <li>Download offline maps before your hike</li>
                    <li>Fully charge your phone and bring a power bank</li>
                    <li>Always carry a basic first aid kit</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        except json.JSONDecodeError:
            st.error("Something went wrong, please try again!")
            st.text(response.content)

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h2>🌍</h2>
            <h3 style="color: white;">Worldwide Trails</h3>
            <p style="color: #a0aec0;">Search any location on Earth</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h2>🤖</h2>
            <h3 style="color: white;">AI Powered</h3>
            <p style="color: #a0aec0;">Smart recommendations just for you</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h2>🎯</h2>
            <h3 style="color: white;">Personalized</h3>
            <p style="color: #a0aec0;">Tailored to your preferences</p>
        </div>
        """, unsafe_allow_html=True)