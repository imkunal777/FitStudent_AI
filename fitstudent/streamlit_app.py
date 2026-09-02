"""
streamlit_app.py – Streamlit Cloud entry point for FitStudent AI.

Streamlit Cloud only runs Streamlit apps directly.  This file:
  1. Starts the Flask app in a background daemon thread (no reloader,
     no signal handling – both of which crash inside Streamlit's worker).
  2. Renders a full-screen iframe so the user sees and uses the Flask UI.

The Flask server listens on 127.0.0.1:5000 (localhost-only), which is
perfectly accessible from the same Streamlit Cloud container.
"""

import threading
import streamlit as st
import streamlit.components.v1 as components

FLASK_PORT = 5000


def _run_flask():
    """Start Flask's built-in server in the background thread.

    use_reloader=False  – reloader tries to fork/exec; forbidden in threads.
    threaded=True       – allow Flask to handle concurrent requests.
    debug=False         – debug mode re-registers SIGTERM; forbidden in threads.
    """
    from app import app  # imports create_app() result from app.py
    app.run(host="127.0.0.1", port=FLASK_PORT,
            debug=False, use_reloader=False, threaded=True)


# Start Flask exactly once per Streamlit session process
if "flask_started" not in st.session_state:
    t = threading.Thread(target=_run_flask, daemon=True)
    t.start()
    st.session_state["flask_started"] = True

# ── Streamlit UI ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FitStudent AI",
    page_icon="💪",
    layout="wide",
)

# Hide Streamlit's own chrome so the Flask UI fills the whole window
st.markdown(
    """
    <style>
      #MainMenu, header, footer { visibility: hidden; }
      .block-container { padding: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

components.iframe(f"http://127.0.0.1:{FLASK_PORT}/", height=900, scrolling=True)
