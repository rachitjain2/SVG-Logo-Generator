"""In-memory API endpoint verification using FastAPI TestClient."""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app import app, startup_event


def run_api_tests():
    print("=" * 65)
    print("Testing FastAPI Backend Endpoints")
    print("=" * 65)

    # Trigger startup event
    startup_event()
    client = TestClient(app)

    # 1. Health check
    print("\n[Test 1] GET /api/health...")
    resp = client.get("/api/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    health_data = resp.json()
    print(f" Health status: {health_data['status']} | LLM: {health_data['llm_model']}")

    # 2. Options list
    print("\n[Test 2] GET /api/options...")
    resp = client.get("/api/options")
    assert resp.status_code == 200
    options = resp.json()
    print(f" Loaded {len(options['shapes'])} shapes, {len(options['layouts'])} layouts, {len(options['fonts'])} fonts.")

    # 3. Full /api/generate pipeline
    print("\n[Test 3] POST /api/generate (Fintech prompt)...")
    payload = {
        "brand_name": "NovaPay",
        "industry": "finance",
        "style_description": "modern, trustworthy, clean, minimal, electric cyan",
        "preferred_color": "cyan",
    }
    resp = client.post("/api/generate", json=payload)
    assert resp.status_code == 200, f"Generate failed: {resp.text}"
    gen_data = resp.json()
    assert "<svg" in gen_data["svg"]
    assert "NovaPay" in gen_data["svg"]
    print(f" Generated SVG: {len(gen_data['svg'])} bytes")
    print(f" Matched Palette: {gen_data['selected_palette']['primary']} / {gen_data['selected_palette']['accent']}")
    print(f" Selected Fonts: {gen_data['selected_typography']['primary_font']} + {gen_data['selected_typography']['secondary_font']}")
    print(f" Similarity Score: {gen_data['similarity_score'] * 100:.1f}%")
    print(f" Alternatives returned: {len(gen_data['alternatives'])}")

    # 4. Instant /api/re-render pipeline
    print("\n[Test 4] POST /api/re-render (manual override)...")
    rerender_payload = {
        "brand_name": "NovaPay",
        "tagline": "Custom Overridden Tagline",
        "palette": {
            "primary": "#FF0055",
            "secondary": "#00FFCC",
            "accent": "#FFFF00",
            "background": "#111111",
            "text": "#FFFFFF",
        },
        "typography": {
            "primary_font": "Outfit",
            "secondary_font": "Inter",
            "weight": 700,
            "letter_spacing": "0.08em",
        },
        "layout_type": "stacked",
        "shape_type": "dynamic_arcs",
        "seed": 999,
    }
    resp = client.post("/api/re-render", json=rerender_payload)
    assert resp.status_code == 200
    rerender_data = resp.json()
    assert "<svg" in rerender_data["svg"]
    assert "#FF0055" in rerender_data["svg"]
    print(f" Re-rendered SVG with custom overrides: {len(rerender_data['svg'])} bytes")

    print("\n" + "=" * 65)
    print("ALL API ENDPOINT TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_api_tests()
