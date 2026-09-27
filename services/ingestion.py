import json
import io
from typing import List, Dict, Any, Tuple
import pymupdf

class IngestionError(Exception):
    pass

class DocumentIngestionService:
    @staticmethod
    def extract_from_pdf(file_bytes: bytes, filename: str = "document.pdf") -> Tuple[str, List[Dict[str, Any]]]:
        """
        Extract text from PDF with page numbers and blocks.
        Detects scanned PDFs with no machine-readable text.
        """
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            raise IngestionError(f"Failed to parse PDF file: {str(e)}")

        total_pages = len(doc)
        if total_pages == 0:
            raise IngestionError("PDF file contains no pages.")

        pages_data = []
        full_text_list = []
        has_text = False

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                has_text = True
                full_text_list.append(f"--- Page {page_num + 1} ---\n{text}")
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "line_count": len(text.splitlines())
                })
            else:
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": "",
                    "line_count": 0
                })

        if not has_text:
            raise IngestionError("No machine-readable text detected. OCR is required.")

        full_content = "\n\n".join(full_text_list)
        return full_content, pages_data

    @staticmethod
    def extract_from_txt(file_bytes: bytes, filename: str = "document.txt") -> Tuple[str, List[Dict[str, Any]]]:
        """
        Extract text from plain text file with simulated page breaks every 300 words.
        """
        try:
            text = file_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            try:
                text = file_bytes.decode("latin-1").strip()
            except Exception as e:
                raise IngestionError(f"Unsupported text encoding: {str(e)}")

        if not text:
            raise IngestionError("The text file is empty.")

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        pages_data = []
        
        # Paginate roughly by 300 words for evidence page referencing
        current_page = 1
        current_words = 0
        current_page_text = []

        for p in paragraphs:
            words = p.split()
            current_words += len(words)
            current_page_text.append(p)
            if current_words > 250:
                pages_data.append({
                    "page_number": current_page,
                    "text": "\n\n".join(current_page_text),
                    "line_count": len(current_page_text)
                })
                current_page += 1
                current_words = 0
                current_page_text = []

        if current_page_text:
            pages_data.append({
                "page_number": current_page,
                "text": "\n\n".join(current_page_text),
                "line_count": len(current_page_text)
            })

        return text, pages_data

    @staticmethod
    def extract_from_json(file_bytes: bytes) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
        """
        Extract structured content from JSON file.
        Expects format with optional title, author, and content/sections.
        """
        try:
            data = json.loads(file_bytes.decode("utf-8"))
        except Exception as e:
            raise IngestionError(f"Invalid JSON format: {str(e)}")

        if not isinstance(data, dict):
            raise IngestionError("JSON file must be an object at top level.")

        content = data.get("content") or data.get("text") or ""
        pages_data = []

        if isinstance(content, list):
            # Array of pages or sections
            full_texts = []
            for idx, item in enumerate(content):
                txt = item if isinstance(item, str) else json.dumps(item)
                pages_data.append({
                    "page_number": idx + 1,
                    "text": txt,
                    "line_count": len(txt.splitlines())
                })
                full_texts.append(txt)
            full_content = "\n\n".join(full_texts)
        elif isinstance(content, str):
            if not content.strip():
                # Check for sections or steps in JSON
                sections = data.get("sections") or data.get("steps") or data.get("elements")
                if sections and isinstance(sections, list):
                    content = "\n\n".join([str(s) for s in sections])
                else:
                    content = json.dumps(data, indent=2)
            full_content = content
            pages_data = [{"page_number": 1, "text": full_content, "line_count": len(full_content.splitlines())}]
        else:
            full_content = json.dumps(data, indent=2)
            pages_data = [{"page_number": 1, "text": full_content, "line_count": len(full_content.splitlines())}]

        if not full_content.strip():
            raise IngestionError("JSON source contains no readable text content.")

        return full_content, pages_data, data

    @staticmethod
    def process_pasted_text(text: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Process user pasted text directly.
        """
        clean_text = text.strip()
        if not clean_text:
            raise IngestionError("Pasted text is empty.")

        paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
        pages_data = []
        current_page = 1
        current_words = 0
        current_page_text = []

        for p in paragraphs:
            words = p.split()
            current_words += len(words)
            current_page_text.append(p)
            if current_words > 250:
                pages_data.append({
                    "page_number": current_page,
                    "text": "\n\n".join(current_page_text),
                    "line_count": len(current_page_text)
                })
                current_page += 1
                current_words = 0
                current_page_text = []

        if current_page_text:
            pages_data.append({
                "page_number": current_page,
                "text": "\n\n".join(current_page_text),
                "line_count": len(current_page_text)
            })

        return clean_text, pages_data
