import os
import re
from ai_utils import get_chapter_article_ai, generate_ai_content

# Cache for Home Article
HOME_CACHE_FILE = 'home_article_cache.json'
def get_home_article():
    if os.path.exists(HOME_CACHE_FILE):
        with open(HOME_CACHE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    
    print("Generating AI article for home page...")
    prompt = """
    Write a cinematic, high-performance Gothic Noir thematic analysis for the main landing page of a Death Note manga portal.
    Title: THE KIRA DOSSIER: AN ANALYTICAL OVERVIEW.
    Focus on the "Investigative Terminal" aesthetic, the rivalry between Light and L, and the technical superiority of this archive.
    Mention the Gothic Noir design, AVIF/WebP optimization, and sub-second LCP.
    Output in HTML format with <h2>, <h3>, and <p> tags. Wrap in a <article class="chapter-article home-article">.
    """
    article = generate_ai_content(prompt)
    if not article:
        # Fallback
        article = '''
        <article class="chapter-article home-article">
            <h2>THE KIRA DOSSIER: AN ANALYTICAL OVERVIEW</h2>
            <p>Welcome to the most complete digital archive of the Death Note investigative history. This portal is more than a simple reader; it is an immersive environment designed to replicate the high-stakes atmosphere of the Kira Task Force headquarters.</p>
            <p>Our Gothic Noir interface is built on a foundation of performance, utilizing sub-second LCP architecture and next-gen image compression.</p>
        </article>
        '''
    
    with open(HOME_CACHE_FILE, 'w', encoding='utf-8') as f:
        f.write(article)
    return article

chapters_dir = 'manga/Death Note'
template_file = 'index.template.html'

def get_chapters():
    if not os.path.exists(chapters_dir):
        return []
    chapters = os.listdir(chapters_dir)
    
    # Sort chapters numerically
    def sort_key(s):
        # Match Chapter 1, Chapter-1, Chapter1, etc.
        match = re.search(r'Chapter[\s-]?(\d+)', s, re.IGNORECASE)
        if match:
            return (0, int(match.group(1)))
        return (1, s)
    
    return sorted(chapters, key=sort_key, reverse=True)

def generate_index():
    chapters = get_chapters()
    
    # Generate Dropdown Links
    dropdown_html = ""
    for ch in chapters:
        dropdown_html += f'<a href="manga/Death%20Note/{ch}/index.html">{ch}</a>\n'
    
    # Generate Cards
    cards_html = ""
    for ch in chapters:
        # Chapter identification for display
        num_match = re.search(r'Chapter[\s-]?(\d+)', ch, re.IGNORECASE)
        ch_display_num = f"CASE #{num_match.group(1)}" if num_match else "FILE EX"
        
        # Clean up name for title: Remove dashes and trim
        ch_display_name = re.sub(r'Chapter[\s-]?\d+[\s-]?', '', ch, flags=re.IGNORECASE)
        if not ch_display_name or ch_display_name.isspace():
            ch_display_name = ch.replace("-", " ")
        else:
            ch_display_name = ch_display_name.replace("-", " ").strip()
            # Restore chapter number to title if it was stripped
            if num_match:
                ch_display_name = f"Chapter {num_match.group(1)}: {ch_display_name}"
        
        # Image strategy: find the actual first image file in the chapter folder
        ch_path_url = f'manga/Death%20Note/{ch.replace(" ", "%20")}'
        ch_full_path = os.path.join(chapters_dir, ch)
        
        # Detect the actual first image filename
        first_img = '01.avif'  # default
        if os.path.exists(ch_full_path):
            img_files = sorted([f for f in os.listdir(ch_full_path) if f.endswith(('.avif', '.webp', '.jpg', '.png'))])
            if img_files:
                first_img = img_files[0]
        
        cards_html += f'''
        <a href="manga/Death%20Note/{ch.replace(" ", "%20")}/index.html" class="case-file">
            <div class="top-secret-stamp">TOP SECRET</div>
            
            <img src="{ch_path_url}/{first_img}" alt="{ch_display_name}" class="case-thumbnail" loading="lazy">

            <div class="case-header">
                <span class="case-number">{ch_display_num}</span>
            </div>
            
            <div class="case-content">
                <h3 class="case-title">{ch_display_name}</h3>
                <div class="case-status">STATUS: EVIDENCE FILED</div>
            </div>
        </a>
        '''

    # Read template and replace placeholders
    if not os.path.exists(template_file):
        print(f"Error: {template_file} not found.")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate Schema
    schema_json = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Death Note Online",
        "url": "https://deathnote-online.com",
        "description": "High-performance Gothic Noir Death Note manga portal.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://deathnote-online.com/index.html?q={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    }
    
    import json
    content = content.replace('{SCHEMA_JSON}', json.dumps(schema_json, indent=4))
    content = content.replace('<!-- CHAPTER_CARDS -->', cards_html)
    content = content.replace('<!-- DROPDOWN_LINKS -->', dropdown_html)
    content = content.replace('{HOME_ARTICLE}', get_home_article())
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully generated index.html with {len(chapters)} chapters.")

if __name__ == "__main__":
    generate_index()
