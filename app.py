import streamlit as st
from google import genai
import os
import json
from pathlib import Path

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are GreenCheck, an expert in environmental claims and sustainability regulation.

You will be given a green claim made by a company or product, and a set of regulatory documents.
Assess whether the claim is substantiated based on established standards.

Respond ONLY in this exact JSON format with no preamble or markdown fences:
{
  "verdict": "Substantiated | Partially Substantiated | Unsubstantiated | Misleading",
  "confidence": "High | Medium | Low",
  "relevant_standard": "Name of the most relevant regulation or framework",
  "what_the_regulation_says": "The actual requirement or definition from the source",
  "why": "One paragraph plain-English explanation of your verdict",
  "red_flags": ["list of specific concerns, or empty list"],
  "what_would_make_it_valid": "What the company would need to do or prove"
}

Be precise. Cite specific language from the documents. Do not invent standards."""

@st.cache_data
def load_corpus():
    corpus_dir = Path("corpus")
    docs = {}
    for f in corpus_dir.glob("*.txt"):
        docs[f.stem] = f.read_text(encoding="utf-8")
    return docs

def check_claim(claim: str, docs: dict) -> dict:
    context = "\n\n".join(
        f"=== SOURCE: {name} ===\n{content}"
        for name, content in docs.items()
    )

    prompt = f"{SYSTEM_PROMPT}\n\nCLAIM TO ASSESS:\n\"{claim}\"\n\nREGULATORY DOCUMENTS:\n{context}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return json.loads(response.text.strip())

# --- UI ---
st.set_page_config(page_title="GreenCheck", page_icon="🌿", layout="centered")
st.title("🌿 GreenCheck")
st.caption("Validate environmental claims against open regulatory standards")

docs = load_corpus()

if not docs:
    st.warning("No documents found in /corpus. Add .txt files to get started.")
else:
    st.caption(f"Checking against {len(docs)} source(s): {', '.join(docs.keys())}")

claim = st.text_area(
    "Paste a green claim to validate",
    placeholder="e.g. 'Our product is carbon neutral' or 'Made from 100% sustainable materials'",
    height=100
)

if st.button("Check claim →", disabled=not claim or not docs):
    with st.spinner("Checking against regulatory standards..."):
        try:
            result = check_claim(claim, docs)

            verdict_colour = {
                "Substantiated": "green",
                "Partially Substantiated": "orange",
                "Unsubstantiated": "red",
                "Misleading": "red"
            }.get(result["verdict"], "gray")

            st.markdown(f"### :{verdict_colour}[{result['verdict']}] · Confidence: {result['confidence']}")
            st.markdown(f"**Relevant standard:** {result['relevant_standard']}")

            with st.expander("What the regulation says"):
                st.write(result["what_the_regulation_says"])

            st.markdown(f"**Why:** {result['why']}")

            if result["red_flags"]:
                st.markdown("**Red flags:**")
                for flag in result["red_flags"]:
                    st.markdown(f"- {flag}")

            st.info(f"**What would make it valid:** {result['what_would_make_it_valid']}")

        except json.JSONDecodeError:
            st.error("Couldn't parse the response. Try again.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")