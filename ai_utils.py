import requests
import json
import random
import re

def get_api_config():
    try:
        with open('ollama_api.json', 'r') as f:
            content = f.read()
            # Basic parsing of the pseudo-python file
            url_match = re.search(r'URL\s*=\s*"([^"]+)"', content)
            model_match = re.search(r'MODEL\s*=\s*"([^"]+)"', content)
            keys_match = re.search(r'API_KEYS\s*=\s*\[(.*?)\]', content, re.DOTALL)
            
            url = url_match.group(1) if url_match else "https://ollama.com/api/generate"
            model = model_match.group(1) if model_match else "gpt-oss:120b"
            keys = []
            if keys_match:
                # Extract strings from the list
                keys = re.findall(r'"([^"]+)"', keys_match.group(1))
            
            return url, model, keys
    except Exception as e:
        print(f"Error reading ollama_api.json: {e}")
        return None, None, []

def generate_ai_content(prompt, system_prompt="You are an expert manga analyst and SEO copywriter."):
    url, model, keys = get_api_config()
    if not keys:
        return None
    
    key = random.choice(keys)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False
    }
    
    try:
        # Note: We use a timeout to avoid hangs
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"API Exception: {e}")
        return None

def get_chapter_article_ai(chapter_title):
    prompt = f"""
    Write a cinematic, pro-tier Gothic Noir thematic analysis article for Death Note chapter: "{chapter_title}".
    The tone should be investigative, dark, and analytical.
    Focus on the psychological tension, the clash of ideologies (Kira vs L), and the atmosphere.
    Use high-level vocabulary. Include a section on "Investigative Takeaway".
    Output in HTML format:
    <h2>ANALYSIS: {chapter_title}</h2>
    <p>... introductory paragraph about the psychological stakes ...</p>
    <p>... deep dive into the specific chapter themes and character maneuvers ...</p>
    <p><b>Investigative Takeaway:</b> ... a sharp, cold conclusion ...</p>
    """
    
    content = generate_ai_content(prompt)
    return content
