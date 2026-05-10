import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)

prompt = ChatPromptTemplate.from_template("""
You are an expert hiking trail recommender. 
Based on the user's preferences, suggest 5-10 most suitable hiking trails.

For each trail provide:
- Trail Name
- Location
- Distance (km)
- Difficulty (Easy/Medium/Hard)
- Estimated time
- What makes it special

User preferences:
- Location/Region: {location}
- Difficulty: {difficulty}
- Desired distance: {distance} km

Give practical, real hiking trails. Be enthusiastic and helpful!
""")

chain = prompt | llm

def get_recommendations(location, difficulty, distance):
    response = chain.invoke({
        "location": location,
        "difficulty": difficulty,
        "distance": distance
    })
    return response.content

def main():
    print("🥾 Hiking Trail Recommender")
    print("=" * 40)
    
    location = input("Where do you want to hike? (city/region/country): ").strip()
    difficulty = input("Difficulty level (easy/medium/hard): ").strip()
    distance = input("How many km do you want to walk?: ").strip()
    
    print("\n🔍 Finding trails for you...\n")
    
    result = get_recommendations(location, difficulty, distance)
    print(result)
    
    print("\n" + "=" * 40)
    another = input("Want another recommendation? (yes/no): ").strip().lower()
    
    while another == "yes":
        location = input("Where do you want to hike?: ").strip()
        difficulty = input("Difficulty level (easy/medium/hard): ").strip()
        distance = input("How many km do you want to walk?: ").strip()
        
        print("\n🔍 Finding trails for you...\n")
        result = get_recommendations(location, difficulty, distance)
        print(result)
        
        print("\n" + "=" * 40)
        another = input("Want another recommendation? (yes/no): ").strip().lower()
    
    print("\nHappy hiking! 🏔️")

if __name__ == "__main__":
    main()