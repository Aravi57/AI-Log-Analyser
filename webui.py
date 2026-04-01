import streamlit as st

from analyser import analyze_log


def main():
    st.title("AI Log Analyser")
    
    # Settings button in header
    with st.container():
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("⚙️ Settings", key="settings_btn"):
                st.session_state.show_settings = not st.session_state.get("show_settings", False)
    
    # Settings modal
    if st.session_state.get("show_settings", False):
        with st.expander("Settings", expanded=True):
            api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
            base_url = st.text_input("Base URL", value=st.session_state.get("base_url", "https://api.openai.com/v1"))
            model = st.text_input("Model", value=st.session_state.get("model", "gpt-4o-mini"))
            
            # Save settings to session state
            st.session_state.api_key = api_key
            st.session_state.base_url = base_url
            st.session_state.model = model
            
            if st.button("Close Settings"):
                st.session_state.show_settings = False
                st.rerun()
    else:
        # Load settings from session state
        api_key = st.session_state.get("api_key", "")
        base_url = st.session_state.get("base_url", "https://api.openai.com/v1")
        model = st.session_state.get("model", "gpt-4o-mini")
    
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
