import pytest
from fastapi.testclient import TestClient
from main import app
from services.normalization import NormalizationService
from services.extraction import KnowledgeExtractionService
from services.comparison import ComparisonService
from services.gap_detector import GapDetectorService
from services.urgency import UrgencyCalculationService
from services.reconstruction import ReconstructionService
from services.ingestion import DocumentIngestionService, IngestionError

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "Cultural Memory Engine" in data["service"] or "Tamil" in data["service"]

def test_dashboard_endpoint():
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert data["total_traditions"] == 7
    assert len(data["traditions"]) == 7
    assert data["total_sources"] > 0
    assert data["total_gaps"] > 0

def test_traditions_endpoint():
    res = client.get("/api/traditions")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 7
    domain_ids = [d["id"] for d in data]
    assert "folk-culture" in domain_ids
    assert "traditional-plants" in domain_ids
    assert "marine-coastal" in domain_ids
    assert "weaving-textiles" in domain_ids
    assert "traditional-crafts" in domain_ids
    assert "agriculture-farming" in domain_ids
    assert "tamil-literature" in domain_ids

def test_branch_detail_and_comparison():
    res = client.get("/api/branches/karagattam")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Karagattam"
    assert data["sources_count"] >= 3

    comp_res = client.get("/api/branches/karagattam/comparison")
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert len(comp_data["sources"]) >= 3
    assert len(comp_data["rows"]) > 0

def test_gaps_endpoint():
    res = client.get("/api/gaps?branch_id=karagattam")
    assert res.status_code == 200
    gaps = res.json()
    assert len(gaps) >= 1
    gap = gaps[0]
    assert "evidences" in gap
    assert len(gap["evidences"]) >= 2
    assert "urgency_factors" in gap
    assert gap["urgency_score"] > 0

def test_verification_flow():
    # Fetch a pending gap
    res = client.get("/api/gaps?verification_status=PENDING")
    gaps = res.json()
    assert len(gaps) > 0
    target_gap = gaps[0]

    # Verify gap
    verify_res = client.post(
        f"/api/gaps/{target_gap['id']}/verify",
        json={"notes": "Verified by historical review test."}
    )
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "verified"

    # Confirm it appears in preserved knowledge
    pres_res = client.get("/api/knowledge")
    assert pres_res.status_code == 200
    pres_items = pres_res.json()
    assert any(p["title"] == f"Verified: {target_gap['element_name']}" for p in pres_items)

def test_glossary_endpoint():
    res = client.get("/api/glossary")
    assert res.status_code == 200
    terms = res.json()
    assert len(terms) >= 10
    assert any("கரகம்" in t["tamil_term"] for t in terms)

def test_graph_endpoint():
    res = client.get("/api/graph/karagattam")
    assert res.status_code == 200
    graph = res.json()
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) > 0
    assert len(graph["edges"]) > 0

def test_normalization_equivalence():
    assert NormalizationService.are_phrases_equivalent("soak the yarn", "yarn soaking")
    assert NormalizationService.are_phrases_equivalent("soaking the thread", "yarn soaking")
    assert NormalizationService.to_canonical_key("soak the yarn") == "yarn_soaking"

def test_urgency_heuristic():
    score, level, factors = UrgencyCalculationService.calculate_urgency(
        total_sources=3,
        present_sources=1,
        is_missing_step=True,
        oldest_year_str="1932"
    )
    assert score >= 65
    assert level in ["HIGH", "CRITICAL"]
    assert factors["is_missing_step"] is True
    assert "disclaimer" in factors

def test_reconstruction_cautious():
    hypo, conf = ReconstructionService.generate_cautious_reconstruction(
        element_name="Margosa Sealing",
        category="process_step",
        is_missing_step=True,
        step_order=3,
        supporting_evidences=[{"author": "Sundaram", "year": "1932", "page_number": 12, "presence_status": "present"}],
        total_sources_count=3
    )
    assert "Available sources suggest" in hypo
    assert conf == "POSSIBLE"
    assert "definitely lost" not in hypo.lower()

def test_ingestion_scanned_pdf_error():
    # Create empty PDF
    import pymupdf
    doc = pymupdf.open()
    doc.new_page() # blank page with no text
    pdf_bytes = doc.tobytes()
    with pytest.raises(IngestionError) as exc_info:
        DocumentIngestionService.extract_from_pdf(pdf_bytes)
    assert "No machine-readable text detected. OCR is required." in str(exc_info.value)
