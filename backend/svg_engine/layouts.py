"""Layout coordinate and typography placement engines for procedural logos."""

from __future__ import annotations
from typing import Dict, Any, Tuple
from .primitives import render_primitive


def render_horizontal_layout(
    brand_name: str,
    tagline: str,
    shape_type: str,
    palette: Dict[str, str],
    typography: Dict[str, Any],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> Tuple[str, int, int]:
    """Horizontal Layout: Icon on the left (200x200), Brand Name + Tagline on the right."""
    width = 800
    height = 320
    icon_cx = 160.0
    icon_cy = 160.0
    icon_size = 180.0

    # Render geometric icon primitive
    initial = brand_name[:1] if brand_name else "A"
    icon_svg = render_primitive(
        shape_type=shape_type,
        cx=icon_cx,
        cy=icon_cy,
        size=icon_size,
        palette=palette,
        grad_ids=grad_ids,
        brand_initial=initial,
        seed=seed,
    )

    # Calculate typography sizes
    text_x = 300.0
    name_y = 155.0 if tagline else 175.0
    tagline_y = 205.0

    primary_font = typography.get("primary_font", "Space Grotesk")
    secondary_font = typography.get("secondary_font", "Inter")
    weight = typography.get("weight", 700)
    letter_spacing = typography.get("letter_spacing", "0.04em")

    # Dynamic font sizing based on length of brand name
    brand_len = len(brand_name)
    font_size = 52.0 if brand_len <= 8 else max(34.0, 52.0 - (brand_len - 8) * 2.2)

    typography_svg = f"""
    <g class="typography-group">
      <!-- Brand Name -->
      <text x="{text_x}" y="{name_y}" 
            font-family="'{primary_font}', sans-serif" 
            font-size="{font_size}px" 
            font-weight="{weight}" 
            letter-spacing="{letter_spacing}" 
            fill="{palette['text']}" 
            dominant-baseline="middle">{brand_name}</text>
      
      <!-- Tagline / Descriptor (if present) -->
      {f'''
      <text x="{text_x + 2}" y="{tagline_y}" 
            font-family="'{secondary_font}', sans-serif" 
            font-size="16px" 
            font-weight="500" 
            letter-spacing="0.22em" 
            fill="{palette['secondary']}" 
            dominant-baseline="middle">{tagline.upper()}</text>
      ''' if tagline else ''}
    </g>
    """

    content_svg = f"""
    <g class="layout-horizontal">
      {icon_svg}
      {typography_svg}
    </g>
    """
    return content_svg, width, height


def render_stacked_layout(
    brand_name: str,
    tagline: str,
    shape_type: str,
    palette: Dict[str, str],
    typography: Dict[str, Any],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> Tuple[str, int, int]:
    """Stacked Layout: Icon centered at top, Brand Name and Subtext centered below."""
    width = 600
    height = 600
    icon_cx = 300.0
    icon_cy = 220.0
    icon_size = 230.0

    initial = brand_name[:1] if brand_name else "A"
    icon_svg = render_primitive(
        shape_type=shape_type,
        cx=icon_cx,
        cy=icon_cy,
        size=icon_size,
        palette=palette,
        grad_ids=grad_ids,
        brand_initial=initial,
        seed=seed,
    )

    name_y = 415.0 if tagline else 440.0
    tagline_y = 475.0

    primary_font = typography.get("primary_font", "Space Grotesk")
    secondary_font = typography.get("secondary_font", "Inter")
    weight = typography.get("weight", 700)
    letter_spacing = typography.get("letter_spacing", "0.06em")

    brand_len = len(brand_name)
    font_size = 46.0 if brand_len <= 8 else max(32.0, 46.0 - (brand_len - 8) * 1.8)

    typography_svg = f"""
    <g class="typography-group">
      <!-- Brand Name -->
      <text x="300" y="{name_y}" 
            font-family="'{primary_font}', sans-serif" 
            font-size="{font_size}px" 
            font-weight="{weight}" 
            letter-spacing="{letter_spacing}" 
            fill="{palette['text']}" 
            text-anchor="middle" 
            dominant-baseline="middle">{brand_name}</text>
      
      <!-- Accent Line Divider -->
      <line x1="220" y1="{name_y + font_size * 0.55}" x2="380" y2="{name_y + font_size * 0.55}" 
            stroke="{palette['accent']}" stroke-width="2.5" opacity="0.65" stroke-linecap="round" />

      <!-- Tagline -->
      {f'''
      <text x="300" y="{tagline_y}" 
            font-family="'{secondary_font}', sans-serif" 
            font-size="15px" 
            font-weight="500" 
            letter-spacing="0.25em" 
            fill="{palette['secondary']}" 
            text-anchor="middle" 
            dominant-baseline="middle">{tagline.upper()}</text>
      ''' if tagline else ''}
    </g>
    """

    content_svg = f"""
    <g class="layout-stacked">
      {icon_svg}
      {typography_svg}
    </g>
    """
    return content_svg, width, height


def render_badge_layout(
    brand_name: str,
    tagline: str,
    shape_type: str,
    palette: Dict[str, str],
    typography: Dict[str, Any],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> Tuple[str, int, int]:
    """Badge / Emblem Layout: Framed outer container enclosing icon and framed typography banner."""
    width = 600
    height = 600
    icon_cx = 300.0
    icon_cy = 230.0
    icon_size = 190.0

    initial = brand_name[:1] if brand_name else "A"
    icon_svg = render_primitive(
        shape_type=shape_type,
        cx=icon_cx,
        cy=icon_cy,
        size=icon_size,
        palette=palette,
        grad_ids=grad_ids,
        brand_initial=initial,
        seed=seed,
    )

    primary_font = typography.get("primary_font", "Cinzel")
    secondary_font = typography.get("secondary_font", "Inter")
    weight = typography.get("weight", 700)

    brand_len = len(brand_name)
    font_size = 40.0 if brand_len <= 8 else max(28.0, 40.0 - (brand_len - 8) * 1.5)

    badge_frame = f"""
    <!-- Outer Shield / Emblem Geometry Container -->
    <rect x="70" y="70" width="460" height="460" rx="36" ry="36" 
          fill="none" stroke="{palette['primary']}" stroke-width="4" opacity="0.4" />
    <rect x="85" y="85" width="430" height="430" rx="28" ry="28" 
          fill="none" stroke="{palette['accent']}" stroke-width="1.5" opacity="0.6" />
    <!-- Decorative Corner Dots -->
    <circle cx="95" cy="95" r="4" fill="{palette['accent']}" />
    <circle cx="505" cy="95" r="4" fill="{palette['accent']}" />
    <circle cx="95" cy="505" r="4" fill="{palette['accent']}" />
    <circle cx="505" cy="505" r="4" fill="{palette['accent']}" />
    """

    typography_svg = f"""
    <g class="typography-group">
      <!-- Name Ribbon Background -->
      <rect x="120" y="380" width="360" height="60" rx="12" ry="12" 
            fill="{palette['primary']}" opacity="0.95" />
      <!-- Brand Name -->
      <text x="300" y="415" 
            font-family="'{primary_font}', sans-serif" 
            font-size="{font_size}px" 
            font-weight="{weight}" 
            letter-spacing="0.10em" 
            fill="#FFFFFF" 
            text-anchor="middle" 
            dominant-baseline="middle">{brand_name}</text>
      
      <!-- Tagline -->
      {f'''
      <text x="300" y="475" 
            font-family="'{secondary_font}', sans-serif" 
            font-size="14px" 
            font-weight="600" 
            letter-spacing="0.25em" 
            fill="{palette['secondary']}" 
            text-anchor="middle" 
            dominant-baseline="middle">{tagline.upper()}</text>
      ''' if tagline else ''}
    </g>
    """

    content_svg = f"""
    <g class="layout-badge">
      {badge_frame}
      {icon_svg}
      {typography_svg}
    </g>
    """
    return content_svg, width, height


LAYOUT_DISPATCHER = {
    "horizontal": render_horizontal_layout,
    "stacked": render_stacked_layout,
    "badge": render_badge_layout,
}
