import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

SPAM_KEYWORDS = [
    "wire transfer",
    "western union",
    "money transfer",
    "bitcoin",
    "cryptocurrency",
    "guaranteed",
    "no experience needed",
    "work from home",
    "processing fee",
    "registration fee",
    "starter kit",
    "commission",
    "paypal",
    "upfront payment"
]

st.set_page_config(
    page_title="Job Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.fake-job {
    background-color: #3b0d0d;
    padding: 20px;
    border-radius: 10px;
    border-left: 6px solid red;
    color: white;
}

.real-job {
    background-color: #052e16;
    padding: 20px;
    border-radius: 10px;
    border-left: 6px solid green;
    color: white;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    return text

def contains_spam_keywords(text):

    text = text.lower()

    return any(keyword in text for keyword in SPAM_KEYWORDS)

@st.cache_resource
def train_job_detector():

  df = pd.read_excel(
    "FakeJobPostings.xlsx",
    engine="openpyxl"
)

    df = df[['title', 'description', 'fraudulent']]

    df['title'] = df['title'].fillna("")

    df['description'] = df['description'].fillna("")

    df = df.dropna(subset=['fraudulent'])

    df['fraudulent'] = df['fraudulent'].astype(int)

    df['text'] = df['title'] + " " + df['description']

    df['cleaned'] = df['text'].apply(clean_text)

    vectorizer = TfidfVectorizer(max_features=5000)

    X = vectorizer.fit_transform(df['cleaned'])

    y = df['fraudulent']

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = MultinomialNB()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred)
    }

    return model, vectorizer, metrics

model, vectorizer, metrics = train_job_detector()

with st.sidebar:

    st.header("🔧 Model Information")

    st.write("### Model Type")
    st.write("Multinomial Naive Bayes")

    st.write("### Feature Extraction")
    st.write("TF-IDF Vectorizer")

st.title("🛡️ Job Scam Detector")

st.write(
    "Analyze job postings to determine whether they are legitimate or fraudulent."
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy", f"{metrics['accuracy']:.2%}")

with col2:
    st.metric("Precision", f"{metrics['precision']:.2%}")

with col3:
    st.metric("Recall", f"{metrics['recall']:.2%}")

with col4:
    st.metric("F1 Score", f"{metrics['f1']:.2%}")

st.markdown("---")

job_text = st.text_area(
    "📝 Paste Job Title and Description",
    height=250
)

if st.button("🔍 Analyze Job"):

    if not job_text.strip():

        st.warning("Please enter job posting text.")

    else:

        cleaned_input = clean_text(job_text)

        vectorized_input = vectorizer.transform([cleaned_input])

        prediction = model.predict(vectorized_input)[0]

        confidence = model.predict_proba(vectorized_input).max()

        spam_keywords_found = contains_spam_keywords(job_text)

        is_spam = prediction == 1 or spam_keywords_found

        st.markdown("---")

        st.subheader("📊 Analysis Result")

        if is_spam:

            st.markdown(f"""
            <div class="fake-job">
                <h2>🚨 SPAM JOB ALERT</h2>
                <h3>Confidence: {confidence:.2%}</h3>
            </div>
            """, unsafe_allow_html=True)

            st.error(
                "This job posting appears suspicious or fraudulent."
            )

        else:

            st.markdown(f"""
            <div class="real-job">
                <h2>✅ THIS JOB LOOKS LEGITIMATE</h2>
                <h3>Confidence: {confidence:.2%}</h3>
            </div>
            """, unsafe_allow_html=True)

            st.success(
                "This posting appears legitimate."
            )

        probs = model.predict_proba(vectorized_input)[0]

        st.markdown("---")

        d1, d2 = st.columns(2)

        with d1:
            st.metric(
                "Legitimate Probability",
                f"{probs[0]:.2%}"
            )

        with d2:
            st.metric(
                "Fraudulent Probability",
                f"{probs[1]:.2%}"
            )

st.markdown("---")

st.markdown("""
<div style="text-align:center;color:gray;">
🛡️ Job Scam Detector | Powered by Machine Learning
</div>
""", unsafe_allow_html=True)
