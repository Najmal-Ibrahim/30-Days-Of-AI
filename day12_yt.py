import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
# NEW: We use the official LangChain Loader
from langchain_community.document_loaders import YoutubeLoader

# 1. Page Config
st.set_page_config(page_title="TubeMind AI", page_icon="📺")
st.title("📺 TubeMind: YouTube Video Summarizer")
st.subheader("Paste a URL -> Get the Insights.")

# 2. Load Secrets
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

# 3. UI Layout
video_url = st.text_input("Enter YouTube Video URL:")
summarize_btn = st.button("Generate Summary")

if summarize_btn and video_url:
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        st.error("Please enter a valid YouTube URL.")
    else:
        # Show Thumbnail (Optional visual)
        try:
            video_id = video_url.split("v=")[1].split("&")[0]
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", width=300)
        except:
            pass # Ignore thumbnail errors if URL format is weird

        with st.spinner("🎧 Downloading Transcript..."):
            try:
                # --- THE MAGIC PART ---
                # LangChain handles the API calls for us
                 # We removed 'translation="en"' because it causes errors on some videos.
            # We also added 'en-GB' and 'auto' to catch more English variants.
                loader = YoutubeLoader.from_youtube_url(
                    video_url, 
                    add_video_info=False,
                    language=["en", "en-US", "en-GB"], 
                )
                docs = loader.load()
                
                # Combine text if multiple parts exist
                transcript_text = "\n".join([doc.page_content for doc in docs])
                
                # Success! Show raw text preview
                with st.expander("View Raw Transcript"):
                    st.write(transcript_text[:1000] + "...") 

                # 4. The Summarization
                with st.spinner("🧠 Llama-3 is summarizing..."):
                    llm = ChatGroq(
                        groq_api_key=groq_api_key, 
                        model_name="llama-3.3-70b-versatile"
                    )
                    
                    prompt = f"""
                    You are an expert Content Creator. Summarize this YouTube video.
                    
                    Structure:
                    1. 🎯 **Main Topic**: One sentence.
                    2. 🔑 **Key Takeaways**: 5 bullet points.
                    3. 💡 **Actionable Advice**: What should the viewer do?
                    
                    Transcript:
                    {transcript_text[:15000]}
                    """
                    
                    response = llm.invoke([HumanMessage(content=prompt)])
                    
                    st.markdown("### 📝 AI Summary")
                    st.markdown(response.content)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Tip: Ensure the video has Closed Captions (CC) enabled.")