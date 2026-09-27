import httpx
from typing import Optional, Dict, Any

OLLAMA_BASE_URL = "http://localhost:11434"

class OllamaClientService:
    @staticmethod
    async def is_available() -> bool:
        """
        Check if local Ollama daemon is reachable.
        """
        try:
            async with httpx.AsyncClient(timeout=0.8) as client:
                res = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    @staticmethod
    async def enrich_reconstruction(
        element_name: str,
        category: str,
        evidence_summary: str,
        model: str = "llama3"
    ) -> Optional[str]:
        """
        Optionally query Ollama to polish cultural reconstruction phrasing.
        Falls back to None if Ollama is not running.
        """
        available = await OllamaClientService.is_available()
        if not available:
            return None

        prompt = (
            f"As a cultural heritage researcher, formulate a cautious 2-sentence synthesis for a potentially missing "
            f"knowledge element '{element_name}' ({category}) in Tamil cultural heritage. "
            f"Evidence points: {evidence_summary}. "
            f"Crucial guideline: Do not claim it is definitely lost or invent details; state it as a cautious hypothesis."
        )

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.post(
                    f"{OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    return data.get("response", "").strip()
        except Exception:
            return None

        return None
