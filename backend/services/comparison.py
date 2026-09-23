from typing import List, Dict, Any, Tuple
from services.normalization import NormalizationService
from rapidfuzz import fuzz

class ComparisonService:
    @staticmethod
    def generate_comparison_matrix(
        sources: List[Dict[str, Any]],
        elements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Build dynamic comparison matrix across N sources.
        Categorizes elements as CONSISTENT, UNCERTAIN, POTENTIAL_GAP, or NEW_KNOWLEDGE.
        """
        source_ids = [s["id"] for s in sources]
        source_map = {s["id"]: s for s in sources}
        total_sources_count = len(sources)

        if total_sources_count == 0:
            return {
                "rows": [],
                "potential_gaps_count": 0,
                "consistent_count": 0,
                "uncertain_count": 0,
                "new_knowledge_count": 0
            }

        # Group elements by normalized key
        grouped_elements: Dict[str, List[Dict[str, Any]]] = {}
        for elem in elements:
            key = elem.get("normalized_key") or NormalizationService.to_canonical_key(elem["name"])
            if key not in grouped_elements:
                grouped_elements[key] = []
            grouped_elements[key].append(elem)

        matrix_rows = []
        gaps_count = 0
        consistent_count = 0
        uncertain_count = 0
        new_knowledge_count = 0

        for norm_key, elem_list in grouped_elements.items():
            # Representative item
            rep = elem_list[0]
            tamil_term = next((e.get("tamil_term") for e in elem_list if e.get("tamil_term")), "")
            category = rep.get("category", "practice")
            step_order = next((e.get("step_order") for e in elem_list if e.get("step_order") is not None), None)

            # Build source presence map
            source_presences = {}
            present_sources = set()

            for elem in elem_list:
                s_id = elem["source_id"]
                present_sources.add(s_id)
                s_title = source_map.get(s_id, {}).get("title", f"Source {s_id[:4]}")
                source_presences[s_id] = {
                    "source_id": s_id,
                    "source_title": s_title,
                    "present": True,
                    "page": elem.get("page_number", 1),
                    "quote": elem.get("evidence_text", ""),
                    "confidence": elem.get("confidence", 0.85)
                }

            # Fill absent sources
            for s_id in source_ids:
                if s_id not in source_presences:
                    s_title = source_map.get(s_id, {}).get("title", f"Source {s_id[:4]}")
                    source_presences[s_id] = {
                        "source_id": s_id,
                        "source_title": s_title,
                        "present": False,
                        "page": None,
                        "quote": None,
                        "confidence": 0.0
                    }

            present_count = len(present_sources)

            # Determine Status
            if total_sources_count == 1:
                status = "NEW_KNOWLEDGE"
                status_label = "Single Source Record"
                explanation = "Documented in the single available source; cross-source corroboration pending."
                new_knowledge_count += 1
            elif present_count == total_sources_count:
                status = "CONSISTENT"
                status_label = "Consistent Corroboration"
                explanation = f"Corroborated across all {total_sources_count} sources examined."
                consistent_count += 1
            elif present_count == 1 and total_sources_count > 1:
                status = "NEW_KNOWLEDGE"
                status_label = "Unique / Source-Specific"
                present_title = source_map.get(list(present_sources)[0], {}).get("title", "One source")
                explanation = f"Documented exclusively in '{present_title}'. Not mentioned in other recorded sources."
                new_knowledge_count += 1
            else:
                # Present in some but absent in others
                status = "POTENTIAL_GAP"
                status_label = "Potential Knowledge Gap"
                missing_titles = [
                    source_map[sid]["title"] for sid in source_ids if sid not in present_sources
                ]
                explanation = (
                    f"Present in {present_count} source(s), but unmentioned in: {', '.join(missing_titles)}. "
                    "Requires human cultural verification."
                )
                gaps_count += 1

            is_missing_step = bool(step_order is not None and status == "POTENTIAL_GAP")

            matrix_rows.append({
                "element_key": norm_key,
                "element_name": rep["name"],
                "tamil_term": tamil_term,
                "category": category,
                "step_order": step_order,
                "source_presences": source_presences,
                "status": status,
                "status_label": status_label,
                "is_missing_step": is_missing_step,
                "explanation": explanation
            })

        # Sort matrix: process steps first by step order, then potential gaps, then others
        def sort_key(row):
            order = 0
            if row["is_missing_step"]:
                order = 1
            elif row["status"] == "POTENTIAL_GAP":
                order = 2
            elif row["status"] == "UNCERTAIN":
                order = 3
            elif row["status"] == "NEW_KNOWLEDGE":
                order = 4
            else:
                order = 5
            step_val = row["step_order"] if row["step_order"] is not None else 999
            return (order, step_val, row["element_name"])

        matrix_rows.sort(key=sort_key)

        return {
            "rows": matrix_rows,
            "potential_gaps_count": gaps_count,
            "consistent_count": consistent_count,
            "uncertain_count": uncertain_count,
            "new_knowledge_count": new_knowledge_count
        }
