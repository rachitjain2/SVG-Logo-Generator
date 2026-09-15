"""Dataset models and loader for curated design catalog."""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field


class DesignAttributes(BaseModel):
    """Normalized continuous design axes (0.0 to 1.0)."""
    minimal_ornate: float = Field(..., ge=0.0, le=1.0, description="0.0 = ultra-minimal, 1.0 = ornate/complex")
    modern_classic: float = Field(..., ge=0.0, le=1.0, description="0.0 = classic/heritage, 1.0 = modern/futuristic")
    playful_serious: float = Field(..., ge=0.0, le=1.0, description="0.0 = formal/corporate, 1.0 = playful/casual")
    warm_cool: float = Field(..., ge=0.0, le=1.0, description="0.0 = cool/cold, 1.0 = warm/vibrant")
    bold_delicate: float = Field(..., ge=0.0, le=1.0, description="0.0 = delicate/fine, 1.0 = bold/heavy")


class ColorPalette(BaseModel):
    """Hex color definitions for harmonious logo theming."""
    primary: str
    secondary: str
    accent: str
    background: str
    text: str


class Typography(BaseModel):
    """Typography pairing and styling specifications."""
    primary_font: str
    secondary_font: str
    font_category: str
    letter_spacing: str = "0.05em"
    weight: int = 700


class DesignProfile(BaseModel):
    """Curated brand aesthetic exemplar."""
    id: str
    name: str
    industry: str
    attributes: DesignAttributes
    palette: ColorPalette
    typography: Typography
    shape_affinity: List[str]
    keywords: List[str] = Field(default_factory=list)


def get_default_catalog_path() -> Path:
    """Returns absolute path to default design_catalog.json."""
    return Path(__file__).resolve().parent / "data" / "design_catalog.json"


def load_catalog(filepath: Optional[Path | str] = None) -> List[DesignProfile]:
    """Loads and validates design profiles from JSON catalog."""
    path = Path(filepath) if filepath else get_default_catalog_path()
    if not path.exists():
        raise FileNotFoundError(f"Design catalog not found at {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [DesignProfile.model_validate(item) for item in data]
