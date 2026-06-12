import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Claude Demo App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Claude_AI_logo.svg/1200px-Claude_AI_logo.svg.png", width=80)
st.sidebar.title("Claude Demo App")
st.sidebar.markdown("Built & deployed via **Claude** 🤖")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📈 Charts", "🎲 Random Data", "ℹ️ About"])

# ── Helpers ───────────────────────────────────────────────────────────────────
def make_timeseries(days=30, base=100, noise=15):
    dates = [datetime.today() - timedelta(days=i) for i in range(days)][::-1]
    values = [base + noise * np.sin(i / 3) + random.gauss(0, noise / 3) for i in range(days)]
    return pd.DataFrame({"Date": dates, "Value": values})

# ── Pages ─────────────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.title("📊 Dashboard")
    st.markdown("Welcome to your **Claude-deployed Streamlit app**! This was pushed to GitHub and deployed in minutes.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Users", "1,284", "+12%")
    col2.metric("Revenue", "$8,420", "+5.3%")
    col3.metric("Uptime", "99.9%", "+0.1%")
    col4.metric("Requests", "42.1k", "-2%")

    st.markdown("---")

    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Daily Active Users")
        df = make_timeseries(30, base=1200, noise=200)
        fig = px.area(df, x="Date", y="Value", color_discrete_sequence=["#6C63FF"])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=280, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("Revenue (30d)")
        df2 = make_timeseries(30, base=8000, noise=1500)
        fig2 = px.bar(df2, x="Date", y="Value", color_discrete_sequence=["#FF6584"])
        fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=280, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

elif page == "📈 Charts":
    st.title("📈 Interactive Charts")

    chart_type = st.selectbox("Chart type", ["Line", "Scatter", "Histogram", "Pie"])
    n = st.slider("Data points", 20, 200, 60)

    np.random.seed(42)
    df = pd.DataFrame({
        "x": np.linspace(0, 10, n),
        "y": np.sin(np.linspace(0, 10, n)) * 50 + np.random.normal(0, 5, n) + 50,
        "category": np.random.choice(["A", "B", "C"], n),
        "size": np.random.uniform(5, 25, n),
    })

    if chart_type == "Line":
        fig = px.line(df, x="x", y="y", color="category", title="Line Chart")
    elif chart_type == "Scatter":
        fig = px.scatter(df, x="x", y="y", color="category", size="size", title="Scatter Plot")
    elif chart_type == "Histogram":
        fig = px.histogram(df, x="y", color="category", nbins=20, title="Histogram")
    else:
        counts = df["category"].value_counts().reset_index()
        counts.columns = ["category", "count"]
        fig = px.pie(counts, names="category", values="count", title="Pie Chart")

    st.plotly_chart(fig, use_container_width=True)

elif page == "🎲 Random Data":
    st.title("🎲 Random Data Generator")
    st.markdown("Generate a random dataset and explore it.")

    col1, col2 = st.columns(2)
    rows = col1.number_input("Rows", 10, 500, 50)
    cols_n = col2.number_input("Columns", 2, 8, 4)

    if st.button("🎲 Generate", type="primary"):
        data = {
            f"Col_{chr(65+i)}": np.round(np.random.randn(rows) * 100, 2)
            for i in range(cols_n)
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        st.subheader("Summary Statistics")
        st.dataframe(df.describe().round(2), use_container_width=True)

        st.subheader("Correlation Heatmap")
        corr = df.corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Hit Generate to create a dataset!")

elif page == "ℹ️ About":
    st.title("ℹ️ About This App")
    st.markdown("""
    ### How this app was created

    This entire app — including the code, GitHub repo, and deployment setup —
    was created by **Claude** in a single conversation.

    **Stack:**
    - 🐍 Python + Streamlit
    - 📊 Plotly for charts
    - 🐙 GitHub (auto-deployed via Claude)
    - ☁️ Streamlit Cloud (free hosting)

    **Deploy your own:**
    1. Fork this repo
    2. Go to [share.streamlit.io](https://share.streamlit.io)
    3. Connect your GitHub and deploy!

    ---
    Made with ❤️ by Claude × Jugal
    """)
