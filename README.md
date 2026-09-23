# Tamil Vanishing Knowledge Detector

### Cultural Memory Engine
**AUREX’26 – Track 06: Open Innovation**

> *"Don't just archive what remains. Detect what is disappearing while there is still time to preserve it."*

---

## 1. Executive Summary & Problem Statement

Most digital cultural preservation projects focus solely on archiving whatever material is readily available in contemporary books and websites. However, cultural attrition occurs silently: subtle preparation steps, oral variants, localized terminology, and hereditary tool methods are omitted from newer manuals and secondary literature, eventually fading from collective human memory.

**The Tamil Vanishing Knowledge Detector** is an AI-assisted comparative cultural knowledge engine. Instead of merely warehousing culture, it compares texts across chronological eras and source typologies (archival records, field monographs, oral interview transcripts, community documentation, and live uploads) to systematically detect:
1. **Potential Knowledge Gaps:** Practices attested in primary or historical records but unmentioned in contemporary or secondary texts.
2. **Missing Procedural Steps:** Specific steps in ancestral sequences (e.g. seed treatments, loom preparation, casting molds, manuscript conditioning) omitted in newer documents.
3. **Evidence-Based Cautious Reconstruction:** Formulating hypotheses about what may have formed part of the practice, supported by verbatim citations and page provenance.
4. **Human Cultural Verification:** Enforcing that AI proposes while human scholars and hereditary community practitioners verify. Only verified entries enter the permanent **Preserved Cultural Knowledge Repository**.

> [!IMPORTANT]
> **Ethical Principle:** The system **never claims** that absence from a source means knowledge is definitely extinct. All gap outputs are cautiously phrased as:  
> *"Potential knowledge gap — requires human cultural verification."*

---

## 2. Seven Cultural Heritage Domains

The platform natively structures knowledge across 7 primary cultural domains and 38 specialized branches:

1. **Folk Culture & Performing Arts (நாட்டுப்புறக் கலைகள் & நிகழ்த்து கலைகள்)**
   - Karagattam (கரகாட்டம்), Oyilattam (ஒயிலாட்டம்), Kummi (கும்மி), Kolattam (கோலாட்டம்), Therukoothu (தெருக்கூத்து), Villupattu (வில்லுப்பாட்டு), Parai Isai (பறை இசை)
2. **Traditional Plants & Herbal Knowledge (பாரம்பரிய தாவரங்கள் & மூலிகை அறிவு)**
   - Medicinal Plants (மருத்துவத் தாவரங்கள்), Herbal Remedies (மூலிகை மருத்துவம்), Sacred Plants (புனிதத் தாவரங்கள்), Wild Edible Plants (காட்டு உணவுகள்), Traditional Plant Uses (தாவர பயன்பாடுகள்)
3. **Marine & Coastal Heritage (கடல்சார் & கடலோர மரபு)**
   - Traditional Fishing (மீன்பிடித்தல்), Boat Building (மரக்கலம் / படகு கட்டுதல்), Fishing Tools (மீன்பிடி கருவிகள்), Coastal Food (கடலோர உணவு முறை), Maritime Traditions (கடல்சார் மரபுகள்)
4. **Weaving & Textiles (நெசவு & ஆடை மரபு)**
   - Handloom (கைத்தறி), Silk Weaving (பட்டு நெசவு), Cotton Textiles (பருத்தி ஆடைகள்), Natural Dyes (இயற்கை சாயங்கள்), Traditional Patterns (பாரம்பரிய உருவங்கள்)
5. **Traditional Crafts & Artisan Heritage (பாரம்பரிய கைவினைக் கலைகள்)**
   - Pottery (மண்பாண்டக் கலை), Bronze Work (வெண்கலச் சிற்பங்கள்), Wood Carving (மரச் சிற்பக்கலை), Stone Carving (கற்சிற்பக்கலை), Palm-Leaf Crafts (பனை ஓலைக் கைவினை)
6. **Agriculture & Indigenous Farming Knowledge (வேளாண்மை & உழவு மரபு)**
   - Traditional Rice (பாரம்பரிய நெல்), Millets (சிறு தானியங்கள்), Seed Preservation (விதை பாதுகாப்பு), Traditional Irrigation (பாசன முறைகள்), Farming Practices (உழவு முறைகள்)
7. **Tamil Books & Literature (தமிழ் நூல்கள் & இலக்கிய மரபு)**
   - Sangam Literature (சங்க இலக்கியம்), Classical Tamil Works (செம்மொழி நூல்கள்), Bhakti Literature (பக்தி இலக்கியம்), Tamil Epics (ஐம்பெருங்காப்பியங்கள்), Poetry (கவிதை மரபு), Grammar Works (இலக்கண நூல்கள்), Palm-Leaf Manuscripts (சுவடி இலக்கியம்)

> [!NOTE]
> The comparison and extraction engine is **100% domain-agnostic**. Adding new domains or branches requires only data insertion in the database, with zero changes to the underlying algorithmic engine.

---

## 3. Real AI/ML Processing Pipeline

```
Live Document / Demo Source (PDF / TXT / JSON / Text)
                         │
                         ▼
        1. Multi-Format Ingestion Engine
       (PyMuPDF fitz / Page Stream Extractor)
                         │
                         ▼
         2. Knowledge Extraction Engine
    (Techniques, Tools, Materials, Process Steps)
                         │
                         ▼
      3. Canonical Normalization & Alignment
   (RapidFuzz similarity, Tamil-English Dictionary)
                         │
                         ▼
         4. Process-Step Sequence Tracker
      (Ordered Stage & Topological Extraction)
                         │
                         ▼
     5. Cross-Source Comparative Matrix (S1..Sn)
(Consistent 🟢, Uncertain 🟡, Potential Gap 🔴, New Knowledge 🔵)
                         │
                         ▼
       6. Potential Gap & Missing Step Engine
      (Unmentioned elements, dropped procedure steps)
                         │
                         ▼
       7. Transparent Urgency Risk Heuristic
      (0-100 Gauge: Scarcity, Age, Contradiction, Elder Risk)
                         │
                         ▼
     8. Evidence-Based Cautious Reconstruction
    (Cautious synthesis: STRONGLY SUPPORTED / POSSIBLE)
           [Optional: Local Ollama LLM Enrichment]
                         │
                         ▼
       9. Human Cultural Verification Portal
       (✓ Verify  |  ✕ Reject  |  ↻ Request Evidence)
                         │
                         ▼
   10. Permanent Preserved Cultural Knowledge Repository
```

- **Core Engine is 100% API-Key-Free:** Uses deterministic Python NLP, RapidFuzz token matching, regex boundary parsing, and PyMuPDF text stream extraction.
- **Optional Local Ollama Support:** If Ollama is running at `http://localhost:11434`, it enriches synthesis phrasing. If Ollama is offline or uninstalled, the system automatically falls back to deterministic NLP with zero errors.

---

## 4. Technology Stack

- **Backend:** Python 3.12 (also supports 3.10 & 3.11), FastAPI, SQLAlchemy, SQLite, Pydantic v2, PyMuPDF (`fitz`), RapidFuzz, Uvicorn.
- **Frontend:** React 18, Vite, Tailwind CSS, Lucide React, bilingual i18n dictionary (English / தமிழ்).
- **Architecture:** Decoupled RESTful API with automated Vite reverse proxy.

---

## 5. Quickstart & Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12 (Python 3.12.10 recommended)
- Node.js 18+ (Node v26.3.0 / npm 11.16.0 tested)

### Backend Setup
```bash
cd backend
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Seed clean demo dataset (all 7 domains & 38 branches)
python seed_demo.py

# 4. Start FastAPI server
uvicorn main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

### Frontend Setup
In a new terminal:
```bash
cd frontend
# 1. Install dependencies
npm install

# 2. Start Vite development server
npm run dev
```
Open your browser at: `http://localhost:5173`

---

## 6. Live Source vs Demo Mode

1. **Demo Mode:** Click **LOAD DEMO DATASET** on the Dashboard or Branch page. Pre-populates all 7 domains and 38 branches with 3 authentic sample sources (S1, S2, S3), 5-8 knowledge elements, potential gaps, verbatim quotes, and urgency scores.
   - Displayed with disclaimer: *"DEMO / SAMPLE DATA — Not independently verified historical evidence."*
2. **Live User Source Mode:** Click **+ ADD LIVE SOURCE** on any branch:
   - Upload real **PDFs**, **TXT** files, **JSON** files, or paste raw transcript text.
   - Collects metadata: Title, Author, Year, Publisher, Source Type, Language.
   - Supports uploading 1, 2, 3, or $N$ sources dynamically via "+ Add Another Source".
   - Displays badge: `LIVE USER SOURCE`.
   - Re-running analysis instantly updates comparison columns ($S_1, S_2, \dots, S_n$) and recalculates gaps.

---

## 7. Automated Test Suite

Run the full pytest suite (13 test cases covering health, dashboard, traditions, gaps, verification, normalization, urgency, scanned PDF handling, and live upload E2E flow):

```bash
cd backend
PYTHONPATH=. .venv/bin/pytest tests/ -v
```

---

## 8. Final Judge Demo Walkthrough (2–4 Minutes)

1. **Dashboard & Philosophy (0:00–0:40):**
   - Open `http://localhost:5173`.
   - Point out the core philosophical message: *"Don't just archive what remains. Detect what is disappearing while there is still time to preserve it."*
   - Toggle language between **English** and **தமிழ்** using the top navbar button.
   - Showcase the 6 aggregate research metrics and the **7 Cultural Heritage Domains** with their icons and urgency scores.

2. **Select Domain & Branch (0:40–1:15):**
   - Click **Folk Culture & Performing Arts** or **Agriculture & Indigenous Farming Knowledge**.
   - Open the **Traditional Rice (பாரம்பரிய நெல்)** branch.
   - Show the 3 existing comparative sources (S1: 1932 Survey, S2: 1984 Oral Transcripts, S3: 2016 Research Monograph).
   - Point out the **Comparison Matrix** with $S_1, S_2, S_3$ checkmarks.
   - Point out the **Potentially Unmentioned Step Alert**: *"Navara Medicinal Paddy Salinity Acclimatization"*.

3. **Live User Source Upload (1:15–2:10):**
   - Click **+ ADD LIVE SOURCE**.
   - Select "Upload File" and pick `backend/data/samples/sample_source_1.txt` (or paste the text directly).
   - Enter title: *"Thanjavur Traditional Rice Protocol (1968)"*.
   - Click "+ Add Another Source" and upload `backend/data/samples/sample_source_2.txt` (*"Modern Farmers Notes (2021)"*).
   - Click **Submit Sources**.
   - Watch the animated **Cultural Analysis Pipeline** execute:
     `Ingesting` $\to$ `Extracting` $\to$ `Normalizing` $\to$ `Comparing` $\to$ `Detecting Gaps` $\to$ `Urgency Heuristic` $\to$ `Reconstructing`.
   - Note the **`LIVE USER SOURCE`** badge and updated comparison columns ($S_1 \dots S_5$).

4. **Evidence Inspection & Cautious Reconstruction (2:10–2:50):**
   - Open the **Evidence Trail & Reconstruction** tab.
   - Inspect the detected missing step: *"Termite mound clay slurry enrobing"*.
   - View exact bibliographic citations and quotes:
     - S1 (1968, p. 1): Attested with exact quote.
     - S2 (2021, p. 1): Unmentioned in text.
   - Show the **Urgency Risk Gauge** (78/100 HIGH) and expand the heuristic factors breakdown.
   - Review the **Evidence-Based Cautious Reconstruction Candidate**:
     *"Available sources suggest that the procedural step... may have traditionally formed part of the sequential workflow..."*

5. **Human Cultural Verification (2:50–3:30):**
   - As human reviewer, click **✓ VERIFY**.
   - Enter annotation: *"Verified by hereditary agro-historians."*
   - Navigate to **Preserved Knowledge** on the sidebar:
     Demonstrate that the item has been immutably recorded into **VERIFIED CULTURAL KNOWLEDGE**.
   - Navigate to the **Knowledge Graph** tab to show dynamic node-link relationships.
   - Open the **Bilingual Glossary** and search for terms like *Mappillai Samba* or *Karagam*.

6. **Closing Statement:**
   > *"We are not asking AI to invent Tamil heritage. We are using AI-assisted comparison to identify what evidence may be disappearing, trace where it came from, and place the final decision with a human reviewer."*
