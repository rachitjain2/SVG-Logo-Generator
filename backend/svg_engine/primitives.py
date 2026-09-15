"""Parametrized geometric primitive engines for procedural vector logo synthesis.

Generates scalable, mathematical SVG vector paths including isometric hexagons,
geometric lettermarks, dynamic curved arcs, minimalist shields, and node networks.
"""

from __future__ import annotations
import math
from typing import Dict, Any


def get_hex_points(cx: float, cy: float, radius: float, rotation: float = 0.0) -> list[tuple[float, float]]:
    """Calculates vertex coordinates for a regular hexagon."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i + rotation)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points


def generate_hex_interlock(
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders a 3D isometric faceted cube / interlocking hexagon emblem."""
    r = size * 0.48
    # Vertices of outer hexagon rotated 30 degrees for flat-top/pointy-side
    pts = get_hex_points(cx, cy, r, rotation=30)
    
    # pts[0] is at 30 deg, pts[1] at 90 deg (bottom), pts[2] at 150 deg, pts[3] at 210 deg, pts[4] at 270 deg (top), pts[5] at 330 deg
    # Facet 1 (Top rhomb): (cx, cy), pts[4] (top), pts[5], pts[0]
    p_center = (cx, cy)
    p_top = (cx, cy - r)
    p_top_right = (cx + r * math.cos(math.radians(-30)), cy + r * math.sin(math.radians(-30)))
    p_bot_right = (cx + r * math.cos(math.radians(30)), cy + r * math.sin(math.radians(30)))
    p_bot = (cx, cy + r)
    p_bot_left = (cx + r * math.cos(math.radians(150)), cy + r * math.sin(math.radians(150)))
    p_top_left = (cx + r * math.cos(math.radians(210)), cy + r * math.sin(math.radians(210)))

    # 3 isometric facets
    d_top = f"M {p_center[0]} {p_center[1]} L {p_top_left[0]} {p_top_left[1]} L {p_top[0]} {p_top[1]} L {p_top_right[0]} {p_top_right[1]} Z"
    d_right = f"M {p_center[0]} {p_center[1]} L {p_top_right[0]} {p_top_right[1]} L {p_bot_right[0]} {p_bot_right[1]} L {p_bot[0]} {p_bot[1]} Z"
    d_left = f"M {p_center[0]} {p_center[1]} L {p_bot[0]} {p_bot[1]} L {p_bot_left[0]} {p_bot_left[1]} L {p_top_left[0]} {p_top_left[1]} Z"

    # Inner concentric floating diamond
    inner_r = r * 0.28
    d_inner = (
        f"M {cx} {cy - inner_r} "
        f"L {cx + inner_r * 0.866} {cy - inner_r * 0.5} "
        f"L {cx} {cy + inner_r} "
        f"L {cx - inner_r * 0.866} {cy - inner_r * 0.5} Z"
    )

    svg = f"""
    <g class="primitive-hex-interlock" filter="url(#shadow-subtle)">
      <!-- Isometric Facet Left -->
      <path d="{d_left}" fill="{palette['primary']}" opacity="0.95" />
      <!-- Isometric Facet Right -->
      <path d="{d_right}" fill="{palette['secondary']}" opacity="0.90" />
      <!-- Isometric Facet Top -->
      <path d="{d_top}" fill="url(#{grad_ids['primary_accent']})" opacity="0.98" />
      <!-- Inner Floating Accent Core -->
      <path d="{d_inner}" fill="{palette['accent']}" opacity="0.9" />
      <!-- Stylized Center Node -->
      <circle cx="{cx}" cy="{cy}" r="{size * 0.05}" fill="#FFFFFF" opacity="0.95" />
    </g>
    """
    return svg


def generate_lettermark_geometric(
    initial: str,
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders a modern geometric badge enclosing a monogram lettermark."""
    char = (initial[:1] if initial else "A").upper()
    r = size * 0.46
    
    # Outer frame: Squircle / rounded container with gradient stroke and subtle fill
    corner = r * 0.38
    svg = f"""
    <g class="primitive-lettermark" filter="url(#shadow-subtle)">
      <!-- Outer Framed Emblem -->
      <rect x="{cx - r}" y="{cy - r}" width="{r * 2}" height="{r * 2}" 
            rx="{corner}" ry="{corner}" 
            fill="url(#{grad_ids['primary_secondary']})" opacity="0.95" />
      <!-- Inner Inset Accent Frame -->
      <rect x="{cx - r * 0.86}" y="{cy - r * 0.86}" width="{r * 1.72}" height="{r * 1.72}" 
            rx="{corner * 0.75}" ry="{corner * 0.75}" 
            fill="none" stroke="{palette['accent']}" stroke-width="{size * 0.02}" opacity="0.5" />
      <!-- Monogram Character -->
      <text x="{cx}" y="{cy + r * 0.34}" 
            font-family="Space Grotesk, Montserrat, sans-serif" 
            font-size="{size * 0.54}" 
            font-weight="800" 
            fill="#FFFFFF" 
            text-anchor="middle">{char}</text>
      <!-- Accent Design Element (corner dot) -->
      <circle cx="{cx + r * 0.6}" cy="{cy - r * 0.6}" r="{size * 0.045}" fill="{palette['accent']}" />
    </g>
    """
    return svg


def generate_dynamic_arcs(
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders sleek overlapping dynamic arcs / kinetic vortex."""
    r = size * 0.44
    stroke_w = size * 0.075

    svg = f"""
    <g class="primitive-dynamic-arcs" filter="url(#shadow-subtle)">
      <!-- Outer Primary Arc -->
      <path d="M {cx - r * 0.85} {cy + r * 0.5} A {r} {r} 0 1 1 {cx + r} {cy}" 
            fill="none" stroke="url(#{grad_ids['primary_secondary']})" 
            stroke-width="{stroke_w}" stroke-linecap="round" />
      <!-- Secondary Inner Arc -->
      <path d="M {cx + r * 0.85} {cy - r * 0.5} A {r * 0.72} {r * 0.72} 0 1 1 {cx - r * 0.72} {cy}" 
            fill="none" stroke="{palette['accent']}" 
            stroke-width="{stroke_w * 0.85}" stroke-linecap="round" opacity="0.9" />
      <!-- Central Satellite Node -->
      <circle cx="{cx}" cy="{cy}" r="{size * 0.09}" fill="{palette['primary']}" />
      <circle cx="{cx}" cy="{cy}" r="{size * 0.04}" fill="#FFFFFF" />
      <!-- Orbital Satellite -->
      <circle cx="{cx + r * 0.7}" cy="{cy - r * 0.65}" r="{size * 0.045}" fill="{palette['secondary']}" />
    </g>
    """
    return svg


def generate_shield_minimal(
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders a sleek minimalist modern shield / crest."""
    w = size * 0.40
    h = size * 0.46

    # Shield path points
    p_top_mid = (cx, cy - h)
    p_top_right = (cx + w, cy - h * 0.7)
    p_mid_right = (cx + w, cy + h * 0.1)
    p_bottom = (cx, cy + h)
    p_mid_left = (cx - w, cy + h * 0.1)
    p_top_left = (cx - w, cy - h * 0.7)

    d_shield = (
        f"M {p_top_mid[0]} {p_top_mid[1]} "
        f"L {p_top_right[0]} {p_top_right[1]} "
        f"L {p_mid_right[0]} {p_mid_right[1]} "
        f"Q {p_mid_right[0]} {cy + h * 0.65} {p_bottom[0]} {p_bottom[1]} "
        f"Q {p_mid_left[0]} {cy + h * 0.65} {p_mid_left[0]} {p_mid_left[1]} "
        f"L {p_top_left[0]} {p_top_left[1]} Z"
    )

    # Inner faceted dividing line
    d_inner_left = (
        f"M {p_top_mid[0]} {p_top_mid[1]} "
        f"L {p_top_left[0]} {p_top_left[1]} "
        f"L {p_mid_left[0]} {p_mid_left[1]} "
        f"Q {p_mid_left[0]} {cy + h * 0.65} {p_bottom[0]} {p_bottom[1]} Z"
    )

    svg = f"""
    <g class="primitive-shield" filter="url(#shadow-subtle)">
      <!-- Main Shield Base -->
      <path d="{d_shield}" fill="url(#{grad_ids['primary_secondary']})" opacity="0.95" />
      <!-- Left Facet Shading for 3D depth -->
      <path d="{d_inner_left}" fill="#000000" opacity="0.18" />
      <!-- Inner Geometric Chevron Key -->
      <path d="M {cx} {cy - h * 0.4} L {cx + w * 0.45} {cy} L {cx} {cy + h * 0.4} L {cx - w * 0.45} {cy} Z" 
            fill="{palette['accent']}" opacity="0.95" />
      <circle cx="{cx}" cy="{cy}" r="{size * 0.05}" fill="#FFFFFF" />
    </g>
    """
    return svg


def generate_nodes_network(
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders a futuristic AI/Neural node network mesh."""
    r = size * 0.44
    angles = [0, 72, 144, 216, 288]
    node_pts = []
    for a in angles:
        rad = math.radians(a - 18)
        x = cx + r * math.cos(rad)
        y = cy + r * math.sin(rad)
        node_pts.append((x, y))

    # Connection lines between nodes
    lines_svg = []
    for i in range(len(node_pts)):
        p1 = node_pts[i]
        # Line to center
        lines_svg.append(f'<line x1="{cx}" y1="{cy}" x2="{p1[0]}" y2="{p1[1]}" stroke="{palette["secondary"]}" stroke-width="{size * 0.016}" opacity="0.5" />')
        # Line to next outer node
        p2 = node_pts[(i + 1) % len(node_pts)]
        lines_svg.append(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="url(#{grad_ids["primary_accent"]})" stroke-width="{size * 0.022}" opacity="0.75" />')
        # Line to skip-one node (star pattern)
        p3 = node_pts[(i + 2) % len(node_pts)]
        lines_svg.append(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p3[0]}" y2="{p3[1]}" stroke="{palette["primary"]}" stroke-width="{size * 0.014}" opacity="0.35" />')

    # Nodes (circles)
    circles_svg = []
    for idx, (x, y) in enumerate(node_pts):
        node_col = palette['accent'] if idx % 2 == 0 else palette['secondary']
        circles_svg.append(f'<circle cx="{x}" cy="{y}" r="{size * 0.045}" fill="{node_col}" />')
        circles_svg.append(f'<circle cx="{x}" cy="{y}" r="{size * 0.02}" fill="#FFFFFF" />')

    # Center pulse node
    center_svg = f"""
    <circle cx="{cx}" cy="{cy}" r="{size * 0.08}" fill="url(#{grad_ids['primary_accent']})" />
    <circle cx="{cx}" cy="{cy}" r="{size * 0.035}" fill="#FFFFFF" />
    """

    return f"""
    <g class="primitive-nodes-network" filter="url(#shadow-subtle)">
      {''.join(lines_svg)}
      {center_svg}
      {''.join(circles_svg)}
    </g>
    """


def generate_circular_orbit(
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders clean concentric circular orbits with modern planetary accents."""
    r = size * 0.44
    stroke_w = size * 0.035

    svg = f"""
    <g class="primitive-circular-orbit" filter="url(#shadow-subtle)">
      <!-- Outer Halo Orbit -->
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{palette['primary']}" 
              stroke-width="{stroke_w}" opacity="0.3" stroke-dasharray="{size * 0.04} {size * 0.02}" />
      <!-- Mid Accent Orbit -->
      <circle cx="{cx}" cy="{cy}" r="{r * 0.72}" fill="none" stroke="url(#{grad_ids['primary_accent']})" 
              stroke-width="{stroke_w * 1.5}" opacity="0.85" />
      <!-- Central Planet Core -->
      <circle cx="{cx}" cy="{cy}" r="{r * 0.40}" fill="url(#{grad_ids['primary_secondary']})" />
      <circle cx="{cx}" cy="{cy}" r="{r * 0.16}" fill="{palette['accent']}" />
      <!-- Orbital Satellites -->
      <circle cx="{cx + r}" cy="{cy}" r="{size * 0.045}" fill="{palette['accent']}" />
      <circle cx="{cx - r * 0.72}" cy="{cy}" r="{size * 0.035}" fill="{palette['secondary']}" />
    </g>
    """
    return svg


def generate_botanical_spiral(
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    seed: int = 42,
) -> str:
    """Renders a serene organic petal / botanical whorl."""
    r = size * 0.44
    num_petals = 4
    petals = []

    for i in range(num_petals):
        deg = i * (360 / num_petals) + 45
        petals.append(f"""
        <g transform="rotate({deg} {cx} {cy})">
          <path d="M {cx} {cy} Q {cx + r * 0.6} {cy - r * 0.7} {cx} {cy - r} Q {cx - r * 0.6} {cy - r * 0.7} {cx} {cy} Z" 
                fill="url(#{grad_ids['primary_secondary']})" opacity="0.8" />
        </g>
        """)

    svg = f"""
    <g class="primitive-botanical" filter="url(#shadow-subtle)">
      {''.join(petals)}
      <circle cx="{cx}" cy="{cy}" r="{size * 0.07}" fill="{palette['accent']}" />
      <circle cx="{cx}" cy="{cy}" r="{size * 0.03}" fill="#FFFFFF" />
    </g>
    """
    return svg


SHAPE_DISPATCHER = {
    "hex_interlock": generate_hex_interlock,
    "lettermark_geometric": generate_lettermark_geometric,
    "dynamic_arcs": generate_dynamic_arcs,
    "shield_minimal": generate_shield_minimal,
    "nodes_network": generate_nodes_network,
    "circular_orbit": generate_circular_orbit,
    "botanical_spiral": generate_botanical_spiral,
}


def render_primitive(
    shape_type: str,
    cx: float,
    cy: float,
    size: float,
    palette: Dict[str, str],
    grad_ids: Dict[str, str],
    brand_initial: str = "A",
    seed: int = 42,
) -> str:
    """Factory function dispatching to corresponding geometric shape primitive."""
    shape_key = shape_type.lower().strip() if shape_type else "hex_interlock"
    fn = SHAPE_DISPATCHER.get(shape_key, generate_hex_interlock)

    if fn == generate_lettermark_geometric:
        return fn(brand_initial, cx, cy, size, palette, grad_ids, seed)
    return fn(cx, cy, size, palette, grad_ids, seed)
