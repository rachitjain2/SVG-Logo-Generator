"""End-to-end integration test verifying the full stack through the Vite frontend proxy."""

from __future__ import annotations
import json
import urllib.request


def test_e2e():
    print("=" * 65)
    print("E2E Integration Verification: Frontend Proxy -> Backend API")
    print("=" * 65)

    # 1. Test Proxy Health
    url_health = "http://localhost:5173/api/health"
    with urllib.request.urlopen(url_health) as res:
        assert res.status == 200
        health = json.loads(res.read().decode())
        print(f"[OK] Health check passed via Vite Proxy: {health}")

    # 2. Test Proxy Full Generation
    url_generate = "http://localhost:5173/api/generate"
    payload = {
        "brand_name": "Verdant",
        "industry": "Eco",
        "style_description": "organic botanical sustainable clean and modern",
    }
    req = urllib.request.Request(
        url_generate,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as res:
        assert res.status == 200
        data = json.loads(res.read().decode())
        assert "<svg" in data["svg"]
        assert "Verdant" in data["svg"]
        print(f"[OK] Full Logo Generation Succeeded!")
        print(f"     Brand Name: {data['brand_name']}")
        print(f"     Tagline: {data['tagline']}")
        print(f"     Shape Archetype: {data['shape']}")
        print(f"     Layout: {data['layout']}")
        print(f"     Similarity Match: {data['similarity_score'] * 100:.1f}%")
        print(f"     SVG Vector Size: {len(data['svg'])} bytes")

    # 3. Test Proxy Manual Re-Render Override
    url_rerender = "http://localhost:5173/api/re-render"
    override_payload = {
        "brand_name": "Verdant",
        "tagline": "Botanical Research Labs",
        "palette": {
            "primary": "#14532D",
            "secondary": "#B45309",
            "accent": "#FDE047",
            "background": "#F0FDF4",
            "text": "#14532D",
        },
        "typography": {
            "primary_font": "Fraunces",
            "secondary_font": "Inter",
            "weight": 700,
            "letter_spacing": "0.04em",
        },
        "layout_type": "stacked",
        "shape_type": "botanical_spiral",
        "seed": 777,
    }
    req2 = urllib.request.Request(
        url_rerender,
        data=json.dumps(override_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req2) as res:
        assert res.status == 200
        rerender_data = json.loads(res.read().decode())
        assert "<svg" in rerender_data["svg"]
        assert "#FDE047" in rerender_data["svg"]
        print(f"[OK] Instant Re-render with Custom Overrides Succeeded! ({len(rerender_data['svg'])} bytes)")

    print("\n" + "=" * 65)
    print("ALL END-TO-END INTEGRATION TESTS PASSED PERFECTLY!")
    print("=" * 65)


if __name__ == "__main__":
    test_e2e()
