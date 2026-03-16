import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are the AI Content Strategist for YouTube InsightX. 
Your goal is to help creators and analysts understand YouTube trends and develop viral content strategies.
You have access to real-time analytics data (provided in context).
Be professional, insightful, and creative. Suggest specific video ideas, hook improvements, and niche opportunities.
"""

def get_ai_response(user_query, context_data=None):
    """Generic function to get a response from Groq AI."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    if context_data:
        messages.append({
            "role": "system", 
            "content": f"Current Trending/Search Data Context: {context_data}"
        })
        
    messages.append({"role": "user", "content": user_query})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI Strategist: {str(e)}"

def analyze_trends(df):
    """Specifically analyze the provided dataframe for trends."""
    if df.empty:
        return "No data available to analyze. Please fetch some videos first."
        
    # Create a concise summary for the AI
    top_videos = df.nlargest(5, 'view_count')[['title', 'view_count', 'engagement_rate']].to_dict(orient='records')
    context = f"Top 5 videos currently: {top_videos}"
    
    query = "Based on this data, what are the current trending topics and what kind of videos should creators make next to go viral?"
    
    return get_ai_response(query, context)
