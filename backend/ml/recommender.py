"""Machine Learning Recommender Engine for Design Aesthetics.

Uses Content-Based Metric Retrieval with k-Nearest Neighbors (k-NN) and Cosine Similarity
over a multi-dimensional normalized design attribute space and categorical industry encodings.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import NearestNeighbors

from .dataset import DesignProfile, load_catalog, DesignAttributes


class DesignRecommender:
    """k-NN Recommender for brand color palettes and typography pairings.
    
    Attributes Space:
    - Continuous (5D): [minimal_ornate, modern_classic, playful_serious, warm_cool, bold_delicate]
    - Categorical (1D): [industry]
    """

    FEATURE_COLS = [
        "minimal_ornate",
        "modern_classic",
        "playful_serious",
        "warm_cool",
        "bold_delicate",
    ]

    def __init__(self, catalog: Optional[List[DesignProfile]] = None):
        self.catalog = catalog or load_catalog()
        self._build_dataframe()
        self._fit_pipeline()

    def _build_dataframe(self) -> None:
        """Flattens the catalog into a Pandas DataFrame for scikit-learn processing."""
        records = []
        for p in self.catalog:
            rec = {
                "id": p.id,
                "name": p.name,
                "industry": p.industry.lower().strip(),
                "minimal_ornate": p.attributes.minimal_ornate,
                "modern_classic": p.attributes.modern_classic,
                "playful_serious": p.attributes.playful_serious,
                "warm_cool": p.attributes.warm_cool,
                "bold_delicate": p.attributes.bold_delicate,
            }
            records.append(rec)
        self.df = pd.DataFrame(records)

    def _fit_pipeline(self) -> None:
        """Configures and trains the scikit-learn preprocessing and k-NN index."""
        # Preprocessing: standard scaling for continuous dimensions, One-Hot for industry
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.FEATURE_COLS),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["industry"]),
            ],
            remainder="drop",
        )

        # Transform catalog features into feature vectors
        X = self.preprocessor.fit_transform(self.df[self.FEATURE_COLS + ["industry"]])
        self.feature_matrix = X

        # Fit Nearest Neighbors model using Cosine distance
        # Cosine distance measures angular orientation in aesthetic space regardless of magnitude
        self.model = NearestNeighbors(
            n_neighbors=min(len(self.catalog), 5),
            metric="cosine",
            algorithm="brute",  # Optimal for small to medium catalog vectors
        )
        self.model.fit(X)

    def _build_query_dataframe(self, attributes: Dict[str, float] | DesignAttributes, industry: str) -> pd.DataFrame:
        """Converts user query inputs into standard DataFrame row for pipeline transformation."""
        if isinstance(attributes, DesignAttributes):
            attr_dict = attributes.model_dump()
        else:
            attr_dict = attributes

        query_row = {
            "minimal_ornate": float(attr_dict.get("minimal_ornate", 0.5)),
            "modern_classic": float(attr_dict.get("modern_classic", 0.5)),
            "playful_serious": float(attr_dict.get("playful_serious", 0.5)),
            "warm_cool": float(attr_dict.get("warm_cool", 0.5)),
            "bold_delicate": float(attr_dict.get("bold_delicate", 0.5)),
            "industry": str(industry).lower().strip(),
        }
        return pd.DataFrame([query_row])

    def recommend(
        self,
        attributes: Dict[str, float] | DesignAttributes,
        industry: str,
        k: int = 3,
        preferred_color: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves top-k recommended design profiles matching query attributes.
        
        Args:
            attributes: 5-axis continuous aesthetic ratings (0.0 to 1.0)
            industry: Industry domain tag (e.g. 'tech', 'finance', 'food')
            k: Number of candidate recommendations to retrieve
            preferred_color: Optional color keyword / hex to boost matching palettes
            
        Returns:
            List of recommendation dicts containing profile, similarity score, and match explanations.
        """
        k = min(max(1, k), len(self.catalog))
        query_df = self._build_query_dataframe(attributes, industry)
        query_vec = self.preprocessor.transform(query_df[self.FEATURE_COLS + ["industry"]])

        distances, indices = self.model.kneighbors(query_vec, n_neighbors=k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            profile = self.catalog[idx]
            # Cosine similarity in [0, 1] range: 1 - cosine_distance
            # In scikit-learn, cosine distance can be in [0, 2], so clamp to [0, 1]
            similarity = max(0.0, min(1.0, 1.0 - float(dist)))

            # If user has a preferred color, compute optional affinity boost
            boost = 0.0
            if preferred_color:
                boost = self._compute_color_affinity(preferred_color, profile)
                similarity = min(1.0, similarity * 0.85 + boost * 0.15)

            # Generate explainable match justifications for viva defense
            explanations = self._generate_match_reasons(
                query_attributes=query_df.iloc[0].to_dict(),
                profile=profile,
            )

            results.append({
                "profile": profile,
                "palette": profile.palette.model_dump(),
                "typography": profile.typography.model_dump(),
                "shape_affinity": profile.shape_affinity,
                "similarity_score": round(similarity, 4),
                "cosine_distance": round(float(dist), 4),
                "match_reasons": explanations,
            })

        # Re-sort results by adjusted similarity score descending
        results.sort(key=lambda r: r["similarity_score"], reverse=True)
        return results

    def _compute_color_affinity(self, preferred_color: str, profile: DesignProfile) -> float:
        """Heuristic affinity match between user preferred color and catalog palette."""
        pref = preferred_color.lower().strip()
        palette_hexes = [
            profile.palette.primary.lower(),
            profile.palette.secondary.lower(),
            profile.palette.accent.lower(),
        ]
        # Direct hex match
        if pref in palette_hexes:
            return 1.0

        # Color name keyword mappings
        color_family_keywords = {
            "blue": ["#0284c7", "#38bdf8", "#2563eb", "#0369a1", "#3b82f6", "#0f172a", "#0a192f"],
            "cyan": ["#06b6d4", "#2dd4bf", "#99f6e4", "#0284c7"],
            "teal": ["#134e4a", "#0f766e", "#2dd4bf", "#10b981"],
            "green": ["#14532d", "#10b981", "#84cc16", "#a3e635", "#86efac", "#1c3829"],
            "gold": ["#d4af37", "#ca8a04", "#eab308", "#f3e5ab"],
            "purple": ["#8b5cf6", "#7c3aed", "#581c87", "#2e1065", "#c084fc", "#701a75"],
            "orange": ["#f97316", "#d97706", "#f59e0b", "#e07a5f"],
            "red": ["#dc2626", "#e11d48", "#fb7185", "#4c0519", "#881337"],
            "dark": ["#0f172a", "#030712", "#18181b", "#000000", "#121212", "#171717"],
            "white": ["#ffffff", "#fafafa", "#f8fafc", "#f0fdfa", "#f0fdf4"],
        }

        for family, hex_list in color_family_keywords.items():
            if family in pref:
                if any(any(h in ph for h in hex_list) for ph in palette_hexes):
                    return 0.95

        return 0.5

    def _generate_match_reasons(self, query_attributes: Dict[str, Any], profile: DesignProfile) -> List[str]:
        """Generates human-readable explanations of why this profile was recommended."""
        reasons = []
        if query_attributes.get("industry") == profile.industry:
            reasons.append(f"Direct industry domain match for '{profile.industry}'")

        # Check key continuous attribute alignments (difference < 0.2)
        diffs = {
            "modernity": abs(query_attributes.get("modern_classic", 0.5) - profile.attributes.modern_classic),
            "minimalism": abs(query_attributes.get("minimal_ornate", 0.5) - profile.attributes.minimal_ornate),
            "tone": abs(query_attributes.get("playful_serious", 0.5) - profile.attributes.playful_serious),
            "color temperature": abs(query_attributes.get("warm_cool", 0.5) - profile.attributes.warm_cool),
            "visual weight": abs(query_attributes.get("bold_delicate", 0.5) - profile.attributes.bold_delicate),
        }

        # Select top 2 closest dimensions
        sorted_diffs = sorted(diffs.items(), key=lambda x: x[1])
        for dim, diff in sorted_diffs[:2]:
            if diff <= 0.25:
                reasons.append(f"High aesthetic concordance on {dim} (diff={diff:.2f})")

        return reasons
