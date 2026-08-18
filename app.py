import streamlit as st
from agents.pipeline import run_pipeline

st.set_page_config(
    page_title="BlogGPT",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 BlogGPT")

topic = st.text_input(
    "Topic",
    placeholder="Write a blog about BERT Transformers"
)

if st.button("Generate"):

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Generating content..."):

        result = run_pipeline(topic)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "SEO",
        "Outline",
        "Blog",
        "FAQ",
        "LinkedIn",
        "Newsletter"
    ])

    with tab1:
        st.markdown(result["SEO"])

    with tab2:
        st.markdown(result["Outline"])

    with tab3:
        st.markdown(result["Blog"])

        st.download_button(
            "Download Blog",
            result["Blog"],
            "blog.md"
        )

    with tab4:
        st.markdown(result["FAQ"])

    with tab5:
        st.markdown(result["LinkedIn"])

    with tab6:
        st.markdown(result["Newsletter"])
