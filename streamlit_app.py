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

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background: linear-gradient(135deg, #0f1117 0%, #1a2332 100%); }
    
    h1 { 
        color: #4CAF50 !important; 
        font-size: 3rem !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
    }
    
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .trail-card {
        background: linear-gradient(135deg, #1e2d3d, #2d3748);
        border: 1px solid #4CAF50;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.2);
    }
    
    .metric-box {
        background: #2d3748;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #4a5568;
    }
    
    .safety-box {
        background: linear-gradient(135deg, #1a2332, #2d3748);
        border-left: 4px solid #f6ad55;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #2d8a32) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4) !important;
    }

    .stSelectbox, .stMultiSelect, .stTextInput {
        background: #2d3748 !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2332, #0f1117) !important;
        border-right: 1px solid #4CAF50 !important;
    }

    .stSuccess {
        background: #1a3a1a !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏔️ Ultimate Hiking Guide</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI-powered personal hiking expert — discover your perfect trail</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎯 Trail Preferences")
    st.markdown("---")
    
    location = st.text_input("📍 Where do you want to hike?", placeholder="e.g. Brisbane, Queensland")
    
    difficulty = st.multiselect(
        "💪 Difficulty Level",
        ["Easy", "Medium", "Hard", "Expert"],
        default=["Easy", "Medium"]
    )
    
    st.markdown("**📏 Distance Range (km)**")
    min_dist, max_dist = st.slider("", min_value=1, max_value=100, value=(5, 20))
    
    num_trails = st.selectbox("🔢 Number of Trails", [3, 5, 10], index=1)
    
    st.markdown("---")
    st.markdown("### 🌿 Trail Features")
    pet_friendly = st.checkbox("🐕 Pet Friendly")
    family_friendly = st.checkbox("👨‍👩‍👧 Family Friendly")
    wheelchair = st.checkbox("♿ Wheelchair Accessible")
    
    st.markdown("---")
    st.markdown("### 🏞️ Scenery")
    scenery = st.multiselect(
        "What do you want to see?",
        ["Ocean Views", "Waterfalls", "Forest", "Mountains", "Wildlife", "Lakes", "Canyons"],
        default=["Forest", "Wildlife"]
    )
    
    season = st.selectbox(
        "📅 Season",
        ["Summer", "Autumn", "Winter", "Spring"]
    )
    
    st.markdown("---")
    find_button = st.button("🔍 Find My Perfect Trails!")

if find_button:
    if not location:
        st.warning("⚠️ Please enter a location to search!")
    elif not difficulty:
        st.warning("⚠️ Please select at least one difficulty level!")
    else:
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)
        
        filters = []
        if pet_friendly: filters.append("pet friendly")
        if family_friendly: filters.append("family friendly")
        if wheelchair: filters.append("wheelchair accessible")
        
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

Make sure trails are real, accurate and match the season {season}.
Be enthusiastic, detailed and helpful like a local expert!
""")
        
        chain = prompt | llm
        
        with st.spinner("🔍 Finding the best trails for you..."):
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
        
        st.success(f"✅ Found {num_trails} amazing trails in {location}!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📍 Location", location)
        with col2:
            st.metric("📏 Distance", f"{min_dist}-{max_dist} km")
        with col3:
            st.metric("💪 Difficulty", difficulty_text)
        with col4:
            st.metric("🔢 Trails Found", num_trails)
        
        st.markdown("---")
        
        st.markdown(f'<div class="trail-card">{response.content}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class="safety-box">
        <h3>⚠️ Safety Reminders</h3>
        <ul>
            <li>Always check weather before heading out</li>
            <li>Tell someone where you're going and when you'll be back</li>
            <li>Bring more water than you think you need</li>
            <li>Download offline maps before your hike</li>
            <li>Fully charge your phone and bring a power bank</li>
            <li>Always carry a basic first aid kit</li>
            <li>Wear appropriate footwear for the terrain</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h2>🌍</h2>
            <h3>Worldwide Trails</h3>
            <p style="color: #a0aec0">Search any location on Earth</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h2>🤖</h2>
            <h3>AI Powered</h3>
            <p style="color: #a0aec0">Smart recommendations just for you</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h2>🎯</h2>
            <h3>Personalized</h3>
            <p style="color: #a0aec0">Tailored to your preferences</p>
        </div>
        """, unsafe_allow_html=True)