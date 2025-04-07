from openai import OpenAI
from agents.env_loader import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class GPTAnswerAgent:
    def generate_answer(self, question, contexts):
        context = "\n".join(contexts)
        prompt = f"""Answer the question based on the following tariff data:\n\n{context}\n\nQ: {question}\nA:"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a U.S. trade tariff expert. Reply only in plain text."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
