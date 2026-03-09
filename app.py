import html
import time

import pandas as pd
import streamlit as st

from db import init_db, create_link, get_link_by_code, increment_click, get_all_links
from utils import normalize_url, is_valid_url, generate_short_code, build_short_url

st.set_page_config(
    page_title="Link Analytics Shortener",
    page_icon="🔗",
    layout="wide"
)

init_db()


def get_base_url() -> str:
    """
    On Streamlit Cloud / deployed env, this gets the real app URL.
    If it cannot detect it, user must manually provide the deployed URL.
    """
    try:
        headers = st.context.headers
        host = headers.get("host", "")
        proto = headers.get("x-forwarded-proto", "https")

        if host:
            return f"{proto}://{host}"
    except Exception:
        pass

    return ""


# -----------------------------
# REDIRECT MODE
# -----------------------------
query_params = st.query_params
incoming_code = query_params.get("code")

if incoming_code:
    row = get_link_by_code(incoming_code)

    if row:
        increment_click(incoming_code)
        target_url = row["original_url"]
        safe_url = html.escape(target_url, quote=True)

        st.markdown("## Redirecting...")
        st.caption("If redirect does not happen automatically, click the link below.")

        st.markdown(
            f"""
            <meta http-equiv="refresh" content="0; url={safe_url}">
            <script>
                window.location.href = "{safe_url}";
            </script>
            <a href="{safe_url}" target="_self">Click here to continue</a>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.2)
        st.stop()
    else:
        st.error("Invalid short URL.")
        st.stop()


# -----------------------------
# MAIN APP
# -----------------------------
st.title("🔗 Link Analytics Shortener")
st.write("Paste a long URL, generate a short link, and track click analytics.")

detected_base_url = get_base_url()

base_url = st.text_input(
    "Deployed App Base URL",
    value=detected_base_url,
    placeholder="https://your-real-app-name.streamlit.app",
    help="Enter your deployed Streamlit app URL. Do not use localhost."
)

st.subheader("Create Short URL")

with st.form("shortener_form", clear_on_submit=True):
    original_url_input = st.text_input(
        "Enter original URL",
        placeholder="https://google.com or youtube.com/watch?v=..."
    )
    submitted = st.form_submit_button("Generate Short URL")

if submitted:
    original_url = normalize_url(original_url_input)

    if not base_url.strip():
        st.error("Please enter your deployed app URL. Localhost is not allowed.")
    elif "localhost" in base_url.lower() or "127.0.0.1" in base_url.lower():
        st.error("Localhost links are not allowed. Use your deployed Streamlit app URL.")
    elif not original_url_input.strip():
        st.error("URL cannot be empty.")
    elif not is_valid_url(original_url):
        st.error("Please enter a valid original URL.")
    else:
        short_code = generate_short_code()
        create_link(original_url, short_code)
        short_url = build_short_url(base_url, short_code)

        st.success("Short URL created successfully!")
        st.code(short_url, language=None)
        st.markdown(f"[Open Short URL]({short_url})")

st.subheader("Dashboard")

rows = get_all_links()

if rows:
    data = []
    for row in rows:
        short_url = build_short_url(base_url, row["short_code"]) if base_url else f"?code={row['short_code']}"
        data.append({
            "Original URL": row["original_url"],
            "Short URL": short_url,
            "Clicks": row["click_count"],
            "Created At": row["created_at"]
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No links created yet.")