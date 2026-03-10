from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from groq import Groq
import os
from dotenv import load_dotenv
from youtube_transcript_api.proxies import WebshareProxyConfig
load_dotenv()



def get_transcript(url):
    parsed_url = urlparse(url)
    ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.getenv("PROXY_USERNAME"),
        proxy_password=os.getenv("PROXY_PASSWORD"),
    )
)

    if parsed_url.netloc=='youtu.be':
        vid_id = parsed_url.path[1:]
    else:

        vid_id_dict = parse_qs(parsed_url.query)
        vid_id = vid_id_dict['v'][0]
    

    try:
        
        transcript_list = ytt_api.fetch(vid_id)
        transcript_text = " ".join([entry.text for entry in transcript_list])
        
        return transcript_text


    except Exception as e:
        return f"ERROR: {e}"

def chunk_text(text, chunk_size):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i: i+chunk_size]
        chunks.append(chunk)
    return chunks

    

def summarize(transcript_text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(model='llama-3.3-70b-versatile', messages=[{"role": "user", "content": f"Summarize the text: {transcript_text}"}] )
    return response.choices[0].message.content

'''
url = input("Enter Youtube Url: ")
transcript = get_transcript(url)
if transcript:
    chunks = chunk_text(transcript, 8000)
    mini_summaries = []
    for transcript in chunks:
        mini_summaries.append(summarize(transcript))
    final_summary = summarize(" ". join(mini_summaries))
    print(final_summary)
else:
    print("Error fetching your transcript")

'''