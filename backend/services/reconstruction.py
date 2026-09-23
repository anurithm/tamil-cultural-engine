from typing import List, Dict, Any, Tuple

class ReconstructionService:
    @staticmethod
    def generate_cautious_reconstruction(
        element_name: str,
        category: str,
        is_missing_step: bool,
        step_order: int,
        supporting_evidences: List[Dict[str, Any]],
        total_sources_count: int
    ) -> Tuple[str, str]:
        """
        Formulate a cautious evidence-based synthesis hypothesis.
        Confidence levels: STRONGLY_SUPPORTED, POSSIBLE, UNSUPPORTED, VERIFIED.
        Never presents reconstruction as historical fact.
        """
        supporting_count = len([e for e in supporting_evidences if e.get("presence_status") == "present"])

        # Determine confidence level
        if supporting_count >= 2:
            confidence = "STRONGLY_SUPPORTED"
            support_desc = f"corroborated by {supporting_count} independent sources"
        elif supporting_count == 1:
            confidence = "POSSIBLE"
            support_desc = "supported by limited textual evidence from a single source"
        else:
            confidence = "UNSUPPORTED"
            support_desc = "lacking sufficient direct textual support"

        source_citations = []
        for e in supporting_evidences:
            if e.get("presence_status") == "present":
                author_year = f"{e.get('author', 'Author')} ({e.get('year', 'n.d.')}, p. {e.get('page_number', 1)})"
                source_citations.append(author_year)

        citations_str = "; ".join(source_citations) if source_citations else "Unrecorded source"

        if is_missing_step:
            hypothesis = (
                f"Available sources suggest that the procedural step '{element_name}' "
                f"(identified as Step {step_order or 'N'}) may have traditionally formed part of the sequential workflow, "
                f"as documented in: {citations_str}. "
                f"While unmentioned in contemporary or comparative records, textual evidence ({support_desc}) "
                f"indicates its role as an intermediate stage. This cautious reconstruction warrants field verification with hereditary practitioners."
            )
        else:
            hypothesis = (
                f"Comparative textual analysis indicates that the {category} '{element_name}' "
                f"is historically attested in {citations_str}. "
                f"Evidence indicates that this practice/material was utilized in traditional contexts ({support_desc}), "
                f"though its absence in other surveyed records suggests either regional variation or documentation attrition. "
                f"This synthesis remains a cautious hypothesis subject to human cultural verification."
            )

        return hypothesis, confidence
