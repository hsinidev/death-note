# Death Note Shinigami Ledger

> **Vibe Focus:** Gothic Noir / Investigative Shinigami Journal  
> **Tech Stack:** Static HTML/JS + Tailwind CSS 4.0 + Python Generators

Welcome to the **Death Note Shinigami Ledger** web portal. This is a high-performance, immersive manga reader site designed specifically for fans of the series. The project leverages modern web optimization techniques to deliver a fast, localized, and beautiful experience.

---

## 🌟 Key Features

- Gothic ink-bleed background textures and serif typography.
- Interactive chapter indexes mimicking a detective case file.
- Gapless scrolling reader with automatic navigation controls.
- SEO-optimized comic-metadata schema mappings.

---

## 🛠️ Getting Started

### 📋 Prerequisites
- **For Web Server:** Python 3.10+ (to serve static files or run generators) or Node.js 18+ (if package dependencies are needed).
- **GitHub CLI (`gh`)**: Recommended for pushing updates.

### 🔑 API Key Configuration
This project includes automated content generation and SEO optimization scripts that use the **Zhipu AI / BigModel API**. 

To utilize these scripts:
1. Copy the `.env.example` file to create a `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your API key:
   ```env
   BIGMODEL_API_KEY=your_actual_api_key_here
   ```
   *Note: If you have multiple keys, you can specify them as a comma-separated list.*

---

## 🚀 Local Development

Run a local web server:
```bash
python -m http.server 8000
```

Then open your browser and navigate to the local server URL (usually `http://localhost:8000` or `http://localhost:5173`).

---

## 🤖 Content Generation & Automation
The project is equipped with local AI-powered generation scripts to build and update the site content dynamically.

You can run these scripts to regenerate and optimize the portal content:

- **`python generate_index.py`**: Builds the master case-file styled portal homepage.
- **`python generate_legal_pages.py`**: Compiles compliance policy pages.
- **`python performance_optimizer.py`**: Minifies scripts and compresses images for production.


---

## 📦 Production Deployment

Deploy the root static files directly to any static provider (Netlify, Vercel, GitHub Pages, or Nginx).

- **Ignored Assets:** Large `manga/` chapter image directories and local archives are excluded from this repository (configured in `.gitignore`) for performance and size constraints. Ensure image files are uploaded directly to your hosting server's path structure.
- **SEO Ready:** Sitemap (`sitemap.xml`) and `.htaccess` file rules are fully configured to rewrite paths and provide Google-friendly crawler access.
