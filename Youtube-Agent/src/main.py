import streamlit as st
from services.youtube_service import YouTubeService
from services.rag_service import RAGService
from services.llm_service import LLMService
import logging
import os
from dotenv import load_dotenv

# Temporary debug
load_dotenv()  # Load .env file
print("GROQ_API_KEY exists:", "GROQ_API_KEY" in os.environ)
print("Current working directory:", os.getcwd())
print("Files in directory:", os.listdir('.'))

def main():
    st.title("YouTube Transcript Q&A System")
    st.write("Enter a YouTube video URL and ask questions about its content.")

    video_url = st.text_input(
        "YouTube Video URL", 
        placeholder="https://www.youtube.com/watch?v=..."
    )

    if not video_url:
        return

    video_id = YouTubeService.extract_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL")
        return

    with st.spinner("Fetching and processing transcript..."):
        try:
            transcript = YouTubeService.get_transcript(video_id)
            if not transcript:
                st.error("No transcript available for this video")
                return

            st.success("Transcript loaded successfully!")
            
            rag_service = RAGService()
            llm_service = LLMService()
            rag_chain = rag_service.create_pipeline(transcript)

            question = st.text_input(
                "Ask a question about the video:",
                placeholder="What is discussed in the video?"
            )

            if question:
                with st.spinner("Generating answer..."):
                    try:
                        # Chain is missing the LLM step - we need to connect it
                        prompt = rag_chain.invoke(question)
                        answer = llm_service.generate_response(prompt)
                        st.write("**Answer:**")
                        st.write(answer)
                    except Exception as e:
                        logging.error(f"Answer generation failed: {e}")
                        st.error("Failed to generate answer")

        except Exception as e:
            logging.error(f"Application error: {e}")
            st.error("An error occurred while processing your request")

if __name__ == "__main__":
    main()