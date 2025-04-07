
import streamlit as st
import altair as alt
from datetime import datetime
from streamlit.components.v1 import html

# 📘 Summary section
def render_summary(country):
    st.subheader("📘 Tariff Policy Summary")
    st.markdown(f"""
The USA administration imposed tariffs on many countries.  
You are currently viewing insights for **{country.title()}**.
""")

# 📌 Tariff Info
def render_tariff_info(agent, countries):
    st.subheader("📌 Tariff Info")
    st.markdown(agent.get_tariff_by_country(countries))

# 📊 Tariffs Charged to U.S.A.
def render_top_tariffs_chart(data):
    st.subheader("📊 Tariffs Charged to U.S.A.")
    if not data.empty:
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X("TariffsCharged2USA:Q", title="Tariff to U.S.A. (%)"),
            y=alt.Y("Country:N", sort='-x'),
            tooltip=["Country", "TariffsCharged2USA"]
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No data to display.")

# 🟦 Reciprocal Tariffs Chart
def render_top_reciprocal_tariffs_chart(data):
    st.subheader("🟦 U.S. Reciprocal Tariffs")
    if not data.empty:
        chart = alt.Chart(data).mark_bar(color="orange").encode(
            x=alt.X("USAReciprocalTariffs:Q", title="U.S. Tariff (%)"),
            y=alt.Y("Country:N", sort='-x'),
            tooltip=["Country", "USAReciprocalTariffs"]
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No data to display.")

# ⚖️ Grouped comparison chart
def render_grouped_comparison_chart(data):
    st.subheader("⚖️ Comparison: Country vs U.S.")
    if not data.empty:
        df_melt = data.melt(
            id_vars=["Country"],
            value_vars=["TariffsCharged2USA", "USAReciprocalTariffs"],
            var_name="Tariff Type",
            value_name="Value"
        )
        chart = alt.Chart(df_melt).mark_bar().encode(
            x=alt.X("Value:Q", title="Tariff (%)"),
            y=alt.Y("Country:N", sort='-x'),
            color="Tariff Type:N",
            tooltip=["Country", "Tariff Type", "Value"]
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No data to display.")

# 💬 Chat Panel
def render_chat_panel(agent):
    st.subheader("💬 Tariff Q&A")

    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    if "chat_input_key" not in st.session_state:
        st.session_state.chat_input_key = "chat_input"

    chat_html = '''
    <style>
        .chat-container {
            min-height: 200px; /* ✅ Ensures visible height even with no chats */
            max-height: 350px;
            overflow-y: auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 10px;
            background-color: #ffffff;
            font-size: 16px;
        }
        .chat-entry {
            margin-bottom: 18px;
        }
        .chat-bubble {
            padding: 12px 18px;
            border-radius: 20px;
            display: inline-block;
            max-width: 75%;
            word-wrap: break-word;
            font-size: 16px;
            line-height: 1.5;
        }
        .user-message {
            background-color: #25D366;
            color: white;
            margin-left: auto;
        }
        .agent-message {
            background-color: #e5e5ea;
            color: black;
            margin-right: auto;
        }
        .chat-label {
            font-size: 11px;
            font-weight: bold;
            color: #666;
            margin-bottom: 2px;
        }
        .chat-row-user, .chat-row-agent {
            display: flex;
            align-items: flex-end;
        }
        .chat-row-user {
            justify-content: flex-end;
        }
        .chat-row-agent {
            justify-content: flex-start;
        }
        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            margin: 0 8px;
        }
        .timestamp {
            font-size: 11px;
            color: #888;
            margin-top: 4px;
        }
    </style>
    <div class="chat-container" id="chat-scroll-box">
    '''

    for qa in st.session_state.qa_history:
        chat_html += f'''
        <div class="chat-entry chat-row-user">
            <div>
                <div class="chat-label">You</div>
                <div class="chat-bubble user-message">{qa['question']}</div>
                <div class="timestamp">{qa['timestamp']}</div>
            </div>
            <img src="https://cdn-icons-png.flaticon.com/512/1946/1946429.png" class="avatar">
        </div>
        <div class="chat-entry chat-row-agent">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" class="avatar">
            <div>
                <div class="chat-label">Agent</div>
                <div class="chat-bubble agent-message">{qa['answer']}</div>
                <div class="timestamp">{qa['timestamp']}</div>
            </div>
        </div>
        '''

    chat_html += "</div><script>var objDiv = document.getElementById('chat-scroll-box'); objDiv.scrollTop = objDiv.scrollHeight;</script>"
    html(chat_html, height=400, scrolling=False)

    question = st.text_input("Ask your question here:", key=st.session_state.chat_input_key)

    if question and (len(st.session_state.qa_history) == 0 or question != st.session_state.qa_history[-1].get("question", "")):
        try:
            answer = agent.answer_question(question.strip())
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.qa_history.append({
                "question": question.strip(),
                "answer": answer,
                "timestamp": timestamp
            })
            st.session_state.chat_input_key = "chat_input_" + datetime.now().strftime("%H%M%S%f")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
