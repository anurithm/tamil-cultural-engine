from typing import Dict, Any, Tuple

class UrgencyCalculationService:
    DISCLAIMER = "Prototype heuristic only. This is not a scientifically validated cultural-risk metric."

    @staticmethod
    def calculate_urgency(
        total_sources: int,
        present_sources: int,
        is_missing_step: bool,
        oldest_year_str: str = "1950",
        source_types: list = None
    ) -> Tuple[int, str, Dict[str, Any]]:
        """
        Calculate transparent 0-100 risk score and factor breakdown.
        Level: LOW (0-39), MEDIUM (40-64), HIGH (65-84), CRITICAL (85-100)
        """
        # Factor 1: Source Scarcity (0-100)
        # If total sources <= 2, scarcity is very high
        if total_sources <= 1:
            source_scarcity = 90
        elif total_sources == 2:
            source_scarcity = 75
        elif total_sources == 3:
            source_scarcity = 60
        else:
            source_scarcity = max(20, 100 - (total_sources * 15))

        # Factor 2: Documentation Gap Scarcity (0-100)
        # Proportion of sources missing this knowledge
        if total_sources > 0:
            missing_ratio = (total_sources - present_sources) / total_sources
            documentation_scarcity = int(missing_ratio * 100)
        else:
            documentation_scarcity = 50

        # Factor 3: Age of Evidence (0-100)
        # Older historical records with no modern corroboration carry higher vanishing risk
        try:
            # Extract 4-digit year
            import re
            m = re.search(r'\b(1[789]\d\d|20[0-2]\d)\b', str(oldest_year_str))
            if m:
                year_val = int(m.group(1))
                if year_val < 1920:
                    age_score = 85
                elif year_val < 1970:
                    age_score = 70
                elif year_val < 2000:
                    age_score = 55
                else:
                    age_score = 35
            else:
                age_score = 65
        except Exception:
            age_score = 60

        # Factor 4: Knowledge-Holder Scarcity (0-100)
        # If oral interview or community documentation is absent, practitioner risk is heightened
        has_community_record = any(
            t in ["Oral Interview Transcript", "Community Documentation"]
            for t in (source_types or [])
        )
        if has_community_record:
            holder_scarcity = 50
        else:
            holder_scarcity = 80

        # Factor 5: Procedural Step Vulnerability
        step_boost = 15 if is_missing_step else 0

        # Weighted heuristic combination
        # weights: 0.25 * source_scarcity + 0.30 * doc_scarcity + 0.20 * age + 0.25 * holder_scarcity
        raw_score = (
            0.25 * source_scarcity +
            0.30 * documentation_scarcity +
            0.20 * age_score +
            0.25 * holder_scarcity +
            step_boost
        )

        final_score = int(min(100, max(10, round(raw_score))))

        # Determine level
        if final_score >= 85:
            level = "CRITICAL"
        elif final_score >= 65:
            level = "HIGH"
        elif final_score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        factors = {
            "source_scarcity": source_scarcity,
            "documentation_scarcity": documentation_scarcity,
            "age_of_evidence": age_score,
            "holder_scarcity": holder_scarcity,
            "independent_source_count": total_sources,
            "present_source_count": present_sources,
            "is_missing_step": is_missing_step,
            "disclaimer": UrgencyCalculationService.DISCLAIMER
        }

        return final_score, level, factors
