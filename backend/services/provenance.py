from typing import Dict, Any, List

class ProvenanceService:
    @staticmethod
    def format_citation(source_dict: Dict[str, Any], page_num: int = 1) -> str:
        """
        Format academic bibliographic citation for cultural evidence.
        """
        author = source_dict.get("author") or "Unknown Author"
        year = source_dict.get("year") or "n.d."
        title = source_dict.get("title") or "Untitled Document"
        publisher = source_dict.get("publisher") or "Archival Repository"
        return f"{author} ({year}). {title}. {publisher}, p. {page_num}."

    @staticmethod
    def extract_evidence_snippet(full_text: str, target_phrase: str, window: int = 120) -> str:
        """
        Find exact snippet surrounding the target phrase for evidence display.
        """
        lower_text = full_text.lower()
        lower_phrase = target_phrase.lower()
        idx = lower_text.find(lower_phrase)
        if idx == -1:
            return full_text[:window * 2].strip() + "..."
        start = max(0, idx - window)
        end = min(len(full_text), idx + len(target_phrase) + window)
        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(full_text) else ""
        return f"{prefix}{full_text[start:end].strip()}{suffix}"
