import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Function to extract video ID from a YouTube URL
def extract_video_id(youtube_url):
    try:
        parsed_url = urlparse(youtube_url)
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query)['v'][0]
            elif parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
            elif parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
    except Exception:
        return None
    return None

# Function to format transcript into readable paragraphs
def format_transcript(transcript):
    paragraphs = []
    buffer = ""

    for entry in transcript:
        text = entry['text'].strip()
        # Break buffer on full stop or long line
        if text.endswith(('.', '?', '!')) and len(buffer) > 100:
            paragraphs.append(buffer + " " + text)
            buffer = ""
        else:
            buffer += " " + text
    if buffer:
        paragraphs.append(buffer)
    return paragraphs

# Streamlit UI
st.set_page_config(page_title="YouTube Transcript Reader", layout="wide")
st.title("📢 YouTube Transcript Reader & English Practice")

# Input field
youtube_url = st.text_input("🔗 Enter YouTube video URL:")

if youtube_url:
    video_id = extract_video_id(youtube_url)

    if video_id:
        try:
            st.success(f"✅ Extracted video ID: `{video_id}`")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            formatted_paragraphs = format_transcript(transcript)

            # Slow Reading Mode toggle
            slow_mode = st.checkbox("🐢 Enable Slow Reading Mode", value=False)

            # Apply styles
            font_size = "24px" if slow_mode else "20px"
            line_height = "2.2" if slow_mode else "1.6"
            spacing = "30px" if slow_mode else "20px"

            st.subheader("🗣️ Transcript to Read Aloud")

            for para in formatted_paragraphs:
                st.markdown(
                    f"<div style='font-size:{font_size}; line-height:{line_height}; margin-bottom:{spacing};'>{para.strip()}</div>",
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error("❌ Could not retrieve transcript.")
            st.code(str(e))
    else:
        st.warning("⚠️ Invalid YouTube URL. Please try again.")
else:
    st.info("Paste a YouTube video link above to begin.")
