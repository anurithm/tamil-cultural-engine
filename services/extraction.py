import re
import uuid
from typing import List, Dict, Any, Optional
from services.normalization import NormalizationService

CATEGORY_PATTERNS = {
    "tool": [
        r'\b(?:using|with|by means of|via|instrument|tool|implement|vessel|pot|needle|loom|spindle|chisel|hammer|knife|stylus|net|boat|plow|mortar|pestle|thavil|parai|urumi|kavadi)\b\s+([A-Za-z0-9_\-\s]{3,30})',
        r'\b([A-Za-z0-9_\-\s]{3,25})\s+(?:is used as a tool|serves as the primary instrument|is the traditional implement)\b',
        r'([\u0B80-\u0BFF\s]{3,30})\s+(?:கருவி|பாத்திரம்|பறை|தவில்|எழுத்தாணி|வலை|கலப்பை)'
    ],
    "material": [
        r'\b(?:made of|prepared from|consisting of|ingredient|material|clay|silk|cotton|wood|stone|bronze|wax|turmeric|neem|cow dung|milk|ghee|herbs|palm leaves|coir|yarn|dyes?)\b\s+([A-Za-z0-9_\-\s]{3,30})',
        r'\b([A-Za-z0-9_\-\s]{3,30})\s+(?:is the primary raw material|is mixed together|is blended)\b',
        r'([\u0B80-\u0BFF\s]{3,30})\s+(?:பொருள்|மூலப்பொருள்|மண்|பட்டு|நூல்|களிமண்|சாணம்|நெய்|எண்ணெய்|ஓலை)'
    ],
    "process_step": [
        r'(?:step\s*\d+|stage\s*\d+|firstly|first|secondly|second|thirdly|third|then|next|subsequently|finally|afterward|prior to|during)\s*[:,\-]?\s*([^\.\n;]{10,120})',
        r'(?:முதலாவதாக|இரண்டாவதாக|மூன்றாவதாக|பின்னர்|அதன் பிறகு|இறுதியாக)\s*[:,\-]?\s*([\u0B80-\u0BFF\s]{10,120})',
        r'(?:^\s*\d+[\.\)]\s*)([^\.\n]{8,120})'
    ],
    "technique": [
        r'\b(?:technique|method|system of|art of|manner of|process of|procedure for)\s+([A-Za-z0-9_\-\s]{4,40})',
        r'\b([A-Za-z0-9_\-\s]{4,30})\s+(?:technique is applied|methodology is followed)\b',
        r'([\u0B80-\u0BFF\s]{4,30})\s+(?:முறை|நுட்பம்|வடிவமைப்பு|விதம்)'
    ],
    "terminology": [
        r'(?:known as|termed|called|referred to as|designated as)\s+[\'"]?([A-Za-z0-9_\-\s]{3,35})[\'"]?',
        r'\((?:Tamil:?\s*)?([\u0B80-\u0BFF\s]{3,40})\)',
        r'[\'"]([\u0B80-\u0BFF\s]{3,30})[\'"]\s+(?:என்று அழைக்கப்படும்|எனப்படும்)'
    ],
    "cultural_context": [
        r'\b(?:performed during|celebrated at|sacred to|traditionally observed in|ritual|festival|temple|ceremony|auspicious|folklore|heritage of)\b\s+([A-Za-z0-9_\-\s]{4,50})',
        r'([\u0B80-\u0BFF\s]{4,40})\s+(?:திருவிழா|சடங்கு|வழிபாடு|மரபு|நிகழ்வு)'
    ]
}

STEP_INDICATORS = [
    r'^\s*(\d+)[\.\)]\s+(.*)',
    r'^(?:step|stage)\s+(\d+)[:\s]+(.*)',
    r'^(firstly|first)[\s,:\-]+(.*)',
    r'^(secondly|second)[\s,:\-]+(.*)',
    r'^(thirdly|third)[\s,:\-]+(.*)',
    r'^(fourthly|fourth)[\s,:\-]+(.*)',
    r'^(fifthly|fifth)[\s,:\-]+(.*)',
    r'^(next|then|subsequently)[\s,:\-]+(.*)',
    r'^(finally|lastly)[\s,:\-]+(.*)',
    r'^(முதலாவதாக|ஆரம்பத்தில்)[\s,:\-]+(.*)',
    r'^(இரண்டாவதாக)[\s,:\-]+(.*)',
    r'^(மூன்றாவதாக|பின்னர்)[\s,:\-]+(.*)',
    r'^(இறுதியாக)[\s,:\-]+(.*)',
]

class KnowledgeExtractionService:
    @staticmethod
    def extract_from_pages(
        pages_data: List[Dict[str, Any]],
        source_id: str,
        source_title: str,
        branch_id: str
    ) -> List[Dict[str, Any]]:
        """
        Generic knowledge extraction from paginated document text.
        Extracts entities, steps, tools, materials, and terminology with full provenance.
        """
        extracted_elements = []
        seen_keys = set()
        step_counter = 1

        for page in pages_data:
            page_num = page.get("page_number", 1)
            text = page.get("text", "")
            if not text:
                continue

            lines = text.splitlines()

            # Pass 1: Line-by-line procedural step extraction
            for line in lines:
                clean_line = line.strip()
                if not clean_line or len(clean_line) < 6:
                    continue

                for pattern in STEP_INDICATORS:
                    match = re.match(pattern, clean_line, re.IGNORECASE)
                    if match:
                        step_text = match.group(2).strip() if match.lastindex >= 2 else match.group(1).strip()
                        if len(step_text) > 5:
                            # Clean punctuation
                            step_name = re.sub(r'[\.:;]+$', '', step_text[:80]).strip()
                            norm_key = NormalizationService.to_canonical_key(step_name)
                            unique_signature = f"{norm_key}_{source_id}"

                            if unique_signature not in seen_keys:
                                seen_keys.add(unique_signature)
                                extracted_elements.append({
                                    "id": str(uuid.uuid4()),
                                    "branch_id": branch_id,
                                    "source_id": source_id,
                                    "source_title": source_title,
                                    "category": "process_step",
                                    "name": step_name,
                                    "normalized_key": norm_key,
                                    "tamil_term": KnowledgeExtractionService._extract_tamil_term(clean_line),
                                    "evidence_text": clean_line,
                                    "page_number": page_num,
                                    "step_order": step_counter,
                                    "confidence": 0.92
                                })
                                step_counter += 1
                        break

            # Pass 2: Sentences for Category Patterns (tools, materials, techniques, context)
            # Break text into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            for sentence in sentences:
                clean_sent = sentence.strip()
                if len(clean_sent) < 15:
                    continue

                for category, patterns in CATEGORY_PATTERNS.items():
                    for pat in patterns:
                        for match in re.finditer(pat, clean_sent, re.IGNORECASE):
                            target_phrase = match.group(1).strip()
                            if len(target_phrase) < 3 or len(target_phrase) > 70:
                                continue

                            # Clean phrase
                            cleaned_name = re.sub(r'[\.,;\'"]+', '', target_phrase).strip().title()
                            norm_key = NormalizationService.to_canonical_key(cleaned_name)
                            unique_sig = f"{norm_key}_{source_id}_{category}"

                            if unique_sig not in seen_keys:
                                seen_keys.add(unique_sig)
                                extracted_elements.append({
                                    "id": str(uuid.uuid4()),
                                    "branch_id": branch_id,
                                    "source_id": source_id,
                                    "source_title": source_title,
                                    "category": category,
                                    "name": cleaned_name,
                                    "normalized_key": norm_key,
                                    "tamil_term": KnowledgeExtractionService._extract_tamil_term(clean_sent),
                                    "evidence_text": clean_sent[:300],
                                    "page_number": page_num,
                                    "step_order": None,
                                    "confidence": 0.86
                                })

            # Pass 3: Extract Tamil terms specifically
            tamil_matches = re.findall(r'[\u0B80-\u0BFF]{3,}(?:\s+[\u0B80-\u0BFF]{3,})*', text)
            for tm in tamil_matches:
                tm_clean = tm.strip()
                if len(tm_clean) >= 4 and len(tm_clean) <= 40:
                    norm_key = NormalizationService.to_canonical_key(tm_clean)
                    unique_sig = f"{norm_key}_{source_id}_tamil"
                    if unique_sig not in seen_keys:
                        seen_keys.add(unique_sig)
                        # Find sentence containing this term for provenance
                        quote = next((s.strip() for s in sentences if tm_clean in s), text[:200])
                        extracted_elements.append({
                            "id": str(uuid.uuid4()),
                            "branch_id": branch_id,
                            "source_id": source_id,
                            "source_title": source_title,
                            "category": "terminology",
                            "name": tm_clean,
                            "normalized_key": norm_key,
                            "tamil_term": tm_clean,
                            "evidence_text": quote[:300],
                            "page_number": page_num,
                            "step_order": None,
                            "confidence": 0.89
                        })

        return extracted_elements

    @staticmethod
    def _extract_tamil_term(text: str) -> str:
        """Find any Tamil script words inside the text."""
        match = re.search(r'[\u0B80-\u0BFF]{3,}(?:\s+[\u0B80-\u0BFF]{3,})*', text)
        return match.group(0).strip() if match else ""
