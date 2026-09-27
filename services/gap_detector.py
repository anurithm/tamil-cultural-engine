from typing import List, Dict, Any, Tuple
import uuid
from services.normalization import NormalizationService

class GapDetectorService:
    @staticmethod
    def detect_gaps_from_matrix(
        matrix_rows: List[Dict[str, Any]],
        sources: List[Dict[str, Any]],
        branch_id: str,
        is_live: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Analyze comparison matrix rows and identify potential knowledge gaps,
        missing process steps, and unmentioned practices with cautious phrasing.
        """
        source_map = {s["id"]: s for s in sources}
        detected_gaps = []

        for row in matrix_rows:
            status = row["status"]
            # We flag POTENTIAL_GAP and single-source unique NEW_KNOWLEDGE as review items
            if status not in ["POTENTIAL_GAP", "NEW_KNOWLEDGE", "UNCERTAIN"]:
                continue

            element_key = row["element_key"]
            element_name = row["element_name"]
            is_step = row["is_missing_step"]
            step_order = row["step_order"]
            presences = row["source_presences"]

            present_source_ids = [sid for sid, p in presences.items() if p["present"]]
            absent_source_ids = [sid for sid, p in presences.items() if not p["present"]]

            present_titles = [source_map[sid]["title"] for sid in present_source_ids if sid in source_map]
            absent_titles = [source_map[sid]["title"] for sid in absent_source_ids if sid in source_map]

            if is_step:
                gap_type = "missing_step"
                description = f"Potentially Unmentioned Step: {element_name}"
                details = (
                    f"This procedural step (Step {step_order}) was documented in {', '.join(present_titles)}, "
                    f"but was not detected in {', '.join(absent_titles)}. "
                    "This represents a potential knowledge gap across the comparative textual record, "
                    "which requires human cultural verification."
                )
            elif status == "POTENTIAL_GAP":
                gap_type = "missing_element"
                description = f"Potential Knowledge Gap: {element_name}"
                details = (
                    f"The knowledge element '{element_name}' ({row['category']}) is attested in "
                    f"{', '.join(present_titles)}, but absent in {', '.join(absent_titles)}. "
                    "Note: Absence from a specific source does not establish that this knowledge was extinct in practice."
                )
            elif status == "NEW_KNOWLEDGE":
                gap_type = "source_specific_element"
                description = f"Single-Source Knowledge Element: {element_name}"
                details = (
                    f"Documented exclusively in {', '.join(present_titles)}. "
                    "No corroborating mention was detected in the other surveyed sources."
                )
            else:
                gap_type = "terminology_conflict"
                description = f"Uncertain Documentation: {element_name}"
                details = f"Varying descriptions or ambiguous matches observed across surveyed sources."

            # Construct evidences for this gap
            evidence_items = []
            for sid in present_source_ids:
                p = presences[sid]
                s_obj = source_map.get(sid, {})
                evidence_items.append({
                    "id": str(uuid.uuid4()),
                    "source_id": sid,
                    "source_title": s_obj.get("title", "Unknown Source"),
                    "author": s_obj.get("author", "Unknown"),
                    "year": str(s_obj.get("year", "Historical")),
                    "page_number": p.get("page") or 1,
                    "quote": p.get("quote") or f"Direct reference to {element_name}",
                    "presence_status": "present"
                })

            for sid in absent_source_ids:
                s_obj = source_map.get(sid, {})
                evidence_items.append({
                    "id": str(uuid.uuid4()),
                    "source_id": sid,
                    "source_title": s_obj.get("title", "Unknown Source"),
                    "author": s_obj.get("author", "Unknown"),
                    "year": str(s_obj.get("year", "Historical")),
                    "page_number": 1,
                    "quote": f"No mention or documentation of '{element_name}' was found in this source text.",
                    "presence_status": "absent"
                })

            gap_dict = {
                "id": str(uuid.uuid4()),
                "branch_id": branch_id,
                "element_key": element_key,
                "element_name": element_name,
                "gap_type": gap_type,
                "status": status,
                "description": description,
                "details": details,
                "step_order": step_order,
                "is_live": is_live,
                "evidences": evidence_items
            }
            detected_gaps.append(gap_dict)

        return detected_gaps
