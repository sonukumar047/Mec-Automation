import streamlit as st
import requests
import os
import json
import re

# Constants
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

# Language-based system prompts
LANGUAGE_SYSTEM_PROMPTS = {
    "Python": """
You are an expert in Siemens NX CAD automation. Based on the user's input, generate Python code using the NX Open API to automate tasks such as creating holes, extrusions, and sketches in Siemens NX. Add comments in the code. Provide complete, runnable Python scripts. Respond ONLY with code, nothing else.
""",
    "C++": """
You are an expert in Siemens NX CAD automation. Based on the user's input, generate C++ code using the NX Open API to automate tasks such as creating holes, extrusions, and sketches in Siemens NX. Add comments in the code. Provide complete, compilable C++ code. Respond ONLY with code, nothing else.
""",
    "VB": """
You are an expert in Siemens NX CAD automation. Based on the user's input, generate Visual Basic code using the NX Open API to automate tasks such as creating holes, extrusions, and sketches in Siemens NX. Add comments in the code. Provide complete, runnable VB.NET code. Respond ONLY with code, nothing else.
"""
}

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Streamlit UI
st.title("🔧 NX CAD Automation Chatbot")
st.markdown("### Enter your CAD automation prompt and get NX Open API code!")

# Language selection
language = st.selectbox("Choose NX Open API Language:", ["Python", "C++", "VB"], index=0)
SYSTEM_PROMPT = LANGUAGE_SYSTEM_PROMPTS[language]

# Example prompts
example_prompts = [
    "Create a block of 100x50x25 mm and drill a hole of 10 mm diameter at the center top face.",
    "Make a cylinder of 30 mm diameter and 40 mm height along Z-axis.",
    "Create a rectangular pocket of 50x30 mm on the top face.",
    "Add 4 holes of 5 mm diameter at the corners of a 60x60 mm square plate."
]

with st.expander("Example prompts (click to insert)"):
    for example in example_prompts:
        if st.button(example, key=example):
            st.session_state.user_input = example

# User prompt input
user_input = st.text_area("Your CAD prompt:", value=st.session_state.user_input, height=150)

# Call to LLM
def call_llama(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        for line in reversed(lines):
            try:
                data = json.loads(line)
                content = data.get("message", {}).get("content", "")
                if content:
                    return extract_code_block(content)
            except json.JSONDecodeError:
                continue
        return "⚠️ Error: No valid code found in response."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Extract code from markdown
def extract_code_block(text):
    # Extract content inside triple backticks (optionally with language label)
    match = re.search(r"```(?:\w+)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

# Save code to file
def save_code_to_file(code, filename="nx_automation.py"):
    with open(filename, "w") as f:
        f.write(code)

# Generate button
if st.button("Generate NX Code"):
    if not user_input.strip():
        st.warning("Please enter a prompt to generate code.")
    else:
        with st.spinner("Generating code..."):
            result = call_llama(user_input)
            st.session_state.history.append((user_input, result, language))
            st.session_state.user_input = ""  # Clear input

# Show history
if st.session_state.history:
    st.markdown("### Conversation History:")
    for i, (prompt, code, lang) in enumerate(reversed(st.session_state.history)):
        idx = len(st.session_state.history) - i
        display_lang = lang.lower() if lang != "VB" else "vbnet"
        st.markdown(f"**Prompt {idx} ({lang}):** {prompt}")
        st.code(code, language=display_lang)
        st.download_button(
            label=f"📥 Download code {idx}",
            data=code,
            file_name=f"nx_automation_{idx}_{lang.lower()}.txt",
            mime="text/plain",
            key=f"download_{i}"
        )

# Optional: Show sample dataset
if st.checkbox("Show sample dataset prompts for inspiration"):
    try:
        with open("nx_open_sample_dataset.json", "r") as f:
            data = json.load(f)
        st.json(data)
    except Exception as e:
        st.error(f"Could not load dataset: {e}")
