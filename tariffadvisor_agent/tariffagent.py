import pandas as pd
from agents.retriever import RetrieverAgent
from agents.gpt_answer import GPTAnswerAgent
import os

def clean_tariff_data(file_path):
    #Get the absolute path relative to this script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)

    df = pd.read_csv(full_path)
    df["TariffsCharged2USA"] = df["TariffsCharged2USA"].str.replace('%', '').astype(float)
    df["USAReciprocalTariffs"] = df["USAReciprocalTariffs"].str.replace('%', '').astype(float)
    return df

class TariffAgent:
    def __init__(self, data_source):
        self.data = clean_tariff_data(data_source)
        self.retriever = RetrieverAgent()
        self.gpt_agent = GPTAnswerAgent()

    def get_country_list(self):
        countries = sorted(self.data["Country"].dropna().unique().tolist())
        return ["All Countries"] + countries

    def get_data_by_country(self, countries):
        if "All Countries" in countries:
            return self.data
        return self.data[self.data["Country"].isin(countries)]

    def get_tariff_by_country(self, countries):
        if "All Countries" in countries or len(countries) > 1:
            return "_Showing data for multiple countries._"
        row = self.get_data_by_country(countries)
        if not row.empty:
            row = row.iloc[0]
            return (
                f"**📍 {row['Country']}**  \n"
                f"🔺 **Tariffs Charged to U.S.A.:** {row['TariffsCharged2USA']}%  \n"
                f"🔻 **U.S. Reciprocal Tariffs:** {row['USAReciprocalTariffs']}%"
            )
        return f"No data found for {countries[0]}."

    def answer_question(self, question):
        context_chunks = self.retriever.retrieve_context(question)
        return self.gpt_agent.generate_answer(question, context_chunks)
