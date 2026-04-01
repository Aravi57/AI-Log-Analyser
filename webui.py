import streamlit as st

from analyser import analyze_log


def main():
    st.title("AI Log Analyser")
    
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("OpenAI API Key", type="password")
        base_url = st.text_input("Base URL", value="https://api.openai.com/v1")
        model = st.selectbox("Model", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"], index=0)
    
    st.write("Input log")

    log_input = st.text_area("Input log", height=220, label_visibility="collapsed")

    if st.button("Analyze"):
        if not log_input.strip():
            st.warning("Please enter a log before analyzing.")
            return

        try:
            with st.spinner("Analyzing log..."):
                result = analyze_log(log_input.strip(), api_key if api_key else None, base_url if base_url else None, model)
            st.subheader("Response")
            st.write(result)
        except Exception as exc:
            st.error(f"Error: {exc}")


if __name__ == "__main__":
    main()
