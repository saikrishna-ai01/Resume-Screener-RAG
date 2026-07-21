import os
import streamlit as st
import requests

API_URL = os.getenv(
    "API_URL",
    "https://resume-screener-rag.onrender.com"
)

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# -------------------------
# Title
# -------------------------
st.title("📄 AI Resume Screener with RAG")
st.write("Upload a resume and ask questions using Gemini + ChromaDB.")

# -------------------------
# Upload Resume
# -------------------------
st.header("1️⃣ Upload Resume")

uploaded_file = st.file_uploader(
    "Choose a Resume",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:

    if st.button("Upload Resume"):

        with st.spinner("Uploading and indexing resume..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

                if response.status_code == 200:

                    st.session_state.uploaded = True

                    result = response.json()

                    # Save parsed resume text for ATS analysis
                    st.session_state.resume_text = result["data"]["text"]

                    st.success("✅ Resume uploaded successfully!")

                    st.write(f"**Filename:** {result['filename']}")

                    if "chunks_created" in result:
                        st.write(f"**Chunks Created:** {result['chunks_created']}")

                    if "total_documents" in result:
                        st.write(f"**Total Documents in ChromaDB:** {result['total_documents']}")

                    with st.expander("Parsed Resume Data"):
                        st.json(result["data"])

                else:
                    st.session_state.uploaded = False
                    st.error(response.text)

            except Exception as e:
                st.session_state.uploaded = False
                st.error(f"Connection Error: {e}")

# -------------------------
# Ask Questions
# -------------------------
st.divider()

st.header("2️⃣ Ask Questions")

question = st.text_input(
    "Ask a question about the uploaded resume"
)

if st.button("Ask"):

    if not st.session_state.uploaded:

        st.warning("Please upload a resume first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating answer..."):

            try:

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.subheader("💡 Answer")
                    st.success(result["answer"])

                    st.subheader("📚 Retrieved Context")

                    context = result.get("context", "")

                    if context.strip():
                        with st.expander("Retrieved Context", expanded=True):
                            st.text_area(
                                "Context",
                                context,
                                height=300,
                                disabled=True
                            )
                    else:
                        st.info("No retrieved context was returned.")

                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Connection Error: {e}")

# -------------------------
# ATS Resume Analysis
# -------------------------

st.divider()

st.header("3️⃣ ATS Resume Analysis")

st.write("Upload a Job Description (PDF, DOCX, TXT)")

jd_file = st.file_uploader(
    "Choose Job Description",
    type=["pdf", "docx", "txt"],
    key="jd_upload"
)

if jd_file is not None:

    if st.button("Upload Job Description"):

        files = {
            "file": (
                jd_file.name,
                jd_file.getvalue(),
                jd_file.type
            )
        }
        try:

           response = requests.post(
               f"{API_URL}/upload-jd",
               files=files
           )

           if response.status_code == 200:

               st.success("✅ Job Description uploaded successfully!")

               # Store locally for ATS request
               if "data" in response.json():
                   st.session_state.job_description = response.json()["data"]["text"]

           else:
                st.error(response.text)

        except Exception as e:

            st.error(f"Connection Error: {e}")

if st.button("Analyze ATS"):

    if not st.session_state.uploaded:

        st.warning("Please upload a resume first.")

    elif st.session_state.job_description == "":
        st.warning("Please upload a Job Description first.")

    else:

        with st.spinner("Analyzing resume..."):

            try:
                response = requests.post(
                    f"{API_URL}/ats-score"
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("ATS Analysis Completed")

                    st.metric(
                        "ATS Score",
                        f"{result['ats_score']}%"
                    )

                    st.write("### Recommendation")
                    st.info(result["recommendation"])

                    st.write("### Matched Skills")

                    if result["matched_skills"]:
                        for skill in result["matched_skills"]:
                            st.success(f"✅ {skill}")
                    else:
                        st.info("No matched skills found.")

                    st.write("### Missing Skills")

                    if result["missing_skills"]:
                        for skill in result["missing_skills"]:
                            st.warning(f"⚠️ {skill}")
                    else:
                        st.success("No missing skills.")

                    st.write("### Additional Skills")

                    if result["additional_skills"]:
                        for skill in result["additional_skills"]:
                            st.info(f"➕ {skill}")
                    else:
                        st.info("No additional skills.")

                    st.write("### Strengths")

                    if result["strengths"]:
                        for strength in result["strengths"]:
                            st.success(f"💪 {strength}")
                    else:
                        st.info("No strengths available.")

                    st.write("### Improvements")

                    if result["improvements"]:
                        for improvement in result["improvements"]:
                            st.warning(f"📝 {improvement}")
                    else:
                        st.success("No improvements suggested.")

                    st.subheader("🤖 AI Review")

                    ai_review = result.get("ai_review")

                    if isinstance(ai_review, str):
                        st.markdown(ai_review)
                    elif isinstance(ai_review, dict):
                        st.warning(ai_review.get("message", "AI Review unavailable."))
                    else:
                        st.info("AI Review unavailable.")

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(f"Connection Error: {e}")
