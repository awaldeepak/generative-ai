from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


user_question = input("👨‍💼")

engineer_persona = """
    You are a senior software engineer specializing in Python. 
    Your tone is technical, concise, and you focus on practical, actionable advice. 
    You prioritize best practices, performance, and code quality. 
    Avoid conversational pleasantries.
"""

counselor_persona = """
    You are a friendly and encouraging career counselor. 
    Your tone is warm, supportive, and motivating. 
    You focus on career development, learning strategies, and long-term goals. 
    Offer encouragement and a positive outlook.
"""


def get_persona_response(user_query, persona_role):
    system_message = {
        "role": "system",
        "content": persona_role
    }
    
    user_message = {
        "role": "user",
        "content": user_query
    }
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_message, user_message],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


engineer_response = get_persona_response(user_question, engineer_persona)
counselor_response = get_persona_response(user_question, counselor_persona)


print("--- Engineer's Response ---")
print(engineer_response)
print("\n--- Counselor's Response ---")
print(counselor_response)
