import streamlit as st
from textblob import TextBlob
import re

# ----------------------------------------
# STEP 1: Clean the input text
# ----------------------------------------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.strip()
    return text

# ----------------------------------------
# STEP 2: Analyze sentiment using TextBlob
# TextBlob gives polarity (-1 to 1) and
# subjectivity (0 to 1)
# Polarity > 0 = Positive
# Polarity < 0 = Negative
# Polarity = 0 = Neutral
# ----------------------------------------
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        sentiment = "Positive"
        emoji = "😊"
        color = "#1D9E75"
    elif polarity < -0.1:
        sentiment = "Negative"
        emoji = "😞"
        color = "#E24B4A"
    else:
        sentiment = "Neutral"
        emoji = "😐"
        color = "#EF9F27"

    confidence = round(abs(polarity) * 100, 1)
    word_count = len(text.split())

    # Extract positive and negative keywords
    positive_words = []
    negative_words = []
    for word in text.split():
        word_clean = re.sub(r'[^a-zA-Z]', '', word).lower()
        word_polarity = TextBlob(word_clean).sentiment.polarity
        if word_polarity > 0.1:
            positive_words.append(word_clean)
        elif word_polarity < -0.1:
            negative_words.append(word_clean)

    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "color": color,
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity * 100, 1),
        "confidence": confidence,
        "word_count": word_count,
        "positive_words": list(set(positive_words)),
        "negative_words": list(set(negative_words))
    }

# ----------------------------------------
# STEP 3: Page config and custom CSS
# ----------------------------------------
st.set_page_config(
    page_title="SentimentAI",
    page_icon="💬",
    layout="centered"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Header styling */
    .main-header {
        background: #1a1a2e;
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 28px;
        font-weight: 600;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.6);
        font-size: 14px;
        margin: 6px 0 0 0;
    }

    /* Result card styling */
    .result-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    .sentiment-text {
        font-size: 32px;
        font-weight: 600;
        margin: 0;
    }

    /* Keyword pill styling */
    .keyword-positive {
        background: #E1F5EE;
        color: #085041;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px;
        display: inline-block;
    }
    .keyword-negative {
        background: #FCEBEB;
        color: #501313;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin: 3px;
        display: inline-block;
    }

    /* Metric card styling */
    .metric-container {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .metric-value {
        font-size: 22px;
        font-weight: 500;
        margin: 0;
        color: white;
    }
    .metric-label {
        font-size: 12px;
        color: rgba(255,255,255,0.5);
        margin: 4px 0 0 0;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# STEP 4: Header
# ----------------------------------------
st.markdown("""
<div class="main-header">
    <h1>💬 SentimentAI</h1>
    <p>Understand the emotion behind any text instantly</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------
# STEP 5: Text input
# ----------------------------------------
st.subheader("Enter your text")
user_text = st.text_area(
    "",
    placeholder="Type or paste any text here — a review, tweet, feedback, or anything you want to analyze...",
    height=150
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("Analyse Sentiment", use_container_width=True)

# ----------------------------------------
# STEP 6: Show results
# ----------------------------------------
if analyze_btn:
    if user_text.strip():
        result = analyze_sentiment(user_text)

        st.markdown("---")
        st.subheader("Result")

        # Main sentiment result
        st.markdown(f"""
        <div class="result-card">
            <p style="font-size: 48px; margin: 0;">{result['emoji']}</p>
            <p class="sentiment-text" style="color: {result['color']};">
                {result['sentiment']}
            </p>
            <p style="color: #888; font-size: 14px; margin: 4px 0 0 0;">
                Overall sentiment detected
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Metrics row
        st.markdown("---")
        st.subheader("Details")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value" style="color: {result['color']};">
                    {result['confidence']}%
            </p>
            <p class="metric-label">Confidence</p>
            <p class="metric-desc">How strongly the text leans 
            toward this sentiment. Higher % means clearer emotion.</p>
        </div>
        """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value">{result['word_count']}</p>
                <p class="metric-label">Word Count</p>
                <p class="metric-desc">Total number of words in 
                your text. More words usually give more accurate results.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <p class="metric-value">{result['subjectivity']}%</p>
                <p class="metric-label">Subjectivity</p>
                <p class="metric-desc">0% means pure fact. 100% means 
                pure personal opinion. Most reviews are between 40–80%.</p>
            </div>
            """, unsafe_allow_html=True)
    

        # Sentiment bar
        st.markdown("---")
        st.subheader("Sentiment breakdown")
        st.write("This bar shows the split between positive, neutral and negative in your text.")

        # Calculate percentages
        polarity = result['polarity']
        if polarity > 0.1:
            positive_pct = round(50 + polarity * 50, 1)
            negative_pct = round(10 - polarity * 5, 1)
            neutral_pct = round(100 - positive_pct - negative_pct, 1)
        elif polarity < -0.1:
            negative_pct = round(50 + abs(polarity) * 50, 1)
            positive_pct = round(10 - abs(polarity) * 5, 1)
            neutral_pct = round(100 - positive_pct - negative_pct, 1)
        else:
            neutral_pct = 60.0
            positive_pct = 20.0
            negative_pct = 20.0

        # Make sure percentages don't go below 0
        positive_pct = max(positive_pct, 0)
        negative_pct = max(negative_pct, 0)
        neutral_pct = max(neutral_pct, 0)

        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="display: flex; height: 12px; border-radius: 6px; overflow: hidden;">
                <div style="width: {positive_pct}%; background: #1D9E75;"></div>
                <div style="width: {neutral_pct}%; background: #EF9F27;"></div>
                <div style="width: {negative_pct}%; background: #E24B4A;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 8px;">
                <span style="font-size: 12px; color: #1D9E75;">
                    Positive {positive_pct}%
                </span>
                <span style="font-size: 12px; color: #EF9F27;">
                    Neutral {neutral_pct}%
                </span>
                <span style="font-size: 12px; color: #E24B4A;">
                    Negative {negative_pct}%
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Keywords
        st.markdown("---")
        st.subheader("Key words detected")

        col1, col2 = st.columns(2)
        with col1:
            st.write("Positive words")
            if result['positive_words']:
                keywords_html = " ".join([
                    f'<span class="keyword-positive">{w}</span>'
                    for w in result['positive_words']
                ])
                st.markdown(keywords_html, unsafe_allow_html=True)
            else:
                st.caption("None detected")

        with col2:
            st.write("Negative words")
            if result['negative_words']:
                keywords_html = " ".join([
                    f'<span class="keyword-negative">{w}</span>'
                    for w in result['negative_words']
                ])
                st.markdown(keywords_html, unsafe_allow_html=True)
            else:
                st.caption("None detected")

    else:
        st.error("Please enter some text to analyze!")