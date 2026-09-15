"""FastAPI Web Server for AI/ML SVG Logo Generator.

Wires up NVIDIA NIM LLM attribute extraction, scikit-learn ML recommender,
and procedural SVG synthesis into high-performance REST API endpoints.
"""

from __future__ import annotations
import random
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from config import NVIDIA_API_KEY, NVIDIA_MODEL
from ml.recommender import DesignRecommender
from llm.extractor import extract_attributes_with_nim, ExtractedDesignAttributes
from svg_engine.generator import generate_logo
from svg_engine.primitives import SHAPE_DISPATCHER
from svg_engine.layouts import LAYOUT_DISPATCHER

app = FastAPI(
    title="AI/ML SVG Logo Generator API",
    description="Procedural & ML-driven SVG Logo Generation Service",
    version="1.0.0",
)

# Enable CORS for React frontend (Vite default is 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global singleton recommender (trained on startup)
recommender: Optional[DesignRecommender] = None


@app.on_event("startup")
def startup_event():
    """Initializes and trains the ML recommender on startup."""
    global recommender
    recommender = DesignRecommender()


# Request/Response Schemas
class GenerateRequest(BaseModel):
    brand_name: str = Field(..., min_length=1, max_length=50, description="Brand or company name")
    industry: str = Field(..., min_length=1, max_length=50, description="Industry domain")
    style_description: str = Field(..., min_length=1, max_length=300, description="Style keywords / mood prompt")
    preferred_color: Optional[str] = Field(None, max_length=50, description="Optional color bias or hex code")


class ReRenderRequest(BaseModel):
    brand_name: str
    tagline: Optional[str] = ""
    palette: Dict[str, str]
    typography: Dict[str, Any]
    layout_type: str = "horizontal"
    shape_type: str = "hex_interlock"
    seed: int = 42


@app.get("/api/health")
def health_check():
    """Health status and LLM capability check."""
    return {
        "status": "healthy",
        "llm_model": NVIDIA_MODEL,
        "has_nvidia_api_key": bool(NVIDIA_API_KEY),
        "recommender_ready": recommender is not None,
    }


@app.get("/api/options")
def get_options():
    """Returns supported shapes, layouts, and curated font lists for the frontend overrides."""
    return {
        "shapes": [
            {"id": "hex_interlock", "name": "Isometric Hex / Cube", "category": "tech"},
            {"id": "lettermark_geometric", "name": "Geometric Monogram", "category": "modern"},
            {"id": "dynamic_arcs", "name": "Dynamic Motion Arcs", "category": "motion"},
            {"id": "shield_minimal", "name": "Minimalist Shield", "category": "prestige"},
            {"id": "nodes_network", "name": "Neural / AI Nodes", "category": "data"},
            {"id": "circular_orbit", "name": "Concentric Orbits", "category": "clean"},
            {"id": "botanical_spiral", "name": "Organic Botanical", "category": "nature"},
        ],
        "layouts": [
            {"id": "horizontal", "name": "Horizontal (Icon Left)"},
            {"id": "stacked", "name": "Stacked (Icon Top)"},
            {"id": "badge", "name": "Badge / Emblem (Framed)"},
        ],
        "fonts": [
            "Space Grotesk",
            "Inter",
            "Cinzel",
            "Syne",
            "Outfit",
            "Plus Jakarta Sans",
            "Fraunces",
            "Playfair Display",
            "Poppins",
            "Lato",
            "Lora",
        ],
    }


@app.post("/api/generate")
def generate_endpoint(req: GenerateRequest):
    """Full AI/ML Pipeline: LLM Extraction -> ML Recommendation -> SVG Procedural Generation."""
    if recommender is None:
        raise HTTPException(status_code=500, detail="ML Recommender not initialized")

    # Step 1: Attribute Extraction via NVIDIA NIM LLM (or heuristic fallback)
    extracted: ExtractedDesignAttributes = extract_attributes_with_nim(
        brand_name=req.brand_name,
        industry=req.industry,
        style_description=req.style_description,
        preferred_color=req.preferred_color,
    )

    # Step 2: Retrieve Top ML Recommendations from Scikit-Learn Recommender
    recs = recommender.recommend(
        attributes=extracted.model_dump(),
        industry=extracted.detected_industry,
        k=4,
        preferred_color=req.preferred_color,
    )

    if not recs:
        raise HTTPException(status_code=500, detail="No matching recommendations found")

    top_rec = recs[0]
    palette = top_rec["palette"]
    typography = top_rec["typography"]

    # Select shape and layout
    shape = extracted.suggested_shape
    if shape not in SHAPE_DISPATCHER:
        shape = top_rec["shape_affinity"][0] if top_rec["shape_affinity"] else "hex_interlock"

    layout = extracted.suggested_layout
    if layout not in LAYOUT_DISPATCHER:
        layout = "horizontal"

    seed = random.randint(100, 99999)
    tagline = extracted.suggested_tagline or req.industry.title()

    # Step 3: Procedural SVG Synthesis
    svg = generate_logo(
        brand_name=req.brand_name,
        tagline=tagline,
        palette=palette,
        typography=typography,
        layout_type=layout,
        shape_type=shape,
        seed=seed,
    )

    return {
        "svg": svg,
        "brand_name": req.brand_name,
        "tagline": tagline,
        "extracted_attributes": extracted.model_dump(),
        "selected_palette": palette,
        "selected_typography": typography,
        "layout": layout,
        "shape": shape,
        "seed": seed,
        "similarity_score": top_rec["similarity_score"],
        "match_reasons": top_rec["match_reasons"],
        "alternatives": [
            {
                "id": r["profile"].id,
                "name": r["profile"].name,
                "similarity_score": r["similarity_score"],
                "palette": r["palette"],
                "typography": r["typography"],
                "shape_affinity": r["shape_affinity"],
                "match_reasons": r["match_reasons"],
            }
            for r in recs
        ],
        "is_llm_powered": extracted.is_llm_powered,
    }


@app.post("/api/re-render")
def re_render_endpoint(req: ReRenderRequest):
    """Instantaneous re-render endpoint for manual overrides (sub-10ms, zero LLM calls)."""
    svg = generate_logo(
        brand_name=req.brand_name,
        tagline=req.tagline or "",
        palette=req.palette,
        typography=req.typography,
        layout_type=req.layout_type,
        shape_type=req.shape_type,
        seed=req.seed,
    )
    return {"svg": svg}
