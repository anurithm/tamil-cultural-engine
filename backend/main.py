from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import uuid
from datetime import datetime

from database import engine, get_db, Base
from models import (
    Tradition, Branch, Source, KnowledgeElement, KnowledgeGap,
    Evidence, PreservedKnowledge, GlossaryTerm
)
from schemas import (
    TraditionOut, BranchSummary, BranchDetailOut, SourceCreate, SourceOut,
    KnowledgeElementOut, KnowledgeGapOut, EvidenceOut, ComparisonMatrixData,
    VerificationActionRequest, PreservedKnowledgeOut, GlossaryTermOut,
    GraphData, GraphNode, GraphEdge, DashboardStats
)
from services.ingestion import DocumentIngestionService, IngestionError
from services.extraction import KnowledgeExtractionService
from services.normalization import NormalizationService
from services.comparison import ComparisonService
from services.gap_detector import GapDetectorService
from services.urgency import UrgencyCalculationService
from services.reconstruction import ReconstructionService
from services.ollama_client import OllamaClientService
import seed_demo

# Initialize tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tamil Vanishing Knowledge Detector",
    description="Cultural Memory Engine for AUREX'26 Track 06",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    ollama_ok = await OllamaClientService.is_available()
    return {
        "status": "healthy",
        "service": "Tamil Vanishing Knowledge Detector",
        "tagline": "Don't just archive what remains. Detect what is disappearing while there is still time to preserve it.",
        "version": "1.0.0",
        "ollama_available": ollama_ok
    }


@app.get("/api/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    traditions = db.query(Tradition).all()
    total_sources = db.query(Source).count()
    total_elements = db.query(KnowledgeElement).count()
    total_gaps = db.query(KnowledgeGap).filter(KnowledgeGap.status == "POTENTIAL_GAP").count()
    total_pending = db.query(KnowledgeGap).filter(KnowledgeGap.verification_status == "PENDING").count()
    total_verified = db.query(PreservedKnowledge).count()
    has_live_source = db.query(Source).filter(Source.is_live == True).count() > 0

    traditions_out = []
    for t in traditions:
        branches = db.query(Branch).filter(Branch.tradition_id == t.id).all()
        branch_summaries = []
        t_sources = 0
        t_elements = 0
        t_gaps = 0
        urgencies = []

        for b in branches:
            s_count = db.query(Source).filter(Source.branch_id == b.id).count()
            k_count = db.query(KnowledgeElement).filter(KnowledgeElement.branch_id == b.id).count()
            g_count = db.query(KnowledgeGap).filter(
                KnowledgeGap.branch_id == b.id,
                KnowledgeGap.status == "POTENTIAL_GAP"
            ).count()
            p_count = db.query(KnowledgeGap).filter(
                KnowledgeGap.branch_id == b.id,
                KnowledgeGap.verification_status == "PENDING"
            ).count()
            v_count = db.query(PreservedKnowledge).filter(PreservedKnowledge.branch_id == b.id).count()

            t_sources += s_count
            t_elements += k_count
            t_gaps += g_count
            urgencies.append(b.urgency_score or 50.0)

            branch_summaries.append(BranchSummary(
                id=b.id,
                name=b.name,
                tamil_name=b.tamil_name,
                description=b.description,
                tamil_description=b.tamil_description,
                urgency_score=b.urgency_score or 50.0,
                urgency_level=b.urgency_level or "MEDIUM",
                source_count=s_count,
                knowledge_count=k_count,
                gap_count=g_count,
                pending_count=p_count,
                verified_count=v_count
            ))

        avg_urgency = sum(urgencies) / len(urgencies) if urgencies else 50.0
        urgency_lvl = "HIGH" if avg_urgency >= 65 else ("MEDIUM" if avg_urgency >= 40 else "LOW")

        traditions_out.append(TraditionOut(
            id=t.id,
            name=t.name,
            tamil_name=t.tamil_name,
            icon=t.icon,
            description=t.description,
            tamil_description=t.tamil_description,
            branch_count=len(branches),
            source_count=t_sources,
            knowledge_count=t_elements,
            gap_count=t_gaps,
            urgency_score=round(avg_urgency, 1),
            urgency_level=urgency_lvl,
            branches=branch_summaries
        ))

    return DashboardStats(
        total_traditions=len(traditions),
        total_sources=total_sources,
        total_elements=total_elements,
        total_gaps=total_gaps,
        total_pending=total_pending,
        total_verified=total_verified,
        is_live_mode=has_live_source,
        traditions=traditions_out
    )


@app.get("/api/traditions", response_model=List[TraditionOut])
def get_traditions(db: Session = Depends(get_db)):
    dash = get_dashboard_stats(db)
    return dash.traditions


@app.get("/api/traditions/{tradition_id}", response_model=TraditionOut)
def get_tradition(tradition_id: str, db: Session = Depends(get_db)):
    tradition = db.query(Tradition).filter(Tradition.id == tradition_id).first()
    if not tradition:
        raise HTTPException(status_code=404, detail="Tradition domain not found")

    branches = db.query(Branch).filter(Branch.tradition_id == tradition.id).all()
    branch_summaries = []
    t_sources = 0
    t_elements = 0
    t_gaps = 0
    urgencies = []

    for b in branches:
        s_count = db.query(Source).filter(Source.branch_id == b.id).count()
        k_count = db.query(KnowledgeElement).filter(KnowledgeElement.branch_id == b.id).count()
        g_count = db.query(KnowledgeGap).filter(
            KnowledgeGap.branch_id == b.id,
            KnowledgeGap.status == "POTENTIAL_GAP"
        ).count()
        p_count = db.query(KnowledgeGap).filter(
            KnowledgeGap.branch_id == b.id,
            KnowledgeGap.verification_status == "PENDING"
        ).count()
        v_count = db.query(PreservedKnowledge).filter(PreservedKnowledge.branch_id == b.id).count()

        t_sources += s_count
        t_elements += k_count
        t_gaps += g_count
        urgencies.append(b.urgency_score or 50.0)

        branch_summaries.append(BranchSummary(
            id=b.id,
            name=b.name,
            tamil_name=b.tamil_name,
            description=b.description,
            tamil_description=b.tamil_description,
            urgency_score=b.urgency_score or 50.0,
            urgency_level=b.urgency_level or "MEDIUM",
            source_count=s_count,
            knowledge_count=k_count,
            gap_count=g_count,
            pending_count=p_count,
            verified_count=v_count
        ))

    avg_urgency = sum(urgencies) / len(urgencies) if urgencies else 50.0
    urgency_lvl = "HIGH" if avg_urgency >= 65 else "MEDIUM"

    return TraditionOut(
        id=tradition.id,
        name=tradition.name,
        tamil_name=tradition.tamil_name,
        icon=tradition.icon,
        description=tradition.description,
        tamil_description=tradition.tamil_description,
        branch_count=len(branches),
        source_count=t_sources,
        knowledge_count=t_elements,
        gap_count=t_gaps,
        urgency_score=round(avg_urgency, 1),
        urgency_level=urgency_lvl,
        branches=branch_summaries
    )


@app.get("/api/traditions/{tradition_id}/branches", response_model=List[BranchSummary])
def get_tradition_branches(tradition_id: str, db: Session = Depends(get_db)):
    t = get_tradition(tradition_id, db)
    return t.branches


@app.get("/api/branches/{branch_id}", response_model=BranchDetailOut)
def get_branch_detail(branch_id: str, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    tradition = db.query(Tradition).filter(Tradition.id == branch.tradition_id).first()
    sources_count = db.query(Source).filter(Source.branch_id == branch.id).count()
    knowledge_count = db.query(KnowledgeElement).filter(KnowledgeElement.branch_id == branch.id).count()
    gaps_count = db.query(KnowledgeGap).filter(
        KnowledgeGap.branch_id == branch.id,
        KnowledgeGap.status == "POTENTIAL_GAP"
    ).count()
    pending_count = db.query(KnowledgeGap).filter(
        KnowledgeGap.branch_id == branch.id,
        KnowledgeGap.verification_status == "PENDING"
    ).count()
    verified_count = db.query(PreservedKnowledge).filter(PreservedKnowledge.branch_id == branch.id).count()
    has_live = db.query(Source).filter(Source.branch_id == branch.id, Source.is_live == True).count() > 0

    return BranchDetailOut(
        id=branch.id,
        tradition_id=branch.tradition_id,
        tradition_name=tradition.name if tradition else "",
        tradition_tamil_name=tradition.tamil_name if tradition else "",
        name=branch.name,
        tamil_name=branch.tamil_name,
        description=branch.description,
        tamil_description=branch.tamil_description,
        urgency_score=branch.urgency_score or 50.0,
        urgency_level=branch.urgency_level or "MEDIUM",
        sources_count=sources_count,
        knowledge_count=knowledge_count,
        gaps_count=gaps_count,
        pending_count=pending_count,
        verified_count=verified_count,
        is_live=has_live
    )


@app.get("/api/sources", response_model=List[SourceOut])
def get_sources(
    branch_id: Optional[str] = None,
    is_live: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Source)
    if branch_id:
        query = query.filter(Source.branch_id == branch_id)
    if is_live is not None:
        query = query.filter(Source.is_live == is_live)
    return query.order_by(Source.created_at.desc()).all()


@app.post("/api/sources", response_model=SourceOut)
def create_manual_source(data: SourceCreate, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == data.branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    content_text = data.content or data.description or ""
    clean_text, pages_data = DocumentIngestionService.process_pasted_text(
        content_text if content_text.strip() else f"Manual record of {data.title}."
    )

    source = Source(
        id=str(uuid.uuid4()),
        branch_id=data.branch_id,
        title=data.title,
        author=data.author or "Community Record",
        year=data.year or "Modern",
        publisher=data.publisher or "Live Submission",
        source_type=data.source_type or "Community Documentation",
        language=data.language or "English / Tamil",
        url=data.url or "",
        description=data.description or "",
        is_live=True,
        raw_content=clean_text,
        total_pages=len(pages_data)
    )
    db.add(source)
    db.flush()

    # Extract knowledge elements from this new live source
    new_elements = KnowledgeExtractionService.extract_from_pages(
        pages_data=pages_data,
        source_id=source.id,
        source_title=source.title,
        branch_id=branch.id
    )

    for ne in new_elements:
        ke = KnowledgeElement(
            id=ne["id"],
            branch_id=branch.id,
            source_id=source.id,
            category=ne["category"],
            name=ne["name"],
            normalized_key=ne["normalized_key"],
            tamil_term=ne.get("tamil_term", ""),
            evidence_text=ne["evidence_text"],
            page_number=ne["page_number"],
            step_order=ne.get("step_order"),
            confidence=ne.get("confidence", 0.85)
        )
        db.add(ke)

    db.commit()
    db.refresh(source)
    return source


@app.post("/api/sources/upload", response_model=SourceOut)
async def upload_source_file(
    branch_id: str = Form(...),
    title: str = Form(...),
    author: Optional[str] = Form("Unknown"),
    year: Optional[str] = Form("Contemporary"),
    publisher: Optional[str] = Form(""),
    source_type: Optional[str] = Form("Digital Book"),
    language: Optional[str] = Form("English / Tamil"),
    url: Optional[str] = Form(""),
    description: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None),
    pasted_text: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    content_text = ""
    pages_data = []

    if file:
        file_bytes = await file.read()
        if len(file_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        filename = file.filename.lower()
        try:
            if filename.endswith(".pdf"):
                content_text, pages_data = DocumentIngestionService.extract_from_pdf(file_bytes, filename)
            elif filename.endswith(".txt"):
                content_text, pages_data = DocumentIngestionService.extract_from_txt(file_bytes, filename)
            elif filename.endswith(".json"):
                content_text, pages_data, _ = DocumentIngestionService.extract_from_json(file_bytes)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Please upload a PDF, TXT, or JSON file."
                )
        except IngestionError as ie:
            raise HTTPException(status_code=400, detail=str(ie))
    elif pasted_text and pasted_text.strip():
        try:
            content_text, pages_data = DocumentIngestionService.process_pasted_text(pasted_text)
        except IngestionError as ie:
            raise HTTPException(status_code=400, detail=str(ie))
    else:
        raise HTTPException(status_code=400, detail="Either a file or pasted text must be provided.")

    source = Source(
        id=str(uuid.uuid4()),
        branch_id=branch_id,
        title=title,
        author=author or "Unknown",
        year=year or "Contemporary",
        publisher=publisher or "Field Submission",
        source_type=source_type or "Written Record",
        language=language or "English / Tamil",
        url=url or "",
        description=description or "",
        is_live=True,
        raw_content=content_text,
        total_pages=len(pages_data)
    )
    db.add(source)
    db.flush()

    # Generic NLP Extraction
    extracted = KnowledgeExtractionService.extract_from_pages(
        pages_data=pages_data,
        source_id=source.id,
        source_title=source.title,
        branch_id=branch.id
    )

    for item in extracted:
        ke = KnowledgeElement(
            id=item["id"],
            branch_id=branch.id,
            source_id=source.id,
            category=item["category"],
            name=item["name"],
            normalized_key=item["normalized_key"],
            tamil_term=item.get("tamil_term", ""),
            evidence_text=item["evidence_text"],
            page_number=item["page_number"],
            step_order=item.get("step_order"),
            confidence=item.get("confidence", 0.88)
        )
        db.add(ke)

    db.commit()
    db.refresh(source)
    return source


@app.post("/api/analyze")
async def run_cultural_analysis(
    branch_id: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Run full cultural comparison engine on all sources for this branch.
    Re-calculates dynamic matrix, identifies potential gaps & missing steps,
    generates cautious reconstructions, and computes urgency score.
    """
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    sources = db.query(Source).filter(Source.branch_id == branch_id).all()
    if len(sources) == 0:
        raise HTTPException(
            status_code=400,
            detail="No sources available for this branch. Add live sources or load demo data first."
        )

    elements = db.query(KnowledgeElement).filter(KnowledgeElement.branch_id == branch_id).all()

    # Format for service
    sources_data = [
        {
            "id": s.id,
            "title": s.title,
            "author": s.author,
            "year": s.year,
            "source_type": s.source_type,
            "is_live": s.is_live,
            "language": s.language
        }
        for s in sources
    ]

    elements_data = [
        {
            "id": e.id,
            "name": e.name,
            "normalized_key": e.normalized_key,
            "category": e.category,
            "source_id": e.source_id,
            "page_number": e.page_number,
            "step_order": e.step_order,
            "evidence_text": e.evidence_text,
            "tamil_term": e.tamil_term,
            "confidence": e.confidence
        }
        for e in elements
    ]

    # Generate Dynamic Comparison Matrix
    matrix_result = ComparisonService.generate_comparison_matrix(sources_data, elements_data)

    # Detect Gaps
    is_live_branch = any(s.is_live for s in sources)
    detected_gaps = GapDetectorService.detect_gaps_from_matrix(
        matrix_rows=matrix_result["rows"],
        sources=sources_data,
        branch_id=branch.id,
        is_live=is_live_branch
    )

    # Clean old unverified gaps for this branch
    old_gaps = db.query(KnowledgeGap).filter(
        KnowledgeGap.branch_id == branch.id,
        KnowledgeGap.verification_status == "PENDING"
    ).all()
    for og in old_gaps:
        db.query(Evidence).filter(Evidence.gap_id == og.id).delete()
        db.delete(og)
    db.flush()

    # Save new detected gaps & evidences
    saved_gaps = []
    urgency_scores = []

    for gd in detected_gaps:
        # Cautious reconstruction
        is_step = gd.get("gap_type") == "missing_step"
        step_ord = gd.get("step_order")
        evs = gd.get("evidences", [])

        hypo, conf = ReconstructionService.generate_cautious_reconstruction(
            element_name=gd["element_name"],
            category="process_step" if is_step else "practice",
            is_missing_step=is_step,
            step_order=step_ord,
            supporting_evidences=evs,
            total_sources_count=len(sources)
        )

        # Check optional Ollama enrichment
        try:
            enriched_hypo = await OllamaClientService.enrich_reconstruction(
                element_name=gd["element_name"],
                category="process_step" if is_step else "practice",
                evidence_summary=gd["details"]
            )
            if enriched_hypo:
                hypo = enriched_hypo
        except Exception:
            pass

        score, level, factors = UrgencyCalculationService.calculate_urgency(
            total_sources=len(sources),
            present_sources=len([e for e in evs if e["presence_status"] == "present"]),
            is_missing_step=is_step,
            oldest_year_str=sources[0].year,
            source_types=[s.source_type for s in sources]
        )
        urgency_scores.append(score)

        gap_record = KnowledgeGap(
            id=gd["id"],
            branch_id=branch.id,
            element_key=gd["element_key"],
            element_name=gd["element_name"],
            gap_type=gd["gap_type"],
            status=gd["status"],
            description=gd["description"],
            details=gd["details"],
            step_order=step_ord,
            urgency_score=score,
            urgency_factors_json=json.dumps(factors),
            reconstruction_hypothesis=hypo,
            reconstruction_confidence=conf,
            verification_status="PENDING",
            is_live=is_live_branch
        )
        db.add(gap_record)
        db.flush()

        for ev in evs:
            ev_record = Evidence(
                id=ev["id"],
                gap_id=gap_record.id,
                source_id=ev["source_id"],
                source_title=ev["source_title"],
                author=ev["author"],
                year=ev["year"],
                page_number=ev["page_number"],
                quote=ev["quote"],
                presence_status=ev["presence_status"]
            )
            db.add(ev_record)

        saved_gaps.append(gap_record)

    # Update Branch Urgency
    if urgency_scores:
        branch.urgency_score = float(max(urgency_scores))
        branch.urgency_level = "CRITICAL" if branch.urgency_score >= 85 else ("HIGH" if branch.urgency_score >= 65 else "MEDIUM")
    db.commit()

    return {
        "status": "success",
        "message": "Cultural analysis completed successfully.",
        "branch_id": branch.id,
        "sources_count": len(sources),
        "elements_count": len(elements),
        "potential_gaps_count": len(saved_gaps),
        "branch_urgency_score": branch.urgency_score,
        "branch_urgency_level": branch.urgency_level,
        "matrix": matrix_result
    }


@app.get("/api/branches/{branch_id}/comparison", response_model=ComparisonMatrixData)
def get_branch_comparison(branch_id: str, db: Session = Depends(get_db)):
    sources = db.query(Source).filter(Source.branch_id == branch_id).all()
    elements = db.query(KnowledgeElement).filter(KnowledgeElement.branch_id == branch_id).all()
    gaps = db.query(KnowledgeGap).filter(KnowledgeGap.branch_id == branch_id).all()
    gap_map = {g.element_key: g.id for g in gaps}

    sources_data = [
        {
            "id": s.id,
            "title": s.title,
            "author": s.author,
            "year": s.year,
            "source_type": s.source_type,
            "is_live": s.is_live,
            "language": s.language
        }
        for s in sources
    ]

    elements_data = [
        {
            "id": e.id,
            "name": e.name,
            "normalized_key": e.normalized_key,
            "category": e.category,
            "source_id": e.source_id,
            "page_number": e.page_number,
            "step_order": e.step_order,
            "evidence_text": e.evidence_text,
            "tamil_term": e.tamil_term,
            "confidence": e.confidence
        }
        for e in elements
    ]

    matrix_result = ComparisonService.generate_comparison_matrix(sources_data, elements_data)

    # Link gap_id to rows
    for r in matrix_result["rows"]:
        if r["element_key"] in gap_map:
            r["gap_id"] = gap_map[r["element_key"]]

    sources_out = [
        SourceOut(
            id=s.id,
            branch_id=s.branch_id,
            title=s.title,
            author=s.author,
            year=s.year,
            publisher=s.publisher,
            source_type=s.source_type,
            language=s.language,
            url=s.url,
            description=s.description,
            is_live=s.is_live,
            total_pages=s.total_pages,
            created_at=s.created_at
        )
        for s in sources
    ]

    return ComparisonMatrixData(
        branch_id=branch_id,
        sources=sources_out,
        rows=matrix_result["rows"],
        potential_gaps_count=matrix_result["potential_gaps_count"],
        consistent_count=matrix_result["consistent_count"],
        uncertain_count=matrix_result["uncertain_count"],
        new_knowledge_count=matrix_result["new_knowledge_count"]
    )


@app.get("/api/gaps", response_model=List[KnowledgeGapOut])
def get_knowledge_gaps(
    branch_id: Optional[str] = None,
    status: Optional[str] = None,
    verification_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(KnowledgeGap)
    if branch_id:
        query = query.filter(KnowledgeGap.branch_id == branch_id)
    if status:
        query = query.filter(KnowledgeGap.status == status)
    if verification_status:
        query = query.filter(KnowledgeGap.verification_status == verification_status)

    gaps = query.order_by(KnowledgeGap.urgency_score.desc()).all()
    results = []

    for g in gaps:
        branch = db.query(Branch).filter(Branch.id == g.branch_id).first()
        tradition = db.query(Tradition).filter(Tradition.id == branch.tradition_id).first() if branch else None
        evidences = db.query(Evidence).filter(Evidence.gap_id == g.id).all()

        results.append(KnowledgeGapOut(
            id=g.id,
            branch_id=g.branch_id,
            branch_name=branch.name if branch else "",
            tradition_name=tradition.name if tradition else "",
            element_key=g.element_key,
            element_name=g.element_name,
            gap_type=g.gap_type,
            status=g.status,
            description=g.description,
            details=g.details,
            step_order=g.step_order,
            urgency_score=g.urgency_score,
            urgency_factors=g.urgency_factors,
            reconstruction_hypothesis=g.reconstruction_hypothesis,
            reconstruction_confidence=g.reconstruction_confidence,
            verification_status=g.verification_status,
            reviewer_notes=g.reviewer_notes or "",
            is_live=g.is_live,
            created_at=g.created_at,
            evidences=[
                EvidenceOut(
                    id=e.id,
                    gap_id=e.gap_id,
                    source_id=e.source_id,
                    source_title=e.source_title,
                    author=e.author,
                    year=e.year,
                    page_number=e.page_number,
                    quote=e.quote,
                    presence_status=e.presence_status
                )
                for e in evidences
            ]
        ))

    return results


@app.get("/api/gaps/{gap_id}", response_model=KnowledgeGapOut)
def get_gap_by_id(gap_id: str, db: Session = Depends(get_db)):
    g = db.query(KnowledgeGap).filter(KnowledgeGap.id == gap_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Knowledge gap not found")

    branch = db.query(Branch).filter(Branch.id == g.branch_id).first()
    tradition = db.query(Tradition).filter(Tradition.id == branch.tradition_id).first() if branch else None
    evidences = db.query(Evidence).filter(Evidence.gap_id == g.id).all()

    return KnowledgeGapOut(
        id=g.id,
        branch_id=g.branch_id,
        branch_name=branch.name if branch else "",
        tradition_name=tradition.name if tradition else "",
        element_key=g.element_key,
        element_name=g.element_name,
        gap_type=g.gap_type,
        status=g.status,
        description=g.description,
        details=g.details,
        step_order=g.step_order,
        urgency_score=g.urgency_score,
        urgency_factors=g.urgency_factors,
        reconstruction_hypothesis=g.reconstruction_hypothesis,
        reconstruction_confidence=g.reconstruction_confidence,
        verification_status=g.verification_status,
        reviewer_notes=g.reviewer_notes or "",
        is_live=g.is_live,
        created_at=g.created_at,
        evidences=[
            EvidenceOut(
                id=e.id,
                gap_id=e.gap_id,
                source_id=e.source_id,
                source_title=e.source_title,
                author=e.author,
                year=e.year,
                page_number=e.page_number,
                quote=e.quote,
                presence_status=e.presence_status
            )
            for e in evidences
        ]
    )


@app.post("/api/gaps/{gap_id}/reconstruct")
async def trigger_reconstruct(gap_id: str, db: Session = Depends(get_db)):
    gap = db.query(KnowledgeGap).filter(KnowledgeGap.id == gap_id).first()
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")

    evidences = db.query(Evidence).filter(Evidence.gap_id == gap.id).all()
    ev_dicts = [
        {"author": e.author, "year": e.year, "page_number": e.page_number, "presence_status": e.presence_status}
        for e in evidences
    ]

    hypo, conf = ReconstructionService.generate_cautious_reconstruction(
        element_name=gap.element_name,
        category="process_step" if gap.gap_type == "missing_step" else "practice",
        is_missing_step=(gap.gap_type == "missing_step"),
        step_order=gap.step_order,
        supporting_evidences=ev_dicts,
        total_sources_count=len(evidences)
    )

    # Try Ollama enrichment
    try:
        enriched = await OllamaClientService.enrich_reconstruction(
            element_name=gap.element_name,
            category=gap.gap_type,
            evidence_summary=gap.details
        )
        if enriched:
            hypo = enriched
    except Exception:
        pass

    gap.reconstruction_hypothesis = hypo
    gap.reconstruction_confidence = conf
    db.commit()

    return {
        "status": "success",
        "gap_id": gap.id,
        "reconstruction": hypo,
        "confidence": conf
    }


@app.post("/api/gaps/{gap_id}/verify")
def verify_knowledge_gap(
    gap_id: str,
    action: VerificationActionRequest,
    db: Session = Depends(get_db)
):
    gap = db.query(KnowledgeGap).filter(KnowledgeGap.id == gap_id).first()
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")

    gap.verification_status = "VERIFIED"
    gap.reviewer_notes = action.notes or "Verified by cultural researcher."
    gap.reconstruction_confidence = "VERIFIED"

    branch = db.query(Branch).filter(Branch.id == gap.branch_id).first()
    tradition = db.query(Tradition).filter(Tradition.id == branch.tradition_id).first() if branch else None

    # Move to Preserved Knowledge repository
    pres = PreservedKnowledge(
        id=str(uuid.uuid4()),
        branch_id=gap.branch_id,
        tradition_id=branch.tradition_id if branch else "unknown",
        branch_name=branch.name if branch else "",
        tradition_name=tradition.name if tradition else "",
        title=f"Verified: {gap.element_name}",
        tamil_title=f"சரிபார்க்கப்பட்ட மரபு: {gap.element_name}",
        category="process_step" if gap.gap_type == "missing_step" else "practice",
        reconstructed_text=gap.reconstruction_hypothesis,
        evidence_summary=gap.details,
        confidence_level="VERIFIED",
        verifier_notes=gap.reviewer_notes,
        verification_date=datetime.utcnow()
    )
    db.add(pres)
    db.commit()

    return {
        "status": "verified",
        "message": f"Knowledge element '{gap.element_name}' has been verified and added to Preserved Cultural Knowledge.",
        "gap_id": gap.id,
        "preserved_id": pres.id
    }


@app.post("/api/gaps/{gap_id}/reject")
def reject_knowledge_gap(
    gap_id: str,
    action: VerificationActionRequest,
    db: Session = Depends(get_db)
):
    gap = db.query(KnowledgeGap).filter(KnowledgeGap.id == gap_id).first()
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")

    gap.verification_status = "REJECTED"
    gap.reviewer_notes = action.notes or "Rejected due to insufficient historical evidence."
    db.commit()

    return {
        "status": "rejected",
        "message": f"Knowledge element '{gap.element_name}' marked as rejected.",
        "gap_id": gap.id
    }


@app.post("/api/gaps/{gap_id}/request-evidence")
def request_more_evidence(
    gap_id: str,
    action: VerificationActionRequest,
    db: Session = Depends(get_db)
):
    gap = db.query(KnowledgeGap).filter(KnowledgeGap.id == gap_id).first()
    if not gap:
        raise HTTPException(status_code=404, detail="Gap not found")

    gap.verification_status = "NEEDS_MORE_EVIDENCE"
    gap.reviewer_notes = action.notes or "Dispatched to community oral archival backlog."
    db.commit()

    return {
        "status": "needs_more_evidence",
        "message": f"Knowledge element '{gap.element_name}' marked for additional evidence collection.",
        "gap_id": gap.id
    }


@app.get("/api/knowledge", response_model=List[PreservedKnowledgeOut])
def get_preserved_knowledge(
    branch_id: Optional[str] = None,
    tradition_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(PreservedKnowledge)
    if branch_id:
        query = query.filter(PreservedKnowledge.branch_id == branch_id)
    if tradition_id:
        query = query.filter(PreservedKnowledge.tradition_id == tradition_id)
    return query.order_by(PreservedKnowledge.verification_date.desc()).all()


@app.get("/api/glossary", response_model=List[GlossaryTermOut])
def get_glossary(
    query_str: Optional[str] = Query(None, alias="q"),
    domain: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(GlossaryTerm)
    if domain:
        q = q.filter(GlossaryTerm.domain_name.ilike(f"%{domain}%"))
    if query_str:
        q = q.filter(
            (GlossaryTerm.tamil_term.ilike(f"%{query_str}%")) |
            (GlossaryTerm.transliteration.ilike(f"%{query_str}%")) |
            (GlossaryTerm.english_meaning.ilike(f"%{query_str}%"))
        )
    return q.all()


@app.get("/api/graph/{branch_id}", response_model=GraphData)
def get_branch_graph(branch_id: str, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    tradition = db.query(Tradition).filter(Tradition.id == branch.tradition_id).first()
    sources = db.query(Source).filter(Source.branch_id == branch.id).all()
    elements = db.query(KnowledgeElement).filter(KnowledgeElement.branch_id == branch.id).limit(10).all()
    gaps = db.query(KnowledgeGap).filter(KnowledgeGap.branch_id == branch.id).all()
    preserved = db.query(PreservedKnowledge).filter(PreservedKnowledge.branch_id == branch.id).all()

    nodes = []
    edges = []

    # Domain Node
    nodes.append(GraphNode(
        id=tradition.id,
        label=tradition.name,
        type="domain",
        data={"tamil_name": tradition.tamil_name}
    ))

    # Branch Node
    nodes.append(GraphNode(
        id=branch.id,
        label=branch.name,
        type="branch",
        data={"urgency": branch.urgency_score, "level": branch.urgency_level}
    ))
    edges.append(GraphEdge(
        id=f"e_{tradition.id}_{branch.id}",
        source=tradition.id,
        target=branch.id,
        label="contains_branch"
    ))

    # Sources Nodes
    for s in sources:
        nodes.append(GraphNode(
            id=s.id,
            label=s.title[:30] + ("..." if len(s.title) > 30 else ""),
            type="source",
            data={"author": s.author, "year": s.year, "is_live": s.is_live}
        ))
        edges.append(GraphEdge(
            id=f"e_{branch.id}_{s.id}",
            source=branch.id,
            target=s.id,
            label="source_record"
        ))

    # Elements Nodes
    for e in elements:
        nodes.append(GraphNode(
            id=e.id,
            label=e.name[:25],
            type="element",
            data={"category": e.category, "page": e.page_number}
        ))
        edges.append(GraphEdge(
            id=f"e_{e.source_id}_{e.id}",
            source=e.source_id,
            target=e.id,
            label="extracted_from"
        ))

    # Gaps Nodes
    for g in gaps:
        nodes.append(GraphNode(
            id=g.id,
            label=f"GAP: {g.element_name[:20]}",
            type="gap",
            data={
                "urgency": g.urgency_score,
                "status": g.status,
                "reconstruction": g.reconstruction_hypothesis[:80] + "..."
            }
        ))
        edges.append(GraphEdge(
            id=f"e_{branch.id}_{g.id}",
            source=branch.id,
            target=g.id,
            label="detected_gap"
        ))

    # Preserved Nodes
    for p in preserved:
        nodes.append(GraphNode(
            id=p.id,
            label=f"PRESERVED: {p.title[:20]}",
            type="preserved",
            data={"date": str(p.verification_date)}
        ))
        edges.append(GraphEdge(
            id=f"e_{branch.id}_{p.id}",
            source=branch.id,
            target=p.id,
            label="preserved_knowledge"
        ))

    return GraphData(nodes=nodes, edges=edges)


@app.post("/api/demo/load")
def reload_demo_data():
    """
    Re-seeds all 7 domains and branches with complete sample dataset.
    """
    seed_demo.seed_database()
    return {
        "status": "success",
        "message": "Demo sample dataset loaded successfully across all 7 cultural domains.",
        "disclaimer": "DEMO / SAMPLE DATA — Not independently verified historical evidence."
    }
