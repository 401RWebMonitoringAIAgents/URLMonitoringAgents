# import streamlit as st
# import json
# from utils.auth import Auth
# from config_file import Config

# from strands import Agent
# from strands.models import BedrockModel

# import tools.list_appointments
# import tools.update_appointment
# import tools.create_appointment
# from strands_tools import calculator, current_time

# # Initialize session state for conversation history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ID of Secrets Manager containing cognito parameters
# secrets_manager_id = Config.SECRETS_MANAGER_ID

# # ID of the AWS region in which Secrets Manager is deployed
# region = Config.DEPLOYMENT_REGION

# if Config.ENABLE_AUTH:
#     # Initialise CognitoAuthenticator
#     authenticator = Auth.get_authenticator(secrets_manager_id, region)

#     # Authenticate user, and stop here if not logged in
#     is_logged_in = authenticator.login()
#     if not is_logged_in:
#         st.stop()

#     def logout():
#         authenticator.logout()

#     with st.sidebar:
#         st.text(f"Welcome,\n{authenticator.get_username()}")
#         st.button("Logout", "logout_btn", on_click=logout)

# # Add title on the page
# st.title("Streamlit Strands Demo")
# st.write("This demo shows how to use Strands to create a personal assistant that can manage appointments and calendar. It also has a calculator tool.")

# # Define agent
# system_prompt = """You are a helpful personal assistant that specializes in managing my appointments and calendar. 
# You have access to appointment management tools, a calculator, and can check the current time to help me organize my schedule effectively. 
# Always provide the appointment id so that I can update it if required"""

# model = BedrockModel(
#     model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
#     max_tokens=64000,
#     additional_request_fields={
#         "thinking": {
#             "type": "disabled",
#         }
#     },
# )

# # Initialize the agent
# if "agent" not in st.session_state:
#     st.session_state.agent = Agent(
#         model=model,
#         system_prompt=system_prompt,
#         tools=[
#             current_time,
#             calculator,
#             tools.create_appointment,
#             tools.list_appointments,
#             tools.update_appointment,
#         ],
#     )

# # Keep track of the number of previous messages in the agent flow
# if "start_index" not in st.session_state:
#     st.session_state.start_index = 0

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.empty()  # This forces the container to render without adding visible content (workaround for streamlit bug)
#         st.markdown(message["content"])

# # Chat input
# if prompt := st.chat_input("Ask your agent..."):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Clear previous tool usage details
#     if "details_placeholder" in st.session_state:
#         st.session_state.details_placeholder.empty()
    
#     # Display user message
#     with st.chat_message("user"):
#         st.write(prompt)
    
#     # Get response from agent
#     with st.spinner("Thinking..."):
#         response = st.session_state.agent(prompt)
    
#     # Extract the assistant's response text
#     assistant_response = ""
#     for m in st.session_state.agent.messages:
#         if m.get("role") == "assistant" and m.get("content"):
#             for content_item in m.get("content", []):
#                 if "text" in content_item:
#                     # We keep only the last response of the assistant
#                     assistant_response = content_item["text"]
#                     break
    
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
#     # Display assistant response
#     with st.chat_message("assistant"):
        
#         start_index = st.session_state.start_index      

#         # Display last messages from agent, with tool usage detail if any
#         st.session_state.details_placeholder = st.empty()  # Create a new placeholder
#         with st.session_state.details_placeholder.container():
#             for m in st.session_state.agent.messages[start_index:]:
#                 if m.get("role") == "assistant":
#                     for content_item in m.get("content", []):
#                         if "text" in content_item:
#                             st.write(content_item["text"])
#                         elif "toolUse" in content_item:
#                             tool_use = content_item["toolUse"]
#                             tool_name = tool_use.get("name", "")
#                             tool_input = tool_use.get("input", {})
#                             st.info(f"Using tool: {tool_name}")
#                             st.code(json.dumps(tool_input, indent=2))
            
#                 elif m.get("role") == "user":
#                     for content_item in m.get("content", []):
#                         if "toolResult" in content_item:
#                             tool_result = content_item["toolResult"]
#                             st.info(f"Tool Result: {tool_result.get('status', '')}")
#                             for result_content in tool_result.get("content", []):
#                                 if "text" in result_content:
#                                     st.code(result_content["text"])

#         # Update the number of previous messages
#         st.session_state.start_index = len(st.session_state.agent.messages)
    

import streamlit as st
from datetime import date

# =====================================================
# TODO: later, import real backend functions here
# from backend import get_today_updates, generate_daily_report, run_graph
# =====================================================

# --------- Mock backend functions for now --------- #
def get_today_updates_mock():
    # demo data 
    return [
        {
            "name": "Machine Learning Summit 2026",
            "status": "Registration opened",
            "date": "2026-03-10",
            "source": "Website",
        },
        {
            "name": "Cloud Expo",
            "status": "Date changed",
            "date": "2026-04-02",
            "source": "Email",
        },
        {
            "name": "Data Science Workshop",
            "status": "Registration closes in 2 days",
            "date": "2026-03-01",
            "source": "Website",
        },
    ]


def generate_daily_report_mock(events):
    lines = [f"Daily Event Update Report – {date.today()}"]
    lines.append("-" * 40)
    for e in events:
        lines.append(f"{e['name']}: {e['status']} (Date: {e['date']}, Source: {e['source']})")
    return "\n".join(lines)


def run_graph_mock(user_input: str) -> str:
    # Placeholder for later multi-agent backend
    return "This is where the assistant’s response will go once the backend is connected."


# =====================================================
# Streamlit UI
# =====================================================

st.set_page_config(page_title="Event Monitoring Dashboard", layout="wide")

# Initialize session state
if "events" not in st.session_state:
    st.session_state.events = []
if "report_text" not in st.session_state:
    st.session_state.report_text = ""


# ----------------- Header ----------------- #
st.title("Event Monitoring Dashboard")
st.caption(
    "Automatically track updates from known event websites and related emails. "
    "View registration openings, closings, date changes, and daily summaries in one place."
)

st.markdown("---")

# ----------------- Sidebar ----------------- #
st.sidebar.header("Configuration")

st.sidebar.subheader("Report settings")
report_email = st.sidebar.text_input("Report email (for future integration)", value="you@example.com")
frequency = st.sidebar.selectbox("Report frequency", ["Daily", "Weekly"])
st.sidebar.caption("These settings will be used when the email feature is implemented.")

st.sidebar.subheader("Filters (UI only for now)")
source_filter = st.sidebar.multiselect(
    "Source",
    options=["Website", "Email"],
    default=["Website", "Email"],
)
status_filter = st.sidebar.multiselect(
    "Status type",
    options=["Registration opened", "Registration closed", "Date changed", "Registration closes soon"],
    default=["Registration opened", "Date changed", "Registration closes soon"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Backend integration will replace mock functions in app.py.")


# ----------------- Main Layout ----------------- #
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Today’s event updates")

    if st.button("Refresh updates"):
        # TODO: replace with real backend:
        # st.session_state.events = get_today_updates()
        st.session_state.events = get_today_updates_mock()
        st.success("Updates refreshed (mock data).")

    events = st.session_state.events

    if not events:
        st.info("No updates yet. Click 'Refresh updates' to load event changes.")
    else:
        # Apply simple UI filters (mock)
        filtered = []
        for e in events:
            if source_filter and e["source"] not in source_filter:
                continue
            if status_filter:
                # do a simple 'contains' match
                if not any(s.lower() in e["status"].lower() for s in status_filter):
                    continue
            filtered.append(e)

        if not filtered:
            st.warning("No events match the current filters.")
        else:
            for e in filtered:
                with st.container(border=True):
                    st.markdown(f"**{e['name']}**")
                    st.markdown(f"- Status: {e['status']}")
                    st.markdown(f"- Event date: {e['date']}")
                    st.markdown(f"- Source: {e['source']}")

with col2:
    st.subheader("Summary (mock)")

    events = st.session_state.events
    if events:
        total = len(events)
        opened = sum("opened" in e["status"].lower() for e in events)
        changed = sum("changed" in e["status"].lower() for e in events)
        closing = sum("closes" in e["status"].lower() for e in events)

        st.metric("Total updates", total)
        st.metric("New registrations", opened)
        st.metric("Date changes", changed)
        st.metric("Closing soon", closing)
    else:
        st.write("Summary will appear here after updates are loaded.")

    st.markdown("---")
    st.subheader("Daily report preview")

    if events:
        # TODO: replace with real backend.generate_daily_report(events)
        st.session_state.report_text = generate_daily_report_mock(events)
        st.text_area("Report text", st.session_state.report_text, height=200)
    else:
        st.write("Report will appear here after you refresh updates.")


st.markdown("---")

# ----------------- Assistant Section (future hook to multi-agent backend) ----------------- #
st.subheader("Ask the event assistant (coming soon)")

st.caption(
    "This section will be connected to a multi-agent backend. "
    "For now, it uses a simple placeholder response."
)

user_query = st.chat_input("Ask about events, schedules, or updates...")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)

    # TODO: later call real backend.run_graph(user_query)
    answer = run_graph_mock(user_query)

    with st.chat_message("assistant"):
        st.write(answer)


# ----------------- Footer ----------------- #
st.markdown("---")
st.caption(
    "UI prototype for event monitoring. "
    "Backend integration points are marked with TODO comments in app.py."
)
