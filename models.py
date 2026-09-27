from datetime import datetime
import uuid
import json
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Tradition(Base):
    __tablename__ = "traditions"

    id = Column(String(64), primary_key=True, index=True)  # e.g. "folk-culture"
    name = Column(String(128), nullable=False)
    tamil_name = Column(String(256), nullable=False)
    icon = Column(String(64), default="theater")
    description = Column(Text, default="")
    tamil_description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    branches = relationship("Branch", back_populates="tradition", cascade="all, delete-orphan")


class Branch(Base):
    __tablename__ = "branches"

    id = Column(String(64), primary_key=True, index=True)  # e.g. "karagattam"
    tradition_id = Column(String(64), ForeignKey("traditions.id"), nullable=False)
    name = Column(String(128), nullable=False)
    tamil_name = Column(String(256), nullable=False)
    description = Column(Text, default="")
    tamil_description = Column(Text, default="")
    urgency_score = Column(Float, default=0.0)
    urgency_level = Column(String(32), default="LOW")
    created_at = Column(DateTime, default=datetime.utcnow)

    tradition = relationship("Tradition", back_populates="branches")
    sources = relationship("Source", back_populates="branch", cascade="all, delete-orphan")
    knowledge_elements = relationship("KnowledgeElement", back_populates="branch", cascade="all, delete-orphan")
    gaps = relationship("KnowledgeGap", back_populates="branch", cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    branch_id = Column(String(64), ForeignKey("branches.id"), nullable=False)
    title = Column(String(256), nullable=False)
    author = Column(String(128), default="Unknown / Oral Tradition")
    year = Column(String(32), default="Historical")
    publisher = Column(String(256), default="")
    source_type = Column(String(64), default="Digital Book")
    language = Column(String(64), default="English / Tamil")
    url = Column(String(512), default="")
    description = Column(Text, default="")
    is_live = Column(Boolean, default=False)
    raw_content = Column(Text, default="")
    total_pages = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    branch = relationship("Branch", back_populates="sources")
    knowledge_elements = relationship("KnowledgeElement", back_populates="source", cascade="all, delete-orphan")
    evidences = relationship("Evidence", back_populates="source", cascade="all, delete-orphan")


class KnowledgeElement(Base):
    __tablename__ = "knowledge_elements"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    branch_id = Column(String(64), ForeignKey("branches.id"), nullable=False)
    source_id = Column(String(64), ForeignKey("sources.id"), nullable=False)
    category = Column(String(64), default="practice")  # practice, process_step, tool, material, technique, terminology, preparation, sequence, role, location, cultural_context
    name = Column(String(256), nullable=False)
    normalized_key = Column(String(256), nullable=False, index=True)
    tamil_term = Column(String(256), default="")
    evidence_text = Column(Text, default="")
    page_number = Column(Integer, default=1)
    step_order = Column(Integer, nullable=True)  # sequential step index if procedural
    confidence = Column(Float, default=0.85)
    created_at = Column(DateTime, default=datetime.utcnow)

    branch = relationship("Branch", back_populates="knowledge_elements")
    source = relationship("Source", back_populates="knowledge_elements")


class KnowledgeGap(Base):
    __tablename__ = "knowledge_gaps"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    branch_id = Column(String(64), ForeignKey("branches.id"), nullable=False)
    element_key = Column(String(256), nullable=False, index=True)
    element_name = Column(String(256), nullable=False)
    gap_type = Column(String(64), default="missing_element")  # missing_element, missing_step, terminology_conflict, conflicting_account
    status = Column(String(32), default="POTENTIAL_GAP")  # CONSISTENT, UNCERTAIN, POTENTIAL_GAP, NEW_KNOWLEDGE
    description = Column(Text, default="")
    details = Column(Text, default="")
    step_order = Column(Integer, nullable=True)
    urgency_score = Column(Integer, default=50)
    urgency_factors_json = Column(Text, default="{}")
    reconstruction_hypothesis = Column(Text, default="")
    reconstruction_confidence = Column(String(32), default="POSSIBLE")  # VERIFIED, STRONGLY_SUPPORTED, POSSIBLE, UNSUPPORTED
    verification_status = Column(String(32), default="PENDING")  # PENDING, VERIFIED, REJECTED, NEEDS_MORE_EVIDENCE
    reviewer_notes = Column(Text, default="")
    is_live = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    branch = relationship("Branch", back_populates="gaps")
    evidences = relationship("Evidence", back_populates="gap", cascade="all, delete-orphan")

    @property
    def urgency_factors(self):
        try:
            return json.loads(self.urgency_factors_json or "{}")
        except Exception:
            return {}

    @urgency_factors.setter
    def urgency_factors(self, val):
        self.urgency_factors_json = json.dumps(val)


class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    gap_id = Column(String(64), ForeignKey("knowledge_gaps.id"), nullable=False)
    source_id = Column(String(64), ForeignKey("sources.id"), nullable=False)
    source_title = Column(String(256), default="")
    author = Column(String(128), default="")
    year = Column(String(32), default="")
    page_number = Column(Integer, default=1)
    quote = Column(Text, default="")
    presence_status = Column(String(32), default="present")  # present, absent, uncertain

    gap = relationship("KnowledgeGap", back_populates="evidences")
    source = relationship("Source", back_populates="evidences")


class PreservedKnowledge(Base):
    __tablename__ = "preserved_knowledge"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    branch_id = Column(String(64), nullable=False, index=True)
    tradition_id = Column(String(64), nullable=False, index=True)
    branch_name = Column(String(128), default="")
    tradition_name = Column(String(128), default="")
    title = Column(String(256), nullable=False)
    tamil_title = Column(String(256), default="")
    category = Column(String(64), default="practice")
    reconstructed_text = Column(Text, nullable=False)
    evidence_summary = Column(Text, default="")
    confidence_level = Column(String(32), default="VERIFIED")
    verifier_notes = Column(Text, default="")
    verification_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    tamil_term = Column(String(256), nullable=False)
    transliteration = Column(String(256), default="")
    english_meaning = Column(Text, nullable=False)
    domain_name = Column(String(128), default="")
    branch_name = Column(String(128), default="")
    source_title = Column(String(256), default="")
    is_live = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
