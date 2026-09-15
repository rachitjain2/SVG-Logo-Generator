"""Main SVG Logo Synthesizer.

Assembles geometric primitives, layout engines, Google Fonts embedding,
and dynamic gradient definitions into standalone, production-ready SVG logos.
"""

from __future__ import annotations
import urllib.parse
from typing import Dict, Any, Optional
from .layouts import LAYOUT_DISPATCHER, render_horizontal_layout


def get_google_font_url(primary_font: str, secondary_font: str) -> str:
    """Constructs valid Google Fonts @import stylesheet URL for embedded typography."""
    fonts = list(set([f.strip() for f in [primary_font, secondary_font] if f and f.strip()]))
    families = []
    for f in fonts:
        encoded = urllib.parse.quote_plus(f)
        families.append(f"family={encoded}:wght@400;500;600;700;800")
    
    query = "&".join(families)
    return f"https://fonts.googleapis.com/css2?{query}&amp;display=swap"


def generate_logo(
    brand_name: str,
    tagline: str = "",
    palette: Optional[Dict[str, str]] = None,
    typography: Optional[Dict[str, Any]] = None,
    layout_type: str = "horizontal",
    shape_type: str = "hex_interlock",
    seed: int = 42,
    include_background: bool = True,
) -> str:
    """Procedurally synthesizes a complete, standalone SVG logo.
    
    Args:
        brand_name: Name of the brand (e.g. 'Apex', 'Verdant')
        tagline: Optional subtitle / industry tag (e.g. 'Wealth Management')
        palette: Hex color mapping {'primary', 'secondary', 'accent', 'background', 'text'}
        typography: Font specifications {'primary_font', 'secondary_font', 'weight', 'letter_spacing'}
        layout_type: 'horizontal' | 'stacked' | 'badge'
        shape_type: 'hex_interlock' | 'lettermark_geometric' | 'dynamic_arcs' | 'shield_minimal' | 'nodes_network' | 'circular_orbit' | 'botanical_spiral'
        seed: Random seed for procedural variations
        include_background: If True, renders solid background rect; if False, transparent
        
    Returns:
        Complete valid XML SVG document as a string.
    """
    # 1. Fallback defaults if not provided
    palette = palette or {
        "primary": "#0F172A",
        "secondary": "#0284C7",
        "accent": "#06B6D4",
        "background": "#FFFFFF",
        "text": "#0F172A",
    }

    typography = typography or {
        "primary_font": "Space Grotesk",
        "secondary_font": "Inter",
        "font_category": "geometric-sans",
        "letter_spacing": "0.05em",
        "weight": 700,
    }

    primary_font = typography.get("primary_font", "Space Grotesk")
    secondary_font = typography.get("secondary_font", "Inter")

    # 2. Gradient IDs unique per render
    grad_ids = {
        "primary_secondary": f"grad-ps-{seed}",
        "primary_accent": f"grad-pa-{seed}",
        "accent_radial": f"grad-ar-{seed}",
    }

    # 3. Google Fonts stylesheet import
    font_url = get_google_font_url(primary_font, secondary_font)

    # 4. Dispatch to Layout Engine
    layout_fn = LAYOUT_DISPATCHER.get(layout_type.lower().strip(), render_horizontal_layout)
    layout_content, width, height = layout_fn(
        brand_name=brand_name,
        tagline=tagline,
        shape_type=shape_type,
        palette=palette,
        typography=typography,
        grad_ids=grad_ids,
        seed=seed,
    )

    # 5. Background Rect
    bg_svg = ""
    if include_background and palette.get("background"):
        bg_svg = f'<rect width="{width}" height="{height}" rx="16" fill="{palette["background"]}" />'

    # 6. Assemble complete SVG document
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <!-- Embedded Google Fonts for Cross-Platform Independence -->
    <style>
      @import url('{font_url}');
      text {{
        font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        text-rendering: geometricPrecision;
      }}
    </style>

    <!-- Dynamic Aesthetic Gradients -->
    <linearGradient id="{grad_ids['primary_secondary']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{palette['primary']}" />
      <stop offset="100%" stop-color="{palette['secondary']}" />
    </linearGradient>

    <linearGradient id="{grad_ids['primary_accent']}" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{palette['secondary']}" />
      <stop offset="100%" stop-color="{palette['accent']}" />
    </linearGradient>

    <!-- Subtle Drop Shadow Filter -->
    <filter id="shadow-subtle" x="-10%" y="-10%" width="125%" height="125%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.10" />
    </filter>
  </defs>

  {bg_svg}
  {layout_content}
</svg>"""

    return svg
