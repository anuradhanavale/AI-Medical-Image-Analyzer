import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

generation_config = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Gemini 2.5 Flash is the standard for 2026
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    generation_config=generation_config
)

# ---------------- UI ----------------
st.set_page_config(page_title="AI Medical Image Analyzer", page_icon="a.png", layout="centered")


col1, col2 = st.columns([0.8, 7])

with col1:
    st.image("a.png", width=80)

with col2:
    st.markdown(
        "<h1 style='margin-top:-10px;'>AI Medical Image Analyzer</h1>",
        unsafe_allow_html=True
    )

st.info("Operate as a high-fidelity Diagnostic Assistant")

uploaded_file = st.file_uploader(" Upload Medical Image", type=["jpg", "jpeg", "png"])

# ---------------- PROMPT ----------------
system_prompt = """
You are an expert medical imaging assistant. 
Analyze the provided image and generate a structured report:

1.Primary Observations

2.Potential Findings (expressed with clinical caution)

3.Technical Quality of Image

4.Recommended Clinical Correlation

Differential Diagnosis (Ranked by likelihood)

6.Anatomical Localization & Relationship to Adjacent Structures

7.Urgency Level (Routine, Urgent, or Emergent Triage)

8.Comparison with Standard Physiological Norms

9.Identification of Relevant Pathological Markers

10.Suggested Follow-up Imaging Modalities (e.g., MRI, CT, PET)

Maintain a professional, objective, and non-diagnostic tone.
"""

# ---------------- PROCESS ----------------
if st.button(" Analyze Image"):
    if not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        try:
            with st.spinner("Gemini 2.5 is analyzing... ⏳"):
                image_bytes = uploaded_file.getvalue()
                
                # Format for the GenAI SDK
                image_part = {
                    "mime_type": uploaded_file.type,
                    "data": image_bytes
                }

                # Generate content
                response = model.generate_content([system_prompt, image_part])

            st.success(" Analysis Complete")
            
            st.image(uploaded_file, use_column_width=True)
            
            st.divider()
            st.subheader(" AI Analysis Report")
            st.markdown(response.text)

        except Exception as e:
            st.error(f" Error: {str(e)}")

st.divider()
st.caption("2026 Edition | Powered by Anuradha Navale")