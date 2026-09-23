import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_full_live_source_ingestion_and_gap_detection():
    branch_id = "traditional-rice"

    # 1. Upload Source 1 (TXT)
    with open("data/samples/sample_source_1.txt", "rb") as f1:
        res1 = client.post(
            "/api/sources/upload",
            data={
                "branch_id": branch_id,
                "title": "Historical Cauvery Protocol (1968)",
                "author": "Thanjavur Society",
                "year": "1968",
                "source_type": "Written Record",
                "language": "English / Tamil",
            },
            files={"file": ("sample_source_1.txt", f1, "text/plain")}
        )
    assert res1.status_code == 200
    s1_data = res1.json()
    assert s1_data["is_live"] is True

    # 2. Upload Source 2 (TXT missing step 3)
    with open("data/samples/sample_source_2.txt", "rb") as f2:
        res2 = client.post(
            "/api/sources/upload",
            data={
                "branch_id": branch_id,
                "title": "Modern Green Collective (2021)",
                "author": "Nagapattinam Farmers",
                "year": "2021",
                "source_type": "Community Documentation",
                "language": "English",
            },
            files={"file": ("sample_source_2.txt", f2, "text/plain")}
        )
    assert res2.status_code == 200
    s2_data = res2.json()
    assert s2_data["is_live"] is True

    # 3. Trigger Cultural Analysis
    res_analyze = client.post(f"/api/analyze?branch_id={branch_id}")
    assert res_analyze.status_code == 200
    analyze_data = res_analyze.json()
    assert analyze_data["status"] == "success"
    assert analyze_data["sources_count"] >= 2
    assert "matrix" in analyze_data

    # 4. Check Comparison Matrix for missing step
    comp_res = client.get(f"/api/branches/{branch_id}/comparison")
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    rows = comp_data["rows"]
    assert len(rows) > 0

    # Look for termite clay slurry step
    termite_step = next(
        (r for r in rows if "termite" in r["element_name"].lower()),
        None
    )
    assert termite_step is not None
    assert termite_step["status"] == "POTENTIAL_GAP"

    # 5. Fetch detected gaps
    gaps_res = client.get(f"/api/gaps?branch_id={branch_id}")
    assert gaps_res.status_code == 200
    gaps = gaps_res.json()
    target_gap = next((g for g in gaps if "termite" in g["element_name"].lower()), None)
    assert target_gap is not None
    assert target_gap["urgency_score"] > 0
    assert len(target_gap["evidences"]) >= 2

    # 6. Human Verification of this Gap
    verify_res = client.post(
        f"/api/gaps/{target_gap['id']}/verify",
        json={"notes": "Corroborated by hereditary agro-historians."}
    )
    assert verify_res.status_code == 200

    # 7. Confirm item is in Preserved Cultural Knowledge
    pres_res = client.get(f"/api/knowledge?branch_id={branch_id}")
    assert pres_res.status_code == 200
    pres_items = pres_res.json()
    assert any("termite" in p["title"].lower() for p in pres_items)
