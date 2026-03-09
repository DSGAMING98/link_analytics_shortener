import html
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from db import init_db, create_link, get_link_by_code, increment_click, get_all_links
from utils import normalize_url, is_valid_url, generate_short_code, build_short_url

st.set_page_config(
    page_title="Link Analytics Shortener",
    page_icon="🔗",
    layout="wide"
)

init_db()

# IMPORTANT:
# After deployment, replace this with your REAL deployed Streamlit app URL
DEPLOYED_BASE_URL = "https://YOUR-REAL-APP-NAME.streamlit.app"


def redirect_page(target_url: str):
    safe_url = html.escape(target_url, quote=True)

    redirect_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url={safe_url}">
        <script>
            window.open("{safe_url}", "_top");
        </script>
        <title>Redirecting...</title>
    </head>
    <body>
        <p>Redirecting...</p>
        <p>If you are not redirected, <a href="{safe_url}" target="_top">click here</a>.</p>
    </body>
    </html>
    """
    components.html(redirect_html, height=120)


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
        redirect_page(target_url)
        st.stop()
    else:
        st.error("Invalid short URL.")
        st.stop()


# -----------------------------
# MAIN APP
# -----------------------------
st.title("🔗 Link Analytics Shortener")
st.write("Shorten any valid URL and track clicks.")

st.caption(f"Configured deployed app URL: {DEPLOYED_BASE_URL}")

with st.form("shortener_form", clear_on_submit=True):
    original_url_input = st.text_input(
        "Enter long URL",
        placeholder="https://youtube.com/watch?v=... or https://amazon.in/..."
    )
    submitted = st.form_submit_button("Generate Short URL")

if submitted:
    original_url = normalize_url(original_url_input)

    if not DEPLOYED_BASE_URL.strip():
        st.error("Deployed base URL is missing.")
    elif "localhost" in DEPLOYED_BASE_URL.lower() or "127.0.0.1" in DEPLOYED_BASE_URL.lower():
        st.error("Localhost is not allowed.")
    elif not original_url_input.strip():
        st.error("URL cannot be empty.")
    elif not is_valid_url(original_url):
        st.error("Please enter a valid URL.")
    else:
        short_code = generate_short_code()
        create_link(original_url, short_code)
        short_url = build_short_url(DEPLOYED_BASE_URL, short_code)

        st.success("Short URL created successfully!")
        st.code(short_url, language=None)
        st.markdown(f'<a href="{short_url}" target="_top">Open Short URL</a>', unsafe_allow_html=True)

st.subheader("Dashboard")

rows = get_all_links()
if rows:
    data = []
    for row in rows:
        short_url = build_short_url(DEPLOYED_BASE_URL, row["short_code"])
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
