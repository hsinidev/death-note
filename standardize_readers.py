import os
import re
import random
import json
from ai_utils import get_chapter_article_ai

# Cache for AI articles to avoid redundant API calls
CACHE_FILE = 'article_cache.json'
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)

cache = load_cache()

def generate_chapter_article(title):
    themes = [
        "the psychological tension between intellectual titans",
        "the moral ambiguity of absolute justice",
        "the intricate rules of the Shinigami realm",
        "the societal impact of Kira's perceived divinity",
        "the breakdown of traditional investigative protocols",
        "the high-stakes game of cat and mouse",
        "the tragic descent of a brilliant mind",
        "the influence of supernatural entities on human destiny"
    ]
    
    opening = [
        f"In {title}, we witness a pivotal moment where {random.choice(themes)} taking center stage.",
        f"The events of {title} further deepen the complex narrative of Death Note, particularly exploring {random.choice(themes)}.",
        f"As the investigation reaches a fever pitch in {title}, the focus shifts toward {random.choice(themes)}."
    ]
    
    middle = [
        "Light Yagami's calculated maneuvers are met with equal brilliance from L, creating a gridlocked battlefield of logic.",
        "The introduction of new variables into the Kira case forces the Task Force to reconsider their baseline assumptions about justice.",
        "Ryuk's presence serves as a constant reminder of the alien nature of the power currently residing in the human world.",
        "The duality of Light's life as a top student and a self-proclaimed god continues to fracture under the pressure of the investigation."
    ]
    
    analysis = [
        f"Experts on the series frequently point to this chapter as a masterclass in suspense. The way the pacing mirrors the heartbeat of a cornered suspect is intentional and effective.",
        f"Visually and narratively, this section of the manga encapsulates the Gothic Noir aesthetic we strive to preserve in this portal.",
        f"The philosophical questions raised here regarding 'Good vs. Evil' are as relevant today as they were during the series' original run."
    ]
    
    footer = [
        f"Continue your study of the Death Note by proceeding to the next case file. The truth remains elusive, but the evidence is consistent.",
        f"Stay tuned for further analysis of the subsequent files in the Kira dossier.",
        f"The investigation is far from over. Study the pages above carefully for hidden clues."
    ]

    article = f"<h2>ANALYSIS: {title}</h2>"
    article += f"<p>{random.choice(opening)} {random.choice(middle)}</p>"
    article += f"<p>{random.choice(analysis)}</p>"
    article += f"<p><b>Key Investigative Takeaway:</b> {random.choice(themes).capitalize()}.</p>"
    article += f"<p>{random.choice(footer)}</p>"
    
    return article

chapters_dir = 'manga/Death Note'
template_file = 'reader.template.html'

def get_chapters():
    if not os.path.exists(chapters_dir):
        return []
    chapters = os.listdir(chapters_dir)
    
    def sort_key(s):
        match = re.search(r'Chapter[\s-]?(\d+)', s, re.IGNORECASE)
        if match:
            return (0, int(match.group(1)))
        return (1, s)
    
    return sorted(chapters, key=sort_key) # Regular order for prev/next logic

def standardize_readers():
    chapters = get_chapters()
    if not os.path.exists(template_file):
        print(f"Error: {template_file} not found.")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    # Generate Dropdown Links
    dropdown_html = ""
    for ch in chapters:
        # Use relative path since chapters are in subfolders
        dropdown_html += f'<a href="../{ch.replace(" ", "%20")}/index.html">{ch}</a>\n'

    for i, ch in enumerate(chapters):
        ch_path = os.path.join(chapters_dir, ch)
        if not os.path.isdir(ch_path):
            continue

        # Navigation
        first_ch = chapters[0].replace(" ", "%20")
        first_link = f'<a href="../{first_ch}/index.html" class="nav-btn" title="Case 1">« FIRST</a>'

        last_ch = chapters[-1].replace(" ", "%20")
        last_link = f'<a href="../{last_ch}/index.html" class="nav-btn" title="Last Case">LAST »</a>'

        prev_link = ""
        if i > 0:
            prev_ch = chapters[i-1].replace(" ", "%20")
            prev_link = f'<a href="../{prev_ch}/index.html" class="nav-btn">PREV</a>'
        
        next_link = ""
        if i < len(chapters) - 1:
            next_ch = chapters[i+1].replace(" ", "%20")
            next_link = f'<a href="../{next_ch}/index.html" class="nav-btn">NEXT</a>'

        # Images
        images = [f for f in os.listdir(ch_path) if f.lower().endswith('.avif')]
        # Get unique numeric bases (e.g., '01' from '01.avif')
        bases = sorted(list(set([os.path.splitext(img)[0] for img in images])), key=lambda x: int(re.sub(r'\D', '', x)) if re.sub(r'\D', '', x) else 0)
        
        reader_content = ""
        for base in bases:
            reader_content += f'''        <img data-src="{base}.avif" alt="Page {base}" class="reader-img">'''

        # Generate Article & Schema
        ch_title = ch.replace("-", " ")
        
        # Try AI generation first
        if ch in cache:
            chapter_article = cache[ch]
        else:
            print(f"Requesting AI article for {ch}...")
            chapter_article = get_chapter_article_ai(ch_title)
            if chapter_article:
                cache[ch] = chapter_article
                save_cache(cache)
            else:
                print(f"AI failed for {ch}, falling back to template.")
                chapter_article = generate_chapter_article(ch_title)
        
        schema_json = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"Read Death Note {ch_title} Online - Analysis & Review",
            "description": f"Deep psychological analysis and read-through of Death Note {ch_title}. Optimized for the Gothic Noir portal.",
            "author": {"@type": "Organization", "name": "Kira Task Force"},
            "publisher": {"@type": "Organization", "name": "Death Note Online"},
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://deathnote-online.com/manga/Death%20Note/{ch.replace(' ', '%20')}/index.html"}
        }

        # Render
        html = template.format(
            chapter_title=ch_title,
            reader_content=reader_content,
            chapter_article=chapter_article,
            SCHEMA_JSON=json.dumps(schema_json, indent=4),
            prev_link=prev_link,
            next_link=next_link,
            first_link=first_link,
            last_link=last_link,
            DROPDOWN_LINKS=dropdown_html
        )

        with open(os.path.join(ch_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        
        if i % 20 == 0:
            print(f"Processed {i}/{len(chapters)} chapters...")

    print(f"Successfully standardized {len(chapters)} chapter readers.")

if __name__ == "__main__":
    standardize_readers()
