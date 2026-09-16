<div align="center">

# 🎨 AI/ML SVG Logo Generator
### An AI/ML-Driven Vector Identity Synthesis Platform
*College AI/ML Mini Project*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM_API-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

<br />

<p align="center">
  <b>Transforming natural language brand descriptions into harmonized, scalable SVG vector logos through LLM aesthetic extraction, learned $k$-NN metric retrieval, and procedural vector geometry.</b>
</p>

[Quick Start](#-quick-start) • [System Architecture](#-system-architecture) • [Project Team](#-project-team) • [Viva Defense Guide](#-viva-defense--technical-justification) • [Colab Notebook](#-google-colab-notebook) • [API Reference](#-api-reference)

</div>

---

## 👥 Project Team

| Name | Role & Core Contributions |
| :--- | :--- |
| **🌟 Rachit Jain** | **System & Design Architecture Lead**<br>• End-to-end system design & aesthetic vector space architecture<br>• ML recommender & LLM pipeline workflow orchestration<br>• Core procedural engine design & integration architecture |
| **🌟 Ruchika Parashar** | **AI/ML & Knowledge Base Lead**<br>• Curated aesthetic catalog dataset schema (`design_catalog.json`)<br>• Scikit-Learn $k$-NN metric retrieval pipeline & feature scaling<br>• NVIDIA NIM LLM structured prompt engineering & attribute extraction |
| **🌟 Yash Singhal** | **Full-Stack & Procedural Engine Lead**<br>• Procedural SVG geometric primitive generators & layouts<br>• FastAPI REST service, CORS middleware & TestClient test suite<br>• React + Vite interactive UI, real-time manual override controls & export pipeline |

---

## 🏛️ System Architecture

```
                 [ USER INPUT ]
     (Brand Name, Industry, Style Description)
                        │
                        ▼
            ┌───────────────────────┐
            │   NVIDIA NIM LLM      │ ◄── Model: nvidia/nemotron-3-super-120b-a12b
            │ (OpenAI-Compatible)   │     Extracts continuous 5D aesthetic axes
            └───────────┬───────────┘
                        │
                        ▼
      [ 5D Normalized Continuous Vector ]
   • minimal_ornate  [0.0 - 1.0]   • warm_cool     [0.0 - 1.0]
   • modern_classic  [0.0 - 1.0]   • bold_delicate [0.0 - 1.0]
   • playful_serious [0.0 - 1.0]   • industry tag  [categorical]
                        │
                        ▼
            ┌───────────────────────┐
            │ Scikit-Learn Pipeline │ ◄── StandardScaler + OneHotEncoder
            │     k-NN Model        │     Metric: Cosine Similarity
            └───────────┬───────────┘
                        │
                        ▼
    [ Top-k Harmonious Palettes & Typography ]
   • Primary, Secondary, Accent, Background, Text Hexes
   • Curated Google Fonts Pairings (Header + Tagline)
                        │
                        ▼
            ┌───────────────────────┐
            │ Procedural SVG Engine │ ◄── Math-driven geometric paths
            │ (XML Synthesizer)     │     Dynamic ViewBox, Gradients & Fonts
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   React + Vite App    │ ◄── Live SVG Canvas Preview
            │   (Frontend UI)       │     Real-Time Manual Overrides
            │                       │     Export as SVG & High-Res PNG
            └───────────────────────┘
```

---

## 🚀 Quick Start

### ⚡ Option 1: One-Click Launcher (Windows)
Simply double-click the included batch script in the root directory:
```powershell
start_app.bat
```
*This simultaneously starts both the FastAPI backend (`port 8000`) and the Vite React frontend (`port 5173`).*

---

### 💻 Option 2: Manual Terminal Startup

<details>
<summary><b>Click to expand manual setup instructions</b></summary>

#### Step 1: Clone Repository
```bash
git clone https://github.com/rachitjain2/SVG-Logo-Generator.git
cd SVG-Logo-Generator
```

#### Step 2: Start Backend Server
```powershell
# From project root:
cd backend
..\.venv\Scripts\python.exe -m uvicorn app:app --port 8000 --reload
```
*Backend runs at `http://127.0.0.1:8000` with interactive Swagger docs at `http://127.0.0.1:8000/docs`.*

#### Step 3: Start React Frontend
```powershell
# In a second terminal from project root:
cd frontend
npm run dev
```
*Open your browser at `http://localhost:5173`.*

</details>

---

## 🎓 Viva Defense & Technical Justification

<details open>
<summary><b>🔍 1. Why $k$-NN Metric Retrieval instead of Hardcoded Rules or Black-Box Classifiers?</b></summary>

> [!IMPORTANT]
> **Key Viva Defense Point**:
> - **Failure of Rule-Based Systems**: A system of `if-else` rules cannot scale across infinite combinations of continuous aesthetic nuances (e.g., a "subtly playful but mostly corporate tech firm with warm undertones").
> - **Failure of Standard Classifiers**: Palette and typography pairings are **not mutually exclusive classes**. A multiclass classification model would suffer severe class collapse and combinatorial explosion ($N$ palettes $\times$ $M$ font pairings).
> - **Why $k$-NN Content-Based Retrieval?**:
>   1. We embed design profiles as dense vectors in a continuous aesthetic space.
>   2. $k$-NN computes angular alignment using **Cosine Similarity**:
>      $$\text{Similarity}(\mathbf{u}, \mathbf{v}) = 1 - d_{\text{cosine}}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$$
>   3. Directly powers **top-$k$ candidate ranking**, enabling instant "Regenerate Variation" and "Alternative Recommendations" features.
>   4. Provides complete **mathematical explainability** (e.g., *"Matched Nordic Slate at 98.9% similarity due to $\Delta=0.00$ on minimalism and tone"*).

</details>

<details>
<summary><b>📊 2. Feature Preprocessing & Scaling Pipeline</b></summary>

The recommender utilizes scikit-learn's `ColumnTransformer` joining:
1. **`StandardScaler`**: Scales continuous axes to zero mean ($\mu = 0$) and unit variance ($\sigma = 1$), preventing dimensions with larger variance from dominating the distance metric.
2. **`OneHotEncoder(handle_unknown='ignore')`**: Categorically encodes the 8 industry domains (`finance`, `tech`, `health`, `creative`, `eco`, `food`, `retail`, `luxury`).
3. **`NearestNeighbors(metric='cosine', algorithm='brute')`**: Evaluates angular distance across the transformed feature matrix.

</details>

<details>
<summary><b>💬 3. Common Viva Questions & Model Answers</b></summary>

* **Q: How does the system handle an unknown or novel industry?**
  * **A**: The `OneHotEncoder` is configured with `handle_unknown='ignore'`, producing a zero vector for unseen industries. The recommender gracefully falls back to the 5 continuous aesthetic dimensions to find the closest aesthetic match.
* **Q: Is the SVG rasterized or true vector?**
  * **A**: It is 100% mathematically constructed XML vector geometry (`<path>`, `<rect>`, `<circle>`, `<polygon>`) with embedded Google Fonts, ensuring zero quality loss at any resolution.
* **Q: How does the backend behave without an internet connection or API key?**
  * **A**: The backend features an automated NLP heuristic fallback that maps prompt keywords to continuous aesthetic ratings, allowing offline demonstrations and testing.

</details>

---

## 📓 Google Colab Notebook

We provide a self-contained Google Colab notebook for cloud-based training, visual validation, and viva presentations:

📁 **[`backend/ml/colab_recommender_notebook.ipynb`](backend/ml/colab_recommender_notebook.ipynb)**

<details>
<summary><b>Features included in the Colab Notebook:</b></summary>

- **Dependency Installation**: Runs without local hardware requirements.
- **2D PCA Projection Plot**: Uses Principal Component Analysis to plot the curated aesthetic space in 2D, illustrating how design styles cluster by industry domain.
- **Interactive Query Vector Tester**: Test arbitrary attribute sliders and verify similarity scores in real-time.

</details>

---

## 📐 Procedural Geometric Primitives

The SVG generation engine synthesizes 7 parametrized geometric shape archetypes:

| Shape Archetype | Typical Industries | Design Geometry & Description |
| :--- | :--- | :--- |
| **Isometric Hex / Cube** | Fintech, SaaS, Web3 | 3D isometric faceted cube with gradient highlights and floating center core |
| **Geometric Monogram** | Modern Agencies, Fashion | Squircle framed badge enclosing the brand's initial letter with accent cutouts |
| **Dynamic Motion Arcs** | Cloud, Analytics, Energy | Dual intersecting kinetic curved arcs with orbital satellite nodes |
| **Minimalist Shield** | Security, Wealth, Law | Faceted dual-tone protective crest with inner geometric chevron |
| **Neural / AI Nodes** | AI/ML, Data Science, Tech | Constellation graph of interconnected coordinate nodes and pulse emitters |
| **Concentric Orbits** | Biotech, Global Platforms | Modern planetary core encircled by dashed outer halos and satellite markers |
| **Organic Botanical** | Eco, Wellness, Food | Golden ratio / Fibonacci petal whorl radiating from an accent center |

---

## 🔌 API Reference

### 1. Generate Logo (`POST /api/generate`)
Executes the full pipeline: LLM extraction $\rightarrow$ ML recommender $\rightarrow$ procedural SVG generator.

```json
// Request Payload
{
  "brand_name": "Apex",
  "industry": "Finance",
  "style_description": "modern fintech, trustworthy, minimal, electric cyan",
  "preferred_color": "cyan"
}
```

```json
// Response Payload
{
  "svg": "<svg ...>...</svg>",
  "brand_name": "Apex",
  "tagline": "Next-Gen Fintech",
  "selected_palette": {
    "primary": "#0F172A",
    "secondary": "#0284C7",
    "accent": "#06B6D4",
    "background": "#FFFFFF",
    "text": "#0F172A"
  },
  "selected_typography": {
    "primary_font": "Space Grotesk",
    "secondary_font": "Inter",
    "weight": 700
  },
  "layout": "horizontal",
  "shape": "hex_interlock",
  "similarity_score": 0.989,
  "match_reasons": [
    "Direct industry domain match for 'finance'",
    "High aesthetic concordance on minimalism (diff=0.00)"
  ],
  "alternatives": [ ... ]
}
```

### 2. Instant Re-Render (`POST /api/re-render`)
Re-renders logo with user overrides in sub-10ms (zero LLM calls).

---

## 📂 Project Directory Layout

```
SVG-Logo-Generator/
├── backend/
│   ├── app.py                     # FastAPI REST server & CORS setup
│   ├── config.py                  # Environment config (NVIDIA_API_KEY)
│   ├── requirements.txt           # Python dependency specifications
│   ├── test_api.py                # In-memory API verification test suite
│   ├── ml/
│   │   ├── dataset.py             # Pydantic schemas & catalog loader
│   │   ├── recommender.py         # Scikit-learn k-NN pipeline & explainability
│   │   ├── evaluate.py            # Standalone evaluation test script
│   │   ├── colab_recommender_notebook.ipynb # Google Colab notebook
│   │   └── data/
│   │       └── design_catalog.json # 24 curated aesthetic profiles
│   ├── llm/
│   │   └── extractor.py           # NVIDIA NIM client with heuristic fallback
│   └── svg_engine/
│       ├── primitives.py          # 7 geometric shape generators
│       ├── layouts.py             # Horizontal, Stacked, and Badge layouts
│       ├── generator.py           # Logo assembler & Google Fonts embedding
│       └── test_generator.py      # Standalone SVG output verification
├── frontend/
│   ├── package.json               # React + Vite dependencies
│   ├── vite.config.js             # API proxy configuration
│   ├── index.html                 # HTML template with Google Fonts
│   └── src/
│       ├── App.jsx                # Main unified interface
│       ├── index.css              # Glassmorphic dark/light styling
│       ├── components/
│       │   ├── InputForm.jsx      # Minimal 3-field input form
│       │   ├── LogoPreview.jsx    # SVG canvas, zoom, SVG/PNG export
│       │   ├── OverridePanel.jsx  # Color pickers, typography, shapes
│       │   └── AlternativesDrawer.jsx # Top-k ML candidates drawer
│       └── services/
│           └── api.js             # Frontend API client
├── start_app.bat                  # Single-click Windows application launcher
├── test_e2e.py                    # End-to-end integration test
└── README.md                      # Interactive project documentation
```

---

<div align="center">
  <b>Developed for College AI/ML Mini Project by Rachit Jain, Ruchika Parashar &amp; Yash Singhal</b><br>
  <i>Empowering procedural generative design through Machine Learning</i>
</div>
