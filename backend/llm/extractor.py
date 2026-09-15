"""Design attribute extractor using NVIDIA NIM API (OpenAI-compatible) and intelligent fallback."""

from __future__ import annotations
import json
import logging
import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from openai import OpenAI

from config import NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_MODEL

logger = logging.getLogger("uvicorn")


class ExtractedDesignAttributes(BaseModel):
    """Structured design attributes extracted from user prompt."""
    minimal_ornate: float = Field(0.5, ge=0.0, le=1.0)
    modern_classic: float = Field(0.5, ge=0.0, le=1.0)
    playful_serious: float = Field(0.5, ge=0.0, le=1.0)
    warm_cool: float = Field(0.5, ge=0.0, le=1.0)
    bold_delicate: float = Field(0.5, ge=0.0, le=1.0)
    detected_industry: str = "tech"
    suggested_tagline: str = ""
    suggested_shape: str = "hex_interlock"
    suggested_layout: str = "horizontal"
    is_llm_powered: bool = False


SYSTEM_PROMPT = """You are an expert Brand Identity & Art Director AI.
Your task is to analyze a brand name, industry, and freeform style description,
and translate them into structured numeric aesthetic dimensions and layout suggestions.

Output ONLY a single valid JSON object with the following schema:
{
  "minimal_ornate": float between 0.0 (ultra-minimal/clean) and 1.0 (ornate/complex),
  "modern_classic": float between 0.0 (traditional/heritage/vintage) and 1.0 (modern/futuristic),
  "playful_serious": float between 0.0 (formal/serious/corporate) and 1.0 (playful/friendly/casual),
  "warm_cool": float between 0.0 (cool/cold/tech) and 1.0 (warm/earthy/vibrant),
  "bold_delicate": float between 0.0 (delicate/fine-line) and 1.0 (bold/heavy/solid),
  "detected_industry": string matching one of ["finance", "tech", "health", "creative", "eco", "food", "retail", "luxury"],
  "suggested_tagline": short catchy 2-4 word tagline suited for the brand,
  "suggested_shape": one of ["hex_interlock", "lettermark_geometric", "dynamic_arcs", "shield_minimal", "nodes_network", "circular_orbit", "botanical_spiral"],
  "suggested_layout": one of ["horizontal", "stacked", "badge"]
}

Important Rules:
- Return strictly raw JSON. No markdown, no triple backticks, no conversational text.
- Normalize all float values strictly between 0.0 and 1.0.
"""


def extract_attributes_with_nim(
    brand_name: str,
    industry: str,
    style_description: str,
    preferred_color: Optional[str] = None,
) -> ExtractedDesignAttributes:
    """Invokes NVIDIA NIM API using OpenAI SDK to extract structured design attributes."""
    if not NVIDIA_API_KEY:
        logger.info("NVIDIA_API_KEY not set. Using intelligent heuristic attribute extractor.")
        return fallback_heuristic_extractor(brand_name, industry, style_description, preferred_color)

    try:
        client = OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY,
            timeout=15.0,
        )

        user_content = (
            f"Brand Name: {brand_name}\n"
            f"Industry: {industry}\n"
            f"Style Description: {style_description}\n"
            f"Preferred Color: {preferred_color or 'None'}"
        )

        response = client.chat.completions.create(
            model=NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
            max_tokens=300,
        )

        content = response.choices[0].message.content.strip()
        
        # Clean any markdown fences if present
        clean_json = re.sub(r"^```json\s*|\s*```$", "", content, flags=re.MULTILINE).strip()
        parsed = json.loads(clean_json)

        return ExtractedDesignAttributes(
            minimal_ornate=max(0.0, min(1.0, float(parsed.get("minimal_ornate", 0.5)))),
            modern_classic=max(0.0, min(1.0, float(parsed.get("modern_classic", 0.5)))),
            playful_serious=max(0.0, min(1.0, float(parsed.get("playful_serious", 0.5)))),
            warm_cool=max(0.0, min(1.0, float(parsed.get("warm_cool", 0.5)))),
            bold_delicate=max(0.0, min(1.0, float(parsed.get("bold_delicate", 0.5)))),
            detected_industry=str(parsed.get("detected_industry", industry)).lower().strip(),
            suggested_tagline=str(parsed.get("suggested_tagline", "")),
            suggested_shape=str(parsed.get("suggested_shape", "hex_interlock")),
            suggested_layout=str(parsed.get("suggested_layout", "horizontal")),
            is_llm_powered=True,
        )

    except Exception as e:
        logger.warning(f"NVIDIA NIM API call failed ({e}). Falling back to heuristic extractor.")
        return fallback_heuristic_extractor(brand_name, industry, style_description, preferred_color)


def fallback_heuristic_extractor(
    brand_name: str,
    industry: str,
    style_description: str,
    preferred_color: Optional[str] = None,
) -> ExtractedDesignAttributes:
    """Deterministic NLP heuristic extractor when offline or without API key."""
    text = f"{industry} {style_description} {preferred_color or ''}".lower()

    # Defaults
    minimal_ornate = 0.5
    modern_classic = 0.5
    playful_serious = 0.5
    warm_cool = 0.5
    bold_delicate = 0.5

    # 1. Minimalism vs Ornate
    if any(w in text for w in ["minimal", "clean", "simple", "flat", "sleek", "sparse"]):
        minimal_ornate = 0.15
    elif any(w in text for w in ["ornate", "detailed", "decorative", "complex", "intricate"]):
        minimal_ornate = 0.75

    # 2. Modern vs Classic
    if any(w in text for w in ["modern", "futuristic", "cutting-edge", "tech", "future", "digital", "ai"]):
        modern_classic = 0.90
    elif any(w in text for w in ["classic", "vintage", "retro", "heritage", "traditional", "historic"]):
        modern_classic = 0.25

    # 3. Playful vs Serious
    if any(w in text for w in ["fun", "playful", "friendly", "whimsical", "casual", "quirky", "young"]):
        playful_serious = 0.75
    elif any(w in text for w in ["serious", "formal", "corporate", "trustworthy", "institutional", "secure"]):
        playful_serious = 0.15

    # 4. Warm vs Cool
    if any(w in text for w in ["warm", "earthy", "cozy", "organic", "sun", "fire", "orange", "yellow", "red"]):
        warm_cool = 0.80
    elif any(w in text for w in ["cool", "ice", "blue", "cyan", "digital", "slate", "tech", "navy"]):
        warm_cool = 0.20

    # 5. Bold vs Delicate
    if any(w in text for w in ["bold", "heavy", "powerful", "strong", "brutalist", "punchy", "solid"]):
        bold_delicate = 0.85
    elif any(w in text for w in ["delicate", "fine", "light", "subtle", "thin", "graceful"]):
        bold_delicate = 0.25

    # Map industry
    ind = industry.lower().strip()
    detected_industry = "tech"
    shape = "hex_interlock"
    layout = "horizontal"

    if any(w in ind for w in ["finan", "bank", "wealth", "crypto", "pay"]):
        detected_industry = "finance"
        shape = "hex_interlock" if modern_classic > 0.6 else "shield_minimal"
    elif any(w in ind for w in ["tech", "soft", "saas", "ai", "cloud", "data"]):
        detected_industry = "tech"
        shape = "nodes_network" if "ai" in text else "dynamic_arcs"
    elif any(w in ind for w in ["health", "med", "well", "care"]):
        detected_industry = "health"
        shape = "circular_orbit" if minimal_ornate < 0.3 else "botanical_spiral"
    elif any(w in ind for w in ["creat", "art", "design", "studio", "media"]):
        detected_industry = "creative"
        shape = "lettermark_geometric"
    elif any(w in ind for w in ["eco", "green", "natur", "bio", "plant"]):
        detected_industry = "eco"
        shape = "botanical_spiral"
    elif any(w in ind for w in ["food", "cafe", "coffee", "bistro", "restaur"]):
        detected_industry = "food"
        shape = "circular_orbit"
        layout = "stacked"
    elif any(w in ind for w in ["luxur", "hotel", "resort", "elite"]):
        detected_industry = "luxury"
        shape = "shield_minimal"
        layout = "badge"
    elif any(w in ind for w in ["retail", "fashion", "shop", "wear"]):
        detected_industry = "retail"
        shape = "lettermark_geometric"

    return ExtractedDesignAttributes(
        minimal_ornate=minimal_ornate,
        modern_classic=modern_classic,
        playful_serious=playful_serious,
        warm_cool=warm_cool,
        bold_delicate=bold_delicate,
        detected_industry=detected_industry,
        suggested_tagline=f"Innovating {industry.title()}" if industry else "Excellence in Motion",
        suggested_shape=shape,
        suggested_layout=layout,
        is_llm_powered=False,
    )
