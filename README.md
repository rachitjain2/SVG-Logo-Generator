# AI/ML SVG Logo Generator (College AI/ML Mini Project)

An AI/ML-driven vector logo generator web application. The system accepts brand identity inputs (brand name, industry, style description), uses an LLM (NVIDIA NIM API with `nvidia/nemotron-3-super-120b-a12b`) to extract continuous aesthetic design attributes, recommends a harmonious color palette and typography pairing using a trained **$k$-Nearest Neighbors ($k$-NN) Content-Based Recommender**, and procedurally synthesizes scalable, production-ready SVG logos with real-time manual override controls and SVG/PNG export.

---

## 🏛️ System Architecture

```
User Input (Brand Name, Industry, Style Description)
         │
         ▼
[NVIDIA NIM LLM API] ──► Extracts 5D Continuous Design Axes:
(`nvidia/nemotron-3-super-120b-a12b`)   • minimal_ornate  [0.0 - 1.0]
                                        • modern_classic  [0.0 - 1.0]
                                        • playful_serious [0.0 - 1.0]
                                        • warm_cool       [0.0 - 1.0]
                                        • bold_delicate   [0.0 - 1.0]
         │
         ▼
[Scikit-Learn ML Recommender] ────────► StandardScaler + OneHotEncoder
(k-NN with Cosine Distance Retrieval)    Retrieves Top-k Curated Aesthetic Matches
         │
         ▼
[Procedural SVG Engine] ──────────────► 7 Parametrized Geometric Primitives
(Math-driven XML Vector Synthesizer)     3 Layout Placements (Horizontal, Stacked, Badge)
                                        Embedded Google Fonts & Dynamic Gradients
         │
         ▼
[React + Vite Frontend] ──────────────► Live SVG Preview Canvas
                                        Regenerate Variations
                                        Real-Time Manual Overrides (Colors/Fonts/Layout)
                                        Export as SVG & High-Res PNG
```

---

## 🎓 Viva Defense & Technical Justification

### 1. Why $k$-NN Metric Retrieval instead of a Black-Box Classifier?
- **Problem**: Design aesthetics cannot be modeled as mutually exclusive discrete classes without severe class collapse and combinatorial explosion ($N$ palettes $\times$ $M$ font pairings).
- **Solution**: We represent design profiles as dense points in a multi-dimensional continuous-categorical aesthetic space. Content-Based Metric Retrieval using $k$-Nearest Neighbors ($k$-NN) finds the nearest exemplar brand aesthetics.
- **Top-$k$ Ranking**: Enables natural variation generation ("Regenerate Variation") by sampling from top-$k$ nearest neighbors.
- **Mathematical Explainability**: Angular alignment is quantified via cosine similarity:
  $$\text{Similarity}(\mathbf{u}, \mathbf{v}) = 1 - d_{\text{cosine}}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

### 2. Feature Preprocessing Pipeline
- **Continuous Features**: Scaled using `StandardScaler` (zero mean, unit variance) to ensure balanced dimensional weighting.
- **Categorical Features**: `OneHotEncoder` encodes the industry domain.
- Combined using scikit-learn `ColumnTransformer`.

### 3. Google Colab Notebook
- A complete experiment notebook is located at [`backend/ml/colab_recommender_notebook.ipynb`](backend/ml/colab_recommender_notebook.ipynb).
- Upload to Google Colab to run 2D PCA cluster visualizations, feature distributions, and interactive query testing without requiring local compute.

---

## 🚀 Quick Start (Running the Application)

### Option A: One-Click Launcher (Windows)
Double-click:
```powershell
start_app.bat
```
This automatically starts both the FastAPI backend (port 8000) and the Vite React frontend (port 5173).

---

### Option B: Manual Terminal Execution

#### 1. Start FastAPI Backend:
```powershell
# From project root:
cd backend
..\.venv\Scripts\python.exe -m uvicorn app:app --port 8000 --reload
```
*Backend runs at `http://127.0.0.1:8000` with interactive Swagger docs at `http://127.0.0.1:8000/docs`.*

#### 2. Start React Frontend:
```powershell
# From project root in a second terminal:
cd frontend
npm run dev
```
*Open `http://localhost:5173` in your browser.*

---

## 🔑 Environment Variables
To enable live NVIDIA NIM LLM attribute extraction, set your API key in `backend/.env`:
```env
NVIDIA_API_KEY="your_nvidia_nim_api_key_here"
```
*(If left empty, the application automatically uses its built-in heuristic NLP extractor so all features remain 100% operational offline).*

---

## 📂 Project Structure
```
SVG Logo generator/
├── backend/
│   ├── app.py                     # FastAPI REST server & CORS
│   ├── config.py                  # Environment config (NVIDIA_API_KEY)
│   ├── requirements.txt           # Python dependencies
│   ├── test_api.py                # In-memory API verification script
│   ├── ml/
│   │   ├── dataset.py             # Pydantic models & catalog loader
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
│       └── test_generator.py      # Standalone SVG output test
├── frontend/
│   ├── package.json
│   ├── vite.config.js             # Vite proxy configuration to /api
│   ├── index.html
│   └── src/
│       ├── App.jsx                # Main unified interface
│       ├── index.css              # Glassmorphic dark/light styling
│       ├── components/
│       │   ├── InputForm.jsx      # Minimal 3-field input form
│       │   ├── LogoPreview.jsx    # SVG canvas, zoom, SVG/PNG export
│       │   ├── OverridePanel.jsx  # Color pickers, typography, shapes
│       │   └── AlternativesDrawer.jsx # Top-k ML candidates drawer
│       └── services/
│           └── api.js             # Backend HTTP client
├── start_app.bat                  # One-click Windows runner
└── README.md                      # Documentation & viva defense guide
```
