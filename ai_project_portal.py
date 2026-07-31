import streamlit as st
import json
import os
import random
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="AI Project Recommendation Portal", page_icon="🎓", layout="wide")

# --- Styling ---
st.markdown("""
<style>
    .project-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .project-card:hover {
        border-color: #1a73e8;
        box-shadow: 0 2px 8px rgba(26,115,232,0.15);
    }
    .difficulty-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        color: white;
    }
    .difficulty-badge.Beginner { background: #4caf50; }
    .difficulty-badge.Intermediate { background: #ff9800; }
    .difficulty-badge.Advanced { background: #dc3545; }
    .match-score {
        font-size: 1.5rem;
        font-weight: 800;
    }
    .stat-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }
    .tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1565c0;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.75rem;
        margin: 2px;
    }
    .stButton > button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- Project Database ---
PROJECTS = [
    {
        "id": 1,
        "title": "Sentiment Analysis on Social Media Posts",
        "description": "Build an NLP model that classifies tweets/posts as positive, negative, or neutral using techniques like TF-IDF, Word2Vec, or BERT embeddings.",
        "category": "NLP",
        "difficulty": "Beginner",
        "skills_required": ["Python", "NLP", "Pandas", "Scikit-learn"],
        "interests": ["Natural Language Processing", "Social Media", "Text Mining"],
        "estimated_time": "2-3 weeks",
        "dataset": "Twitter Sentiment140 / Kaggle",
        "tools": ["Python", "NLTK", "Transformers", "Scikit-learn"],
        "learning_outcomes": ["Text preprocessing", "Feature extraction (TF-IDF)", "Classification models", "BERT fine-tuning"],
    },
    {
        "id": 2,
        "title": "Image Classification with CNN (Digit Recognition)",
        "description": "Implement a Convolutional Neural Network from scratch to classify handwritten digits using the MNIST dataset.",
        "category": "Computer Vision",
        "difficulty": "Beginner",
        "skills_required": ["Python", "Deep Learning", "TensorFlow/PyTorch"],
        "interests": ["Computer Vision", "Image Processing", "Deep Learning"],
        "estimated_time": "2-3 weeks",
        "dataset": "MNIST / Fashion-MNIST",
        "tools": ["TensorFlow/Keras", "PyTorch", "NumPy", "Matplotlib"],
        "learning_outcomes": ["CNN architecture", "Data augmentation", "Model evaluation", "Overfitting prevention"],
    },
    {
        "id": 3,
        "title": "Chatbot using Seq2Seq Model",
        "description": "Create a conversational chatbot using sequence-tosequence models with attention mechanism trained on dialogue datasets.",
        "category": "NLP",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "NLP", "Deep Learning", "TensorFlow/PyTorch"],
        "interests": ["Natural Language Processing", "Conversational AI", "Deep Learning"],
        "estimated_time": "4-6 weeks",
        "dataset": "Cornell Movie Dialogues / Daily Dialog",
        "tools": ["PyTorch", "HuggingFace Transformers", "NLTK", "spaCy"],
        "learning_outcomes": ["Encoder-decoder architecture", "Attention mechanisms", "Beam search decoding", "Dialogue management"],
    },
    {
        "id": 4,
        "title": "Stock Price Prediction with LSTM",
        "description": "Use Long Short-Term Memory (LSTM) networks to predict stock prices based on historical data and technical indicators.",
        "category": "Time Series / Finance",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "Deep Learning", "Pandas", "Data Visualization"],
        "interests": ["Finance", "Time Series Analysis", "Deep Learning"],
        "estimated_time": "3-5 weeks",
        "dataset": "Yahoo Finance API / Alpha Vantage",
        "tools": ["TensorFlow/Keras", "Pandas", "Matplotlib", "yfinance"],
        "learning_outcomes": ["Time series preprocessing", "LSTM architecture", "Sequence modeling", "Financial data handling"],
    },
    {
        "id": 5,
        "title": "Object Detection with YOLOv8",
        "description": "Build a real-time object detection system using YOLOv8 for identifying and localizing objects in images and video streams.",
        "category": "Computer Vision",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "Deep Learning", "OpenCV", "PyTorch"],
        "interests": ["Computer Vision", "Real-time Systems", "Object Detection"],
        "estimated_time": "4-6 weeks",
        "dataset": "COCO Dataset / Custom annotated data",
        "tools": ["Ultralytics YOLOv8", "OpenCV", "PyTorch", "Roboflow"],
        "learning_outcomes": ["Object detection fundamentals", "YOLO architecture", "Bounding box prediction", "Real-time inference"],
    },
    {
        "id": 6,
        "title": "Fake News Detection System",
        "description": "Develop a machine learning model to detect fake news articles using NLP techniques and various ML classifiers.",
        "category": "NLP",
        "difficulty": "Beginner",
        "skills_required": ["Python", "NLP", "Scikit-learn", "Pandas"],
        "interests": ["Natural Language Processing", "Social Good", "Text Classification"],
        "estimated_time": "2-4 weeks",
        "dataset": "LIAR Dataset / Kaggle Fake News",
        "tools": ["Scikit-learn", "NLTK", "TF-IDF", "XGBoost"],
        "learning_outcomes": ["Text classification", "Feature engineering", "Model comparison", "Misinformation detection"],
    },
    {
        "id": 7,
        "title": "Recommendation System (Movie/Product)",
        "description": "Build a collaborative filtering and content-based recommendation system for movies or e-commerce products.",
        "category": "Recommender Systems",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "Machine Learning", "Pandas", "NumPy"],
        "interests": ["Recommender Systems", "E-commerce", "Machine Learning"],
        "estimated_time": "3-5 weeks",
        "dataset": "MovieLens / Amazon Product Reviews",
        "tools": ["Surprise library", "Scikit-learn", "Pandas", "NumPy"],
        "learning_outcomes": ["Collaborative filtering", "Content-based filtering", "Matrix factorization", "Evaluation metrics (RMSE/MAE)"],
    },
    {
        "id": 8,
        "title": "Diabetes Prediction using ML",
        "description": "Build a healthcare ML model to predict diabetes risk using patient health indicators with multiple ML algorithms.",
        "category": "Healthcare AI",
        "difficulty": "Beginner",
        "skills_required": ["Python", "Machine Learning", "Scikit-learn", "Pandas"],
        "interests": ["Healthcare", "Machine Learning", "Social Good"],
        "estimated_time": "2-3 weeks",
        "dataset": "PIMA Indians Diabetes / Kaggle",
        "tools": ["Scikit-learn", "Pandas", "Matplotlib", "XGBoost"],
        "learning_outcomes": ["Data preprocessing", "Model selection", "Cross-validation", "Healthcare analytics"],
    },
    {
        "id": 9,
        "title": "Autonomous Driving Lane Detection",
        "description": "Implement computer vision techniques to detect and track lane markings on roads for autonomous driving applications.",
        "category": "Computer Vision",
        "difficulty": "Advanced",
        "skills_required": ["Python", "Computer Vision", "OpenCV", "Deep Learning"],
        "interests": ["Computer Vision", "Autonomous Systems", "Edge AI"],
        "estimated_time": "6-8 weeks",
        "dataset": "TuSimple Lane Detection / CULane",
        "tools": ["OpenCV", "PyTorch", "U-Net", "ROS"],
        "learning_outcomes": ["Edge detection", "Hough transforms", "Semantic segmentation", "Real-time video processing"],
    },
    {
        "id": 10,
        "title": "Text-to-Speech Generation with TTS",
        "description": "Build a text-to-speech system using deep learning models like Tacotron or VITS for natural-sounding speech synthesis.",
        "category": "Generative AI",
        "difficulty": "Advanced",
        "skills_required": ["Python", "Deep Learning", "Audio Processing", "PyTorch"],
        "interests": ["Generative AI", "Audio Processing", "NLP"],
        "estimated_time": "6-10 weeks",
        "dataset": "LJSpeech / Blizzard Challenge",
        "tools": ["PyTorch", "librosa", "HuggingFace", "Coqui TTS"],
        "learning_outcomes": ["Spectrogram generation", "Vocoder models", "Audio synthesis", "Sequence modeling"],
    },
    {
        "id": 11,
        "title": "Face Recognition Attendance System",
        "description": "Create an automated attendance system using face recognition with OpenCV and deep learning face embeddings.",
        "category": "Computer Vision",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "OpenCV", "Deep Learning", "Flask"],
        "interests": ["Computer Vision", "Web Development", "Automation"],
        "estimated_time": "3-5 weeks",
        "dataset": "LFW / Custom classroom dataset",
        "tools": ["OpenCV", "FaceNet", "Flask", "SQLite"],
        "learning_outcomes": ["Face detection & recognition", "Embedding vectors", "Web app integration", "Database management"],
    },
    {
        "id": 12,
        "title": "AI Music Generation with RNN",
        "description": "Generate musical compositions using Recurrent Neural Networks trained on MIDI datasets.",
        "category": "Generative AI",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "Deep Learning", "Music Theory", "TensorFlow/PyTorch"],
        "interests": ["Generative AI", "Music", "Creative AI"],
        "estimated_time": "4-6 weeks",
        "dataset": "MAESTRO Dataset / Lakh MIDI",
        "tools": ["TensorFlow", "music21", "Mido", "FluidSynth"],
        "learning_outcomes": ["RNN/LSTM for sequences", "MIDI processing", "Music representation", "Creative AI"],
    },
    {
        "id": 13,
        "title": "COVID-19 X-Ray Analysis with Transfer Learning",
        "description": "Use transfer learning with pre-trained CNNs to detect COVID-19 from chest X-ray images.",
        "category": "Healthcare AI",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "Deep Learning", "Computer Vision", "Transfer Learning"],
        "interests": ["Healthcare", "Computer Vision", "Deep Learning"],
        "estimated_time": "3-5 weeks",
        "dataset": "COVID-19 Radiography Database",
        "tools": ["TensorFlow/Keras", "ResNet50", "OpenCV", "Scikit-learn"],
        "learning_outcomes": ["Transfer learning", "Medical imaging", "Data augmentation", "Model fine-tuning"],
    },
    {
        "id": 14,
        "title": "Smart Home Automation with IoT + AI",
        "description": "Build an IoT-based smart home system that uses AI to automate lighting, temperature, and security based on user behavior.",
        "category": "IoT + AI",
        "difficulty": "Advanced",
        "skills_required": ["Python", "IoT", "Machine Learning", "Embedded Systems"],
        "interests": ["IoT", "Automation", "Smart Systems"],
        "estimated_time": "6-8 weeks",
        "dataset": "Custom sensor data / Smart Home datasets",
        "tools": ["Raspberry Pi", "MQTT", "Scikit-learn", "Flask"],
        "learning_outcomes": ["Sensor integration", "Edge AI", "Predictive automation", "MQTT protocol"],
    },
    {
        "id": 15,
        "title": "Resume Screening with NLP",
        "description": "Automate resume screening by extracting skills and matching candidates to job descriptions using NLP.",
        "category": "NLP",
        "difficulty": "Beginner",
        "skills_required": ["Python", "NLP", "Scikit-learn", "Pandas"],
        "interests": ["Natural Language Processing", "HR Tech", "Automation"],
        "estimated_time": "2-4 weeks",
        "dataset": "Kaggle Resume Dataset / Custom",
        "tools": ["spaCy", "Scikit-learn", "TF-IDF", "Streamlit"],
        "learning_outcomes": ["Information extraction", "Entity recognition", "Document classification", "HR automation"],
    },
    {
        "id": 16,
        "title": "GAN-based Image Generation",
        "description": "Train a Generative Adversarial Network to generate realistic images (faces, art, or fashion items).",
        "category": "Generative AI",
        "difficulty": "Advanced",
        "skills_required": ["Python", "Deep Learning", "PyTorch", "Computer Vision"],
        "interests": ["Generative AI", "Computer Vision", "Creative AI"],
        "estimated_time": "6-10 weeks",
        "dataset": "CelebA / MNIST Fashion / Custom",
        "tools": ["PyTorch", "TensorFlow", "Matplotlib", "Weights & Biases"],
        "learning_outcomes": ["GAN architecture", "Generator & discriminator training", "Loss functions", "Image generation"],
    },
    {
        "id": 17,
        "title": "AI-Powered Crop Disease Detection",
        "description": "Build a CNN model that detects crop diseases from leaf images and recommends treatments.",
        "category": "AI for Agriculture",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "Deep Learning", "Computer Vision", "Mobile Dev"],
        "interests": ["Agriculture", "Computer Vision", "Social Good"],
        "estimated_time": "4-6 weeks",
        "dataset": "PlantVillage Dataset / Kaggle",
        "tools": ["TensorFlow", "Keras", "Flutter", "TensorFlow Lite"],
        "learning_outcomes": ["Image classification", "Transfer learning", "Mobile deployment", "Agriculture AI"],
    },
    {
        "id": 18,
        "title": "Language Translation with Transformers",
        "description": "Implement a neural machine translation system using Transformer architecture for Indian languages.",
        "category": "NLP",
        "difficulty": "Advanced",
        "skills_required": ["Python", "NLP", "Deep Learning", "PyTorch"],
        "interests": ["Natural Language Processing", "Translation", "Deep Learning"],
        "estimated_time": "6-8 weeks",
        "dataset": "OPUS / IIT Bombay Hindi-English Corpus",
        "tools": ["PyTorch", "HuggingFace Transformers", "Tokenizers", "BLEU score"],
        "learning_outcomes": ["Transformer architecture", "Multi-head attention", "Tokenization", "Evaluation (BLEU)"],
    },
    {
        "id": 19,
        "title": "Student Performance Prediction",
        "description": "Analyze student academic data to predict performance and identify at-risk students using ML.",
        "category": "Education AI",
        "difficulty": "Beginner",
        "skills_required": ["Python", "Machine Learning", "Pandas", "Data Visualization"],
        "interests": ["Education", "Machine Learning", "Social Good"],
        "estimated_time": "2-3 weeks",
        "dataset": "UCI Student Performance / Kaggle",
        "tools": ["Scikit-learn", "Pandas", "Plotly", "XGBoost"],
        "learning_outcomes": ["EDA", "Feature engineering", "Classification & regression", "Educational analytics"],
    },
    {
        "id": 20,
        "title": "AI Chatbot for Mental Health Support",
        "description": "Develop an empathetic AI chatbot that provides preliminary mental health support using NLP and sentiment analysis.",
        "category": "NLP",
        "difficulty": "Intermediate",
        "skills_required": ["Python", "NLP", "Deep Learning", "Flask"],
        "interests": ["Mental Health", "NLP", "Social Good", "Conversational AI"],
        "estimated_time": "4-6 weeks",
        "dataset": "Reddit Mental Health / HOPE dataset",
        "tools": ["HuggingFace Transformers", "BERT", "Flask", "Firebase"],
        "learning_outcomes": ["Sentiment analysis", "Empathetic response generation", "Safety in AI", "Web deployment"],
    },
]

# --- Session State ---
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "student_profile" not in st.session_state:
    st.session_state.student_profile = {}

# --- Recommendation Engine ---
def calculate_match(project, skills, interests, difficulty_pref):
    score = 0
    reasons = []

    # Skill match (40% weight)
    project_skills = set(s.lower() for s in project["skills_required"])
    user_skills = set(s.lower() for s in skills)
    skill_matches = project_skills & user_skills
    skill_score = len(skill_matches) / len(project_skills) * 40 if project_skills else 0
    score += skill_score
    if skill_matches:
        reasons.append(f"Matches your skills: {', '.join(skill_matches)}")

    # Interest match (40% weight)
    project_interests = set(i.lower() for i in project["interests"])
    user_interests = set(i.lower() for i in interests)
    interest_matches = project_interests & user_interests
    interest_score = len(interest_matches) / len(project_interests) * 40 if project_interests else 0
    score += interest_score
    if interest_matches:
        reasons.append(f"Aligns with your interests: {', '.join(interest_matches)}")

    # Difficulty match (20% weight)
    diff_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    pref_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Any": 0}
    if difficulty_pref == "Any":
        score += 10
        reasons.append("Suitable for any level")
    else:
        if diff_map.get(project["difficulty"], 2) == pref_map.get(difficulty_pref, 0):
            score += 20
            reasons.append(f"Matches your level: {project['difficulty']}")
        elif diff_map.get(project["difficulty"], 2) < pref_map.get(difficulty_pref, 0):
            score += 15
            reasons.append(f"Slightly easier than your level — good for building confidence")
        else:
            score += 5
            reasons.append(f"More challenging than your level — great for growth")

    return round(score), reasons

# --- Header ---
st.title("🎓 AI Project Recommendation Portal")
st.markdown("Find the perfect AI/ML project tailored to your skills, interests, and experience level.")

st.markdown("---")

# --- Input Form Sidebar ---
with st.sidebar:
    st.header("👤 Student Profile")

    student_name = st.text_input("Name", placeholder="Enter your name")

    st.subheader("Experience Level")
    experience = st.select_slider(
        "Select your level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )

    st.subheader("🛠️ Your Skills")
    all_skills = ["Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
                  "Data Analysis", "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
                  "PyTorch", "OpenCV", "Flask", "Data Visualization", "Statistics",
                  "SQL", "Git", "Cloud (AWS/GCP)", "IoT", "Embedded Systems",
                  "Web Development", "Mobile Development", "Audio Processing", "Music Theory"]
    selected_skills = st.multiselect("Select your skills", all_skills)

    st.subheader("💡 Your Interests")
    all_interests = ["Natural Language Processing", "Computer Vision", "Deep Learning",
                     "Generative AI", "Healthcare", "Finance", "Education", "Social Good",
                     "Automation", "Recommender Systems", "Time Series Analysis",
                     "Conversational AI", "Autonomous Systems", "IoT", "Music",
                     "Creative AI", "Agriculture", "E-commerce", "HR Tech",
                     "Real-time Systems", "Edge AI", "Mental Health", "Smart Systems",
                     "Text Mining", "Social Media", "Image Processing", "Object Detection",
                     "Text Classification", "Conversational AI"]
    selected_interests = st.multiselect("Select your interests", all_interests)

    st.subheader("📊 Preferred Difficulty")
    difficulty_pref = st.selectbox("Project difficulty", ["Any", "Beginner", "Intermediate", "Advanced"])

    st.markdown("---")

    if st.button("🎯 Get Recommendations", type="primary", use_container_width=True):
        if not student_name.strip():
            st.error("Please enter your name!")
        elif not selected_skills and not selected_interests:
            st.error("Select at least your skills or interests!")
        else:
            # Calculate match scores
            scored = []
            for project in PROJECTS:
                score, reasons = calculate_match(
                    project, selected_skills, selected_interests, difficulty_pref
                )
                scored.append((project, score, reasons))

            scored.sort(key=lambda x: x[1], reverse=True)
            st.session_state.recommendations = scored
            st.session_state.student_profile = {
                "name": student_name.strip(),
                "experience": experience,
                "skills": selected_skills,
                "interests": selected_interests,
                "difficulty_pref": difficulty_pref,
            }
            st.success(f"Recommendations generated for {student_name}! ✅")

# --- Main Content ---

# Stats
stat_cols = st.columns(4)
with stat_cols[0]:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{len(PROJECTS)}</div><div class="stat-label">Total Projects</div></div>', unsafe_allow_html=True)
with stat_cols[1]:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#4caf50">{sum(1 for p in PROJECTS if p["difficulty"]=="Beginner")}</div><div class="stat-label">Beginner</div></div>', unsafe_allow_html=True)
with stat_cols[2]:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#ff9800">{sum(1 for p in PROJECTS if p["difficulty"]=="Intermediate")}</div><div class="stat-label">Intermediate</div></div>', unsafe_allow_html=True)
with stat_cols[3]:
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="color:#dc3545">{sum(1 for p in PROJECTS if p["difficulty"]=="Advanced")}</div><div class="stat-label">Advanced</div></div>', unsafe_allow_html=True)

st.markdown("")

# --- Recommendations Display ---
if st.session_state.recommendations:
    profile = st.session_state.student_profile
    st.markdown(f"### 🎯 Personalized Recommendations for {profile['name']}")
    st.markdown(f"**Level:** {profile['experience']} | **Skills:** {', '.join(profile['skills']) if profile['skills'] else 'None'} | **Interests:** {', '.join(profile['interests']) if profile['interests'] else 'None'}")
    st.markdown("---")

    top_n = st.slider("Number of recommendations", min_value=3, max_value=len(st.session_state.recommendations), value=10)

    for i, (project, score, reasons) in enumerate(st.session_state.recommendations[:top_n]):
        with st.container():
            cols = st.columns([0.15, 0.85])

            with cols[0]:
                color = "#4caf50" if score >= 70 else "#ff9800" if score >= 50 else "#dc3545"
                st.markdown(f"""
                <div style='text-align:center; padding-top:8px;'>
                    <div class='match-score' style='color:{color}'>{score}%</div>
                    <div style='font-size:0.7rem; color:#9aa0a6; margin-top:2px;'>Match</div>
                </div>
                """, unsafe_allow_html=True)

            with cols[1]:
                diff_class = project["difficulty"].lower()
                st.markdown(f"""
                <div class='project-card'>
                    <h4 style='margin:0 0 6px 0;'>#{i+1} {project['title']}</h4>
                    <p style='color:#5f6368; margin:0 0 8px 0; font-size:0.9rem;'>{project['description']}</p>
                    <div style='margin:4px 0;'>
                        <span class='difficulty-badge {diff_class}'>{project['difficulty']}</span>
                        <span class='tag'>📂 {project['category']}</span>
                        <span class='tag'>⏱️ {project['estimated_time']}</span>
                        <span class='tag'>📊 {project['dataset']}</span>
                    </div>
                    <div style='margin:6px 0;'>
                        <strong>🔧 Tools:</strong> {', '.join(project['tools'])}
                    </div>
                    <div style='margin:6px 0;'>
                        <strong>🛠️ Required Skills:</strong> {', '.join(project['skills_required'])}
                    </div>
                    <div style='margin:6px 0;'>
                        <strong>📚 Learning Outcomes:</strong>
                        <ul style='margin:4px 0; padding-left:20px;'>
                            {''.join(f'<li>{lo}</li>' for lo in project['learning_outcomes'])}
                        </ul>
                    </div>
                    <div style='margin:6px 0; background:#e8f5e9; padding:8px 12px; border-radius:8px;'>
                        <strong>✨ Why this matches:</strong>
                        <ul style='margin:4px 0; padding-left:20px;'>
                            {''.join(f'<li>{r}</li>' for r in reasons)}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander(f"📋 Detailed View — {project['title']}", expanded=False):
                detail_cols = st.columns(3)
                with detail_cols[0]:
                    st.markdown(f"**Category:** {project['category']}")
                    st.markdown(f"**Difficulty:** {project['difficulty']}")
                    st.markdown(f"**Estimated Time:** {project['estimated_time']}")
                with detail_cols[1]:
                    st.markdown(f"**Dataset:** {project['dataset']}")
                    st.markdown(f"**Tools:** {', '.join(project['tools'])}")
                    st.markdown(f"**Skills Required:** {', '.join(project['skills_required'])}")
                with detail_cols[2]:
                    st.markdown("**Learning Outcomes:**")
                    for lo in project['learning_outcomes']:
                        st.markdown(f"- {lo}")

                    # Export this project
                    if st.button(f"📥 Export Project Details", key=f"export_{project['id']}"):
                        export_text = f"""
AI PROJECT RECOMMENDATION
=========================
Project: {project['title']}
Category: {project['category']}
Difficulty: {project['difficulty']}
Estimated Time: {project['estimated_time']}

DESCRIPTION:
{project['description']}

SKILLS REQUIRED:
{', '.join(project['skills_required'])}

TOOLS:
{', '.join(project['tools'])}

DATASET:
{project['dataset']}

LEARNING OUTCOMES:
{chr(10).join('- ' + lo for lo in project['learning_outcomes'])}

MATCH SCORE: {score}%

WHY THIS MATCHES:
{chr(10).join('- ' + r for r in reasons)}

---
Generated for: {profile['name']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
                        st.download_button(
                            label="⬇️ Download as Text",
                            data=export_text,
                            file_name=f"project_{project['id']}_{project['title'][:30].replace(' ','_')}.txt",
                            mime="text/plain",
                        )

            st.markdown("")

    # Export all recommendations
    st.markdown("---")
    if st.button("📥 Export All Recommendations as JSON", use_container_width=True):
        export_data = {
            "student": profile,
            "recommendations": [
                {
                    "project": p["title"],
                    "category": p["category"],
                    "difficulty": p["difficulty"],
                    "match_score": s,
                    "reasons": r,
                }
                for p, s, r in st.session_state.recommendations[:top_n]
            ],
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name="ai_project_recommendations.json",
            mime="application/json",
        )

else:
    # --- Browse All Projects ---
    st.markdown("### 📂 Browse All Projects")
    st.markdown("Fill out your profile in the sidebar and click **Get Recommendations** for personalized results. Or browse all projects below.")

    browse_cols = st.columns([2, 1, 1])
    with browse_cols[0]:
        search = st.text_input("🔍 Search projects", placeholder="Search by title, category, or keyword...")
    with browse_cols[1]:
        filter_diff = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
    with browse_cols[2]:
        categories = ["All"] + sorted(set(p["category"] for p in PROJECTS))
        filter_cat = st.selectbox("Category", categories)

    st.markdown("---")

    for project in PROJECTS:
        if search and search.lower() not in project["title"].lower() and search.lower() not in project["category"].lower() and search.lower() not in project["description"].lower():
            continue
        if filter_diff != "All" and project["difficulty"] != filter_diff:
            continue
        if filter_cat != "All" and project["category"] != filter_cat:
            continue

        diff_class = project["difficulty"].lower()
        st.markdown(f"""
        <div class='project-card'>
            <h4 style='margin:0 0 4px 0;'>{project['title']}</h4>
            <p style='color:#5f6368; margin:0 0 6px 0; font-size:0.9rem;'>{project['description']}</p>
            <div style='margin:4px 0;'>
                <span class='difficulty-badge {diff_class}'>{project['difficulty']}</span>
                <span class='tag'>📂 {project['category']}</span>
                <span class='tag'>⏱️ {project['estimated_time']}</span>
            </div>
            <div style='margin:4px 0; font-size:0.85rem;'>
                <strong>Skills:</strong> {', '.join(project['skills_required'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Built with Streamlit · AI Project Recommendation Portal by Solene 🤖")
