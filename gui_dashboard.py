import streamlit as st

def display_logs():
    st.title("📜 Voice-Git Automation Logs")
    if not open("logs/commands.txt", "a"):
        with open("logs/commands.txt", "w"): pass
    with open("logs/commands.txt", "r") as f:
        st.text(f.read())

if __name__ == "__main__":
    display_logs()
