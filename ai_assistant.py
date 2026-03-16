from groq import Groq
import pandas as pd
import json

class InsightXAI:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        self.system_prompt = """
        You are 'InsightX AI', a professional YouTube Content Strategist and Trend Analyst. 
        Your goal is to help creators grow by analyzing real-time data and suggesting actionable strategies.
        
        Guidelines:
        1. Base your advice on the 'Real-time Context' provided (video titles, views, stats).
        2. Be creative with video ideas, titles, and hooks.
        3. Suggest specific niches or 'micro-niches' that are currently underserved.
        4. Focus on engagement metrics and virality factors.
        5. Keep responses concise, professional, and encouraging.
        """

    def get_ai_response(self, user_query, context_df):
        """
        Generates a response based on user query and the current dashboard data.
        """
        try:
            # Prepare context
            if context_df is not None and not context_df.empty:
                # Top 10 videos as context
                top_videos = context_df.sort_values("views", ascending=False).head(10)
                context_str = "REAL-TIME TRENDING DATA CONTEXT:\n"
                for i, row in top_videos.iterrows():
                    context_str += f"- Video: {row['title']} | Channel: {row['channel_title']} | Views: {row['views']} | Likes: {row['likes']}\n"
            else:
                context_str = "No real-time data currently available. Advise based on general YouTube best practices."

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{context_str}\n\nUSER QUESTION: {user_query}"}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to AI Strategist (Groq): {str(e)}"

    def suggest_initial_topics(self, context_df):
        """
        Provides 3-4 trending topic ideas based on data.
        """
        query = "Based on the trending videos, what are 3 specific, viral content ideas for a new creator?"
        return self.get_ai_response(query, context_df)
