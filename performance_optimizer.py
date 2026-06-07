import os
import subprocess

chapters_dir = 'manga/Death Note'
base_url = 'https://deathnote-manga.online'

def generate_sitemap(chapters):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += f'  <url><loc>{base_url}/index.html</loc><priority>1.0</priority></url>\n'
    for ch in chapters:
        xml += f'  <url><loc>{base_url}/manga/Death%20Note/{ch}/index.html</loc><priority>0.8</priority></url>\n'
    xml += '</urlset>'
    with open('sitemap.xml', 'w') as f:
        f.write(xml)

def generate_robots():
    content = "User-agent: *\nAllow: /\n"
    content += f"Sitemap: {base_url}/sitemap.xml\n"
    content += "Disallow: /out/\n"
    with open('robots.txt', 'w') as f:
        f.write(content)

import pillow_avif
from PIL import Image

def convert_to_avif(chapters):
    print("Starting AVIF optimization with Pillow...")
    for ch in chapters:
        ch_path = os.path.join(chapters_dir, ch)
        images = [f for f in os.listdir(ch_path) if f.lower().endswith(('.jpg', '.png'))]
        for img in images:
            source = os.path.join(ch_path, img)
            target = source.rsplit('.', 1)[0] + '.avif'
            if not os.path.exists(target):
                print(f"Converting {source} to {target}...")
                try:
                    with Image.open(source) as im:
                        # Convert to RGB if needed
                        if im.mode != "RGB":
                            im = im.convert("RGB")
                        im.save(target, format="AVIF", quality=75)
                except Exception as e:
                    print(f"Failed to convert {source}: {e}")
            else:
                pass

if __name__ == "__main__":
    if os.path.exists(chapters_dir):
        # Sort chapters naturally
        import re
        def natural_sort_key(s):
            return [int(text) if text.isdigit() else text.lower()
                    for text in re.split('([0-9]+)', s)]
        
        chapters = sorted(os.listdir(chapters_dir), key=natural_sort_key)
        generate_sitemap(chapters)
        generate_robots()
        convert_to_avif(chapters)
        print(f"Successfully optimized SEO and images for {len(chapters)} chapters.")
    else:
        print("Manga directory not found.")
