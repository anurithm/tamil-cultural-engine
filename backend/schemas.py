from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Tradition & Branch Schemas ---

class BranchSummary(BaseModel):
    id: str
    name: str
    tamil_name: str
    description: str
    tamil_description: str
    urgency_score: float
    urgency_level: str
    source_count: int = 0
    knowledge_count: int = 0
    gap_count: int = 0
    pending_count: int = 0
    verified_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class TraditionOut(BaseModel):
    id: str
    name: str
    tamil_name: str
    icon: str
    description: str
    tamil_description: str
    branch_count: int = 0
    source_count: int = 0
    knowledge_count: int = 0
    gap_count: int = 0
    urgency_score: float = 0.0
    urgency_level: str = "LOW"
    branches: List[BranchSummary] = []

    model_config = ConfigDict(from_attributes=True)


class BranchDetailOut(BaseModel):
    id: str
    tradition_id: str
    tradition_name: str
    tradition_tamil_name: str
    name: str
    tamil_name: str
    description: str
    tamil_description: str
    urgency_score: float
    urgency_level: str
    sources_count: int
    knowledge_count: int
    gaps_count: int
    pending_count: int
    verified_count: int
    is_live: bool = False

    model_config = ConfigDict(from_attributes=True)


# --- Source Schemas ---

class SourceCreate(BaseModel):
    branch_id: str
    title: str
    author: Optional[str] = "Unknown"
    year: Optional[str] = "Historical"
    publisher: Optional[str] = ""
    source_type: Optional[str] = "Digital Book"
    language: Optional[str] = "English / Tamil"
    url: Optional[str] = ""
    description: Optional[str] = ""
    content: Optional[str] = ""
    is_live: bool = True


class SourceOut(BaseModel):
    id: str
    branch_id: str
    title: str
    author: str
    year: str
    publisher: str
    source_type: str
    language: str
    url: str
    description: str
    is_live: bool
    total_pages: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Knowledge Element Schemas ---

class KnowledgeElementOut(BaseModel):
    id: str
    branch_id: str
    source_id: str
    source_title: Optional[str] = ""
    category: str
    name: str
    normalized_key: str
    tamil_term: str
    evidence_text: str
    page_number: int
    step_order: Optional[int] = None
    confidence: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Evidence Schemas ---

class EvidenceOut(BaseModel):
    id: str
    gap_id: str
    source_id: str
    source_title: str
    author: str
    year: str
    page_number: int
    quote: str
    presence_status: str

    model_config = ConfigDict(from_attributes=True)


# --- Gap Schemas ---

class UrgencyFactors(BaseModel):
    source_scarcity: int = 50
    documentation_scarcity: int = 50
    conflicting_evidence: int = 30
    age_of_evidence: int = 60
    holder_scarcity: int = 70
    independent_source_count: int = 2
    evidence_strength: int = 65


class KnowledgeGapOut(BaseModel):
    id: str
    branch_id: str
    branch_name: Optional[str] = ""
    tradition_name: Optional[str] = ""
    element_key: str
    element_name: str
    gap_type: str
    status: str  # CONSISTENT, UNCERTAIN, POTENTIAL_GAP, NEW_KNOWLEDGE
    description: str
    details: str
    step_order: Optional[int] = None
    urgency_score: int
    urgency_factors: Dict[str, Any] = {}
    reconstruction_hypothesis: str
    reconstruction_confidence: str
    verification_status: str
    reviewer_notes: Optional[str] = ""
    is_live: bool
    created_at: datetime
    evidences: List[EvidenceOut] = []

    model_config = ConfigDict(from_attributes=True)


# --- Comparison Matrix Row ---

class SourcePresence(BaseModel):
    source_id: str
    source_title: str
    present: bool
    page: Optional[int] = None
    quote: Optional[str] = None
    confidence: float = 0.0


class ComparisonMatrixRow(BaseModel):
    element_key: str
    element_name: str
    tamil_term: str
    category: str
    step_order: Optional[int] = None
    source_presences: Dict[str, SourcePresence]  # key: source_id
    status: str  # CONSISTENT, UNCERTAIN, POTENTIAL_GAP, NEW_KNOWLEDGE
    status_label: str
    gap_id: Optional[str] = None
    is_missing_step: bool = False
    explanation: str


class ComparisonMatrixData(BaseModel):
    branch_id: str
    sources: List[SourceOut]
    rows: List[ComparisonMatrixRow]
    potential_gaps_count: int
    consistent_count: int
    uncertain_count: int
    new_knowledge_count: int


# --- Verification & Preserved Knowledge ---

class VerificationActionRequest(BaseModel):
    notes: Optional[str] = ""


class PreservedKnowledgeOut(BaseModel):
    id: str
    branch_id: str
    tradition_id: str
    branch_name: str
    tradition_name: str
    title: str
    tamil_title: str
    category: str
    reconstructed_text: str
    evidence_summary: str
    confidence_level: str
    verifier_notes: str
    verification_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Glossary ---

class GlossaryTermOut(BaseModel):
    id: str
    tamil_term: str
    transliteration: str
    english_meaning: str
    domain_name: str
    branch_name: str
    source_title: str
    is_live: bool

    model_config = ConfigDict(from_attributes=True)


# --- Graph Schemas ---

class GraphNode(BaseModel):
    id: str
    label: str
    type: str  # domain, branch, source, element, gap, evidence, reconstruction, preserved
    data: Dict[str, Any] = {}


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = ""


class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


# --- Dashboard Stats ---

class DashboardStats(BaseModel):
    total_traditions: int
    total_sources: int
    total_elements: int
    total_gaps: int
    total_pending: int
    total_verified: int
    is_live_mode: bool = False
    traditions: List[TraditionOut]
