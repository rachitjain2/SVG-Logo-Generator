"""Standalone verification script for procedural SVG generation engine.

Renders sample SVG logos from hardcoded style vectors, palettes, and layouts
directly to `backend/output/` for quick visual inspection.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from svg_engine.generator import generate_logo


def run_tests():
    output_dir = backend_dir / "output"
    output_dir.mkdir(exist_ok=True)

    print("=" * 65)
    print("Testing Procedural SVG Generation Engine")
    print("=" * 65)

    test_cases = [
        {
            "filename": "logo_1_fintech_horizontal.svg",
            "brand_name": "Apex",
            "tagline": "Next-Gen Fintech",
            "layout_type": "horizontal",
            "shape_type": "hex_interlock",
            "palette": {
                "primary": "#0F172A",
                "secondary": "#0284C7",
                "accent": "#06B6D4",
                "background": "#FFFFFF",
                "text": "#0F172A",
            },
            "typography": {
                "primary_font": "Space Grotesk",
                "secondary_font": "Inter",
                "weight": 700,
                "letter_spacing": "0.06em",
            },
        },
        {
            "filename": "logo_2_eco_stacked.svg",
            "brand_name": "Verdant",
            "tagline": "Organic Botanical Labs",
            "layout_type": "stacked",
            "shape_type": "botanical_spiral",
            "palette": {
                "primary": "#14532D",
                "secondary": "#B45309",
                "accent": "#86EFAC",
                "background": "#F0FDF4",
                "text": "#14532D",
            },
            "typography": {
                "primary_font": "Fraunces",
                "secondary_font": "Lato",
                "weight": 600,
                "letter_spacing": "0.04em",
            },
        },
        {
            "filename": "logo_3_creative_lettermark.svg",
            "brand_name": "Kroma",
            "tagline": "Design Agency",
            "layout_type": "horizontal",
            "shape_type": "lettermark_geometric",
            "palette": {
                "primary": "#171717",
                "secondary": "#EC4899",
                "accent": "#06B6D4",
                "background": "#FAFAFA",
                "text": "#171717",
            },
            "typography": {
                "primary_font": "Syne",
                "secondary_font": "Space Grotesk",
                "weight": 800,
                "letter_spacing": "0.05em",
            },
        },
        {
            "filename": "logo_4_security_badge.svg",
            "brand_name": "Aegis",
            "tagline": "Cloud Security Protocol",
            "layout_type": "badge",
            "shape_type": "shield_minimal",
            "palette": {
                "primary": "#030712",
                "secondary": "#10B981",
                "accent": "#34D399",
                "background": "#030712",
                "text": "#F9FAFB",
            },
            "typography": {
                "primary_font": "Cinzel",
                "secondary_font": "Inter",
                "weight": 700,
                "letter_spacing": "0.10em",
            },
        },
    ]

    for idx, tc in enumerate(test_cases, 1):
        svg_content = generate_logo(
            brand_name=tc["brand_name"],
            tagline=tc["tagline"],
            palette=tc["palette"],
            typography=tc["typography"],
            layout_type=tc["layout_type"],
            shape_type=tc["shape_type"],
            seed=100 * idx,
        )

        # Basic integrity assertion
        assert "<svg" in svg_content and "</svg>" in svg_content
        assert tc["brand_name"] in svg_content

        target_file = output_dir / tc["filename"]
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(svg_content)

        print(f"[{idx}/4] Rendered '{tc['brand_name']}' -> {target_file.name} ({len(svg_content)} bytes)")

    print("=" * 65)
    print("ALL SVG LOGO RENDERS SUCCEEDED! Files written to backend/output/")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
