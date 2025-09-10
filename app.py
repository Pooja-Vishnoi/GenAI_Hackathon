import streamlit as st
import pandas as pd
from analyse_pipeline import create_results, recalculate_results, analyze_results

def main():
    st.set_page_config(page_title="Gen AI Crew - AI Analyst for Startups", layout="wide")

    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "results_df" not in st.session_state:
        st.session_state.results_df = create_results()

    st.title("🚀 Gen AI Crew → AI Analyst for Startups")

    if not st.session_state.show_results:
        st.write("Upload the required and optional documents below:")

        pitch_deck = st.file_uploader("Pitch Deck (PDF) *Required", type=["pdf"], key="pitch_deck")
        call_transcript = st.file_uploader("Call Transcript (DOC, TXT)", type=["doc", "docx", "txt"], key="call_transcript")
        email_copy = st.file_uploader("Email Copy (DOC, TXT)", type=["doc", "docx", "txt"], key="email_copy")
        founders_doc = st.file_uploader("Founders Document (DOC, TXT)", type=["doc", "docx", "txt"], key="founders_doc")

        uploaded_files = [f for f in [pitch_deck, call_transcript, email_copy, founders_doc] if f is not None]

        if st.button("🔍 Analyse"):
            if pitch_deck is None:
                st.error("⚠️ Please upload the Pitch Deck (PDF). It is mandatory.")
            else:
                st.session_state.show_results = True
                summary_df, results_df, score, flags, recommendations = create_results(uploaded_files)
                st.session_state.summary_df = summary_df
                st.session_state.results_df = results_df
                st.rerun()

    else:

        # Calculate metrics (will refresh only after Analyse Again is clicked)
        score, flags, recommendations = analyze_results(st.session_state.results_df)
        st.subheader("📊 Analysis Results")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("Highlights from report")
            st.write(st.session_state.summary_df )
        with col2:
            
            st.markdown("### 📈 Trends from Data")
            # Editable table
            st.session_state.results_df = st.data_editor(
                st.session_state.results_df,
                # num_rows="dynamic",
                disabled=["Column 3"],  # col 4 & 5 remain editable
                # hide_index=True,
                key="editor"
            )
        

            st.metric("Final Score", score)

        # Show insights
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("### 🚩 Red Flags")
            if flags:
                for f in flags:
                    st.error(f)
            else:
                st.success("No major red flags detected.")
        with col2:
            st.markdown("### 💡 Recommendations")
            for r in recommendations:
                st.info(r)

        
        col1, col2 = st.columns([1, 1])
        with col1:
            # Line chart
            st.markdown("### 📈 Trends from Data")
            st.line_chart(
                st.session_state.results_df[["Score", "Threshold"]],
                use_container_width=True
            )
        with col2:
            # Line chart
            st.markdown("### 📈 Trends from Data")
            st.line_chart(
                st.session_state.results_df[["Score", "Benchmark_normalized"]],
                use_container_width=True
            )
        
        # Buttons at bottom
        col_left, col_mid, col_right = st.columns([1, 1, 1])
        with col_left:
            if st.button("🔄 Analyse Again"):
                # st.session_state.results_df = analyze_results(st.session_state.results_df)
                final_score, flags, recommendations = analyze_results(st.session_state.results_df)
                st.session_state.score = final_score
                st.session_state.flags = flags
                st.session_state.recommendations = recommendations
                st.rerun()
        with col_right:
            if st.button("⬅️ Download Report"):
                # here download code should be there
                st.session_state.show_results = False
                st.rerun()
        with col_right:
            if st.button("⬅️ Back to Uploads"):
                st.session_state.show_results = False
                st.rerun()

if __name__ == "__main__":
    main()
