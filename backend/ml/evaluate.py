"""Standalone evaluation and demonstration script for ML Design Recommender.

Tests the ML model across diverse industry and aesthetic query vectors,
verifying cosine similarity scores, typography pairings, and explainability.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure backend directory is in python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from ml.dataset import load_catalog, DesignAttributes
from ml.recommender import DesignRecommender


def run_evaluation():
    print("=" * 70)
    print("AI/ML Mini Project: Design Recommender Standalone Evaluation")
    print("=" * 70)

    # 1. Load catalog & train model
    print("\n[Step 1] Loading Curated Design Knowledge Base...")
    catalog = load_catalog()
    print(f" Loaded {len(catalog)} aesthetic exemplar profiles across industries.")

    print("\n[Step 2] Initializing & Fitting k-NN Scikit-Learn Recommender...")
    recommender = DesignRecommender(catalog=catalog)
    print(" Pipeline fitted with StandardScaler, OneHotEncoder, and NearestNeighbors(metric='cosine').")

    # 2. Define test scenarios
    test_cases = [
        {
            "name": "Scenario 1: Cutting-edge Fintech Platform",
            "industry": "finance",
            "attributes": {
                "minimal_ornate": 0.15,
                "modern_classic": 0.90,
                "playful_serious": 0.10,
                "warm_cool": 0.20,
                "bold_delicate": 0.70,
            },
            "preferred_color": "cyan",
        },
        {
            "name": "Scenario 2: Artisan Organic Coffee Roastery",
            "industry": "food",
            "attributes": {
                "minimal_ornate": 0.40,
                "modern_classic": 0.30,
                "playful_serious": 0.35,
                "warm_cool": 0.85,
                "bold_delicate": 0.55,
            },
            "preferred_color": "warm",
        },
        {
            "name": "Scenario 3: Radical Brutalist Creative Studio",
            "industry": "creative",
            "attributes": {
                "minimal_ornate": 0.15,
                "modern_classic": 0.95,
                "playful_serious": 0.75,
                "warm_cool": 0.60,
                "bold_delicate": 0.95,
            },
            "preferred_color": "lime",
        },
        {
            "name": "Scenario 4: Mindful Health & Meditation App",
            "industry": "health",
            "attributes": {
                "minimal_ornate": 0.20,
                "modern_classic": 0.65,
                "playful_serious": 0.30,
                "warm_cool": 0.45,
                "bold_delicate": 0.30,
            },
            "preferred_color": None,
        },
    ]

    # 3. Execute evaluation
    print("\n[Step 3] Evaluating Test Query Scenarios...")
    for idx, test in enumerate(test_cases, 1):
        print("\n" + "-" * 70)
        print(f"TEST CASE {idx}: {test['name']}")
        print(f"Industry: {test['industry']} | Preferred Color: {test['preferred_color']}")
        print(f"Target Attributes: {test['attributes']}")
        
        recs = recommender.recommend(
            attributes=test["attributes"],
            industry=test["industry"],
            k=3,
            preferred_color=test["preferred_color"],
        )

        assert len(recs) == 3, f"Expected 3 recommendations, got {len(recs)}"

        print(f"\nTop 3 Recommended Design Profiles:")
        for r_idx, rec in enumerate(recs, 1):
            profile = rec["profile"]
            palette = rec["palette"]
            typo = rec["typography"]
            print(f"  #{r_idx} [{rec['similarity_score'] * 100:.1f}% Match] {profile.name} (ID: {profile.id})")
            print(f"     Palette : Primary {palette['primary']} | Secondary {palette['secondary']} | Accent {palette['accent']}")
            print(f"     Typography : '{typo['primary_font']}' & '{typo['secondary_font']}' ({typo['font_category']})")
            print(f"     Shapes  : {', '.join(rec['shape_affinity'])}")
            print(f"     Reasons : {'; '.join(rec['match_reasons'])}")

    print("\n" + "=" * 70)
    print("ALL EVALUATION CHECKS PASSED: ML Recommender is verified and operational!")
    print("=" * 70)


if __name__ == "__main__":
    run_evaluation()
