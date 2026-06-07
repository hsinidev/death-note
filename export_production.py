import os
import shutil

source_dir = r"c:\Users\hsini\Desktop\website manga projects\Death Note"
out_dir = os.path.join(source_dir, "out")

# Clean the out directory first
if os.path.exists(out_dir):
    print("Cleaning existing out directory...")
    shutil.rmtree(out_dir)
os.makedirs(out_dir)

# Files directly needed for production
files_to_copy = [
    "index.html", 
    "index.css", 
    "about.html", 
    "contact.html", 
    "privacy-policy.html", 
    "dmca.html", 
    "terms.html", 
    "cookies.html", 
    "disclaimer.html", 
    "robots.txt", 
    "sitemap.xml", 
    ".htaccess",
    "background.png",
    "hero_kira.png",
    "hero_l.png"
]

for f in files_to_copy:
    src_path = os.path.join(source_dir, f)
    dst_path = os.path.join(out_dir, f)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied {f}")

# Copy the manga directory
manga_src = os.path.join(source_dir, "manga")
manga_dst = os.path.join(out_dir, "manga")

print("Copying manga contents... this might take a little bit of time depending on size.")
shutil.copytree(manga_src, manga_dst)
print("Finished copying manga data.")
print("Static site exported successfully in out folder!")
