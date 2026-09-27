import React, { useState } from 'react';
// Theme palette: bg #2D0A16, card #1a0812, border #4A1528, gold #E8B023, cream #FDF8EC
import {
  Upload, Plus, Trash2, X, CheckCircle, AlertCircle,
  ShieldCheck, Sparkles, AlertTriangle, TrendingUp, Eye, ArrowRight
} from 'lucide-react';
import { translations } from '../i18n/translations';

const SOURCE_TYPES = [
  'Digital Book',
  'Research Paper',
  'Written Record',
  'Oral Interview Transcript',
  'Archival Description',
  'Community Documentation',
  'Manuscript',
  'Other'
];

// ─── Urgency colour helpers ───────────────────────────────────────────────────
function urgencyColors(level) {
  switch (level) {
    case 'CRITICAL': return { bg: 'bg-red-50', border: 'border-red-400', text: 'text-red-800', badge: 'bg-red-600 text-white' };
    case 'HIGH': return { bg: 'bg-orange-50', border: 'border-orange-400', text: 'text-orange-800', badge: 'bg-orange-500 text-white' };
    case 'MEDIUM': return { bg: 'bg-amber-50', border: 'border-amber-400', text: 'text-amber-800', badge: 'bg-amber-500 text-white' };
    default: return { bg: 'bg-emerald-50', border: 'border-emerald-400', text: 'text-emerald-800', badge: 'bg-emerald-600 text-white' };
  }
}

// ─── Per-element status chips ─────────────────────────────────────────────────
function StatusChip({ status, isMissingStep }) {
  if (status === 'CONSISTENT') return <span className="px-2 py-0.5 rounded text-2xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">✓ Consistent</span>;
  if (status === 'NEW_KNOWLEDGE') return <span className="px-2 py-0.5 rounded text-2xs font-bold bg-sky-100 text-sky-800 border border-sky-300">✨ New Knowledge</span>;
  if (isMissingStep) return <span className="px-2 py-0.5 rounded text-2xs font-bold bg-amber-100 text-amber-800 border border-amber-300">⚠ Missing Step</span>;
  return <span className="px-2 py-0.5 rounded text-2xs font-bold bg-rose-100 text-rose-800 border border-rose-300">⚠ Gap Detected</span>;
}

// ─── Decision recommendation label ───────────────────────────────────────────
function DecisionLabel({ status }) {
  if (status === 'CONSISTENT') return <span className="text-emerald-700 font-semibold text-2xs">Preserve ✓</span>;
  if (status === 'NEW_KNOWLEDGE') return <span className="text-sky-700 font-semibold text-2xs">Add New Knowledge</span>;
  return <span className="text-rose-700 font-semibold text-2xs">Needs Review</span>;
}

// ─── Animated progress bar ────────────────────────────────────────────────────
function ScoreBar({ score, level }) {
  const col = level === 'CRITICAL' ? '#dc2626' : level === 'HIGH' ? '#f97316' : level === 'MEDIUM' ? '#f59e0b' : '#10b981';
  return (
    <div className="relative w-full h-2 rounded-full bg-slate-200 overflow-hidden">
      <div
        className="absolute inset-y-0 left-0 rounded-full transition-all duration-700"
        style={{ width: `${score}%`, background: col }}
      />
    </div>
  );
}

export default function AddSourceModal({ branchId, branchName, isOpen, onClose, onSourceAdded, lang = 'en' }) {
  const t = translations[lang];

  const [sources, setSources] = useState([
    {
      id: 1,
      title: '',
      author: '',
      year: '2024',
      publisher: '',
      source_type: 'Written Record',
      language: 'English / Tamil',
      url: '',
      description: '',
      inputType: 'paste',
      file: null,
      pastedText: ''
    }
  ]);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  // ── Analysis results state ──────────────────────────────────────────────────
  const [analysisResult, setAnalysisResult] = useState(null); // null = not done yet

  if (!isOpen) return null;

  // ── Source slot management ──────────────────────────────────────────────────
  const handleAddSourceSlot = () => {
    setSources([
      ...sources,
      {
        id: Date.now(),
        title: '',
        author: '',
        year: '2024',
        publisher: '',
        source_type: 'Community Documentation',
        language: 'English / Tamil',
        url: '',
        description: '',
        inputType: 'paste',
        file: null,
        pastedText: ''
      }
    ]);
  };

  const handleRemoveSourceSlot = (id) => {
    if (sources.length === 1) return;
    setSources(sources.filter((s) => s.id !== id));
  };

  const handleFieldChange = (id, field, value) => {
    setSources(sources.map((s) => (s.id === id ? { ...s, [field]: value } : s)));
  };

  // ── Submit all sources then run analysis ────────────────────────────────────
  const handleSubmitAll = async (e) => {
    e.preventDefault();
    setError(null);
    setAnalysisResult(null);
    setIsSubmitting(true);

    try {
      // Validate
      for (let i = 0; i < sources.length; i++) {
        const s = sources[i];
        if (!s.title.trim()) throw new Error(`Source ${i + 1} requires a Title.`);
        if (s.inputType === 'paste' && !s.pastedText.trim()) throw new Error(`Source ${i + 1} has no pasted text.`);
        if (s.inputType === 'file' && !s.file) throw new Error(`Source ${i + 1} has no file selected.`);
      }

      // Upload each source
      const uploadedSources = [];
      for (const s of sources) {
        const formData = new FormData();
        formData.append('branch_id', branchId);
        formData.append('title', s.title);
        formData.append('author', s.author || 'Community Contributor');
        formData.append('year', s.year || 'Modern');
        formData.append('publisher', s.publisher || 'Field Archival Entry');
        formData.append('source_type', s.source_type);
        formData.append('language', s.language);
        formData.append('url', s.url || '');
        formData.append('description', s.description || '');

        if (s.inputType === 'file' && s.file) {
          formData.append('file', s.file);
        } else {
          formData.append('pasted_text', s.pastedText);
        }

        const res = await fetch('/api/sources/upload', { method: 'POST', body: formData });
        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || `Failed to ingest Source: ${s.title}`);
        }
        const created = await res.json();
        uploadedSources.push(created);
      }

      setIsSubmitting(false);
      setIsAnalyzing(true);

      // Run analysis
      const analyzeRes = await fetch(`/api/analyze?branch_id=${encodeURIComponent(branchId)}`, {
        method: 'POST'
      });
      if (!analyzeRes.ok) {
        const errData = await analyzeRes.json().catch(() => ({}));
        throw new Error(errData.detail || 'Analysis failed.');
      }
      const analyzeData = await analyzeRes.json();

      // Fetch comparison matrix for element-level rows
      const matrixRes = await fetch(`/api/branches/${encodeURIComponent(branchId)}/comparison`);
      const matrixData = matrixRes.ok ? await matrixRes.json() : null;

      setIsAnalyzing(false);
      setAnalysisResult({
        sourcesIngested: uploadedSources.length,
        urgencyScore: analyzeData.branch_urgency_score,
        urgencyLevel: analyzeData.branch_urgency_level,
        matrix: matrixData,
        potentialGapsCount: analyzeData.potential_gaps_count,
        consistentCount: matrixData?.consistent_count ?? 0,
        newKnowledgeCount: matrixData?.new_knowledge_count ?? 0,
        rows: matrixData?.rows ?? []
      });

      // Notify parent to reload data
      if (onSourceAdded) onSourceAdded(uploadedSources);

    } catch (err) {
      setIsSubmitting(false);
      setIsAnalyzing(false);
      setError(err.message);
    }
  };

  // ─── Render analysis results panel ─────────────────────────────────────────
  if (analysisResult) {
    const uc = urgencyColors(analysisResult.urgencyLevel);
    const rows = analysisResult.rows.slice(0, 20); // cap display

    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 overflow-y-auto">
        <div className="rounded-2xl max-w-3xl w-full shadow-2xl my-8 flex flex-col overflow-hidden" style={{ background: '#1a0812', border: '1.5px solid #4A1528' }}>

          {/* ── Header ── */}
          <div className={`px-6 py-5 border-b ${uc.border}`} style={{ background: uc.bg.includes('red') ? '#2d0808' : uc.bg.includes('orange') ? '#2d1408' : uc.bg.includes('amber') ? '#2d1e08' : '#08201a' }}>
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center space-x-2 mb-1">
                  <span className={`px-2.5 py-0.5 rounded-full text-2xs font-extrabold uppercase tracking-wider ${uc.badge}`}>
                    {analysisResult.urgencyLevel}
                  </span>
                  <span className="text-xs font-medium" style={{ color: '#E8B023', opacity: 0.7 }}>
                    {analysisResult.sourcesIngested} source{analysisResult.sourcesIngested > 1 ? 's' : ''} ingested &amp; analysed
                  </span>
                </div>
                <h2 className={`text-xl font-bold font-serif-title ${uc.text}`}>
                  Analysis Complete — {branchName}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Cross-source comparison ran across all {analysisResult.sourcesIngested} submitted sources.
                </p>
              </div>
              <button onClick={onClose} className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Urgency score bar */}
            <div className="mt-4 space-y-1">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className={uc.text}>Cultural Urgency Score</span>
                <span className={`text-2xl font-extrabold ${uc.text}`}>{Math.round(analysisResult.urgencyScore)}<span className="text-sm font-semibold">/100</span></span>
              </div>
              <ScoreBar score={analysisResult.urgencyScore} level={analysisResult.urgencyLevel} />
            </div>
          </div>

          {/* ── Summary Stats Row ── */}
          <div className="grid grid-cols-3 divide-x border-b" style={{ borderColor: '#4A1528', background: '#150309' }}>
            <div className="px-4 py-3 text-center">
              <p className="text-xl font-extrabold text-emerald-700">{analysisResult.consistentCount}</p>
              <p className="text-2xs font-medium mt-0.5" style={{ color: '#E8B023', opacity: 0.6 }}>Consistent Elements</p>
            </div>
            <div className="px-4 py-3 text-center">
              <p className="text-xl font-extrabold text-rose-700">{analysisResult.potentialGapsCount}</p>
              <p className="text-2xs font-medium mt-0.5" style={{ color: '#E8B023', opacity: 0.6 }}>Potential Gaps</p>
            </div>
            <div className="px-4 py-3 text-center">
              <p className="text-xl font-extrabold text-sky-700">{analysisResult.newKnowledgeCount}</p>
              <p className="text-2xs font-medium mt-0.5" style={{ color: '#E8B023', opacity: 0.6 }}>New Knowledge</p>
            </div>
          </div>

          {/* ── Per-element decision table ── */}
          <div className="overflow-y-auto max-h-[40vh] flex-1" style={{ background: '#1a0812' }}>
            {rows.length === 0 ? (
              <div className="p-6 text-center text-xs" style={{ color: '#E8B023', opacity: 0.5 }}>
                No knowledge elements extracted. Try adding more descriptive source text.
              </div>
            ) : (
              <table className="w-full text-left text-xs">
                <thead className="sticky top-0 z-10" style={{ background: '#150309', borderBottom: '1px solid #4A1528' }}>
                  <tr>
                    <th className="px-5 py-2.5 font-semibold uppercase tracking-wider" style={{ color: '#E8B023', opacity: 0.7 }}>Knowledge Element</th>
                    <th className="px-3 py-2.5 font-semibold uppercase tracking-wider" style={{ color: '#E8B023', opacity: 0.7 }}>Status</th>
                    <th className="px-3 py-2.5 font-semibold uppercase tracking-wider" style={{ color: '#E8B023', opacity: 0.7 }}>Decision</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, idx) => (
                    <tr
                      key={idx}
                      style={{
                        borderBottom: '1px solid #2d0e1a',
                        background: row.is_missing_step ? 'rgba(180,120,0,0.08)'
                          : row.status === 'POTENTIAL_GAP' ? 'rgba(180,0,30,0.08)'
                            : row.status === 'NEW_KNOWLEDGE' ? 'rgba(0,100,180,0.08)'
                              : 'transparent'
                      }}
                    >
                      <td className="px-5 py-3">
                        <div className="font-semibold leading-tight" style={{ color: '#FDF8EC' }}>
                          {row.element_name}
                          {row.step_order && (
                            <span className="ml-1.5 text-3xs px-1.5 py-0.2 rounded font-mono align-middle" style={{ background: '#3d1020', color: '#E8B023' }}>
                              Step {row.step_order}
                            </span>
                          )}
                        </div>
                        {row.tamil_term && (
                          <div className="text-2xs tamil-font mt-0.5" style={{ color: '#E8B023' }}>{row.tamil_term}</div>
                        )}
                      </td>
                      <td className="px-3 py-3">
                        <StatusChip status={row.status} isMissingStep={row.is_missing_step} />
                      </td>
                      <td className="px-3 py-3">
                        <DecisionLabel status={row.status} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* ── Cautious disclaimer ── */}
          <div className="px-5 py-2.5 border-t" style={{ background: '#150309', borderColor: '#2d0e1a' }}>
            <p className="text-3xs italic" style={{ color: '#E8B023', opacity: 0.45 }}>
              * Absence from a source does not confirm extinction. All gap detections require human cultural verification before preservation action.
            </p>
          </div>

          {/* ── Footer actions ── */}
          <div className="px-6 py-4 border-t flex items-center justify-between" style={{ borderColor: '#4A1528' }}>
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-xs font-semibold transition-colors" style={{ border: '1px solid #4A1528', color: '#FDF8EC', background: 'transparent' }}
            >
              Done
            </button>
            <button
              onClick={onClose}
              className="px-5 py-2 bg-[#6B1D2F] hover:bg-[#86461b] text-white rounded-lg text-xs font-bold shadow-xs flex items-center space-x-2 transition-colors"
            >
              <Eye className="w-3.5 h-3.5" />
              <span>View Full Comparison</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ─── Uploading / Analysing overlay ─────────────────────────────────────────
  if (isSubmitting || isAnalyzing) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
        <div className="rounded-2xl max-w-sm w-full p-8 shadow-2xl text-center space-y-4" style={{ background: '#1a0812', border: '1.5px solid #4A1528' }}>
          <div className="w-12 h-12 border-4 border-[#6B1D2F]/20 border-t-[#6B1D2F] rounded-full animate-spin mx-auto" />
          <div>
            <p className="text-base font-bold" style={{ color: '#FDF8EC' }}>
              {isSubmitting ? 'Ingesting Sources…' : 'Running Cultural Analysis…'}
            </p>
            <p className="text-xs mt-1" style={{ color: '#E8B023', opacity: 0.6 }}>
              {isSubmitting
                ? `Processing ${sources.length} source${sources.length > 1 ? 's' : ''}…`
                : 'Comparing elements across sources & computing urgency score…'}
            </p>
          </div>
          {/* Progress steps */}
          <div className="text-left space-y-2 pt-2">
            {[
              { label: 'Extracting knowledge elements', done: true },
              { label: 'Running cross-source comparison', done: isAnalyzing },
              { label: 'Computing urgency score', done: isAnalyzing },
              { label: 'Detecting gaps & new knowledge', done: isAnalyzing }
            ].map((step, i) => (
              <div key={i} className="flex items-center space-x-2 text-xs">
                {step.done
                  ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  : <div className="w-3.5 h-3.5 rounded-full border-2 shrink-0" style={{ borderColor: '#4A1528' }} />}
                <span style={{ color: step.done ? '#10b981' : '#E8B023', opacity: step.done ? 1 : 0.4, fontWeight: step.done ? 600 : 400 }}>
                  {step.label}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // ─── Main form (default view) ───────────────────────────────────────────────
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="rounded-2xl max-w-3xl w-full p-6 shadow-2xl my-8 max-h-[90vh] flex flex-col" style={{ background: '#1a0812', border: '1.5px solid #4A1528' }}>

        {/* Header */}
        <div className="flex justify-between items-start pb-4 border-b" style={{ borderColor: '#4A1528' }}>
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-2xs font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300">
                {t.liveBadge}
              </span>
              <span className="text-xs text-slate-500">
                Branch: <strong className="text-slate-800">{branchName}</strong>
              </span>
            </div>
            <h2 className="text-xl font-bold mt-1 font-serif-title" style={{ color: '#FDF8EC' }}>
              {lang === 'ta' ? '+ நேரடி மூலப்பதிவுகளைச் சேர்க்க' : 'Add Live Cultural Sources'}
            </h2>
            <p className="text-xs mt-0.5" style={{ color: '#E8B023', opacity: 0.6 }}>
              {lang === 'ta'
                ? 'PDF, TXT, JSON அல்லது நேரடியாக உரையை ஒட்டவும். பல மூலங்களை ஒரே நேரத்தில் சேர்க்கலாம்.'
                : 'Upload authentic research documents or paste transcript text. Add 2+ sources for cross-comparison & urgency scoring.'}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Error banner */}
        {error && (
          <div className="mt-4 p-3 text-xs rounded-lg flex items-center space-x-2" style={{ background: '#3d0808', border: '1px solid #7a1020', color: '#fca5a5' }}>
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Multi-source form */}
        <form onSubmit={handleSubmitAll} className="mt-4 space-y-6 overflow-y-auto pr-1 flex-1">
          {sources.map((src, index) => (
            <div
              key={src.id}
              className="p-4 rounded-xl space-y-3 relative"
              style={{ background: '#150309', border: '1px solid #4A1528' }}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider flex items-center space-x-1.5" style={{ color: '#FDF8EC' }}>
                  <span className="w-5 h-5 rounded-full bg-[#6B1D2F] text-amber-200 text-2xs flex items-center justify-center font-bold">
                    {index + 1}
                  </span>
                  <span>Source {index + 1}</span>
                </span>
                {sources.length > 1 && (
                  <button
                    type="button"
                    onClick={() => handleRemoveSourceSlot(src.id)}
                    className="text-slate-400 hover:text-rose-600 transition-colors p-1"
                    title="Remove source"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Title & Author */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div>
                  <label className="block font-semibold mb-1" style={{ color: '#E8B023', opacity: 0.8 }}>Document Title *</label>
                  <input
                    type="text"
                    required
                    value={src.title}
                    onChange={(e) => handleFieldChange(src.id, 'title', e.target.value)}
                    placeholder="e.g. Field Ethnography of Thanjavur..."
                    className="w-full px-3 py-2 rounded-lg focus:outline-none"
                    style={{ background: '#2D0A16', border: '1px solid #4A1528', color: '#FDF8EC', boxShadow: 'none' }}
                  />
                </div>
                <div>
                  <label className="block font-semibold mb-1" style={{ color: '#E8B023', opacity: 0.8 }}>Author / Informant</label>
                  <input
                    type="text"
                    value={src.author}
                    onChange={(e) => handleFieldChange(src.id, 'author', e.target.value)}
                    placeholder="e.g. Dr. K. Meenakshisundaram"
                    className="w-full px-3 py-2 rounded-lg focus:outline-none"
                    style={{ background: '#2D0A16', border: '1px solid #4A1528', color: '#FDF8EC' }}
                  />
                </div>
              </div>

              {/* Year, Publisher, Type */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                <div>
                  <label className="block font-semibold mb-1" style={{ color: '#E8B023', opacity: 0.8 }}>Year / Era</label>
                  <input
                    type="text"
                    value={src.year}
                    onChange={(e) => handleFieldChange(src.id, 'year', e.target.value)}
                    placeholder="e.g. 1978 or 2024"
                    className="w-full px-3 py-2 rounded-lg focus:outline-none"
                    style={{ background: '#2D0A16', border: '1px solid #4A1528', color: '#FDF8EC' }}
                  />
                </div>
                <div>
                  <label className="block font-semibold mb-1" style={{ color: '#E8B023', opacity: 0.8 }}>Publisher / Archive</label>
                  <input
                    type="text"
                    value={src.publisher}
                    onChange={(e) => handleFieldChange(src.id, 'publisher', e.target.value)}
                    placeholder="e.g. Saraswathi Mahal Library"
                    className="w-full px-3 py-2 rounded-lg focus:outline-none"
                    style={{ background: '#2D0A16', border: '1px solid #4A1528', color: '#FDF8EC' }}
                  />
                </div>
                <div>
                  <label className="block font-semibold mb-1" style={{ color: '#E8B023', opacity: 0.8 }}>Source Type</label>
                  <select
                    value={src.source_type}
                    onChange={(e) => handleFieldChange(src.id, 'source_type', e.target.value)}
                    className="w-full px-3 py-2 rounded-lg focus:outline-none"
                    style={{ background: '#2D0A16', border: '1px solid #4A1528', color: '#FDF8EC' }}
                  >
                    {SOURCE_TYPES.map((st) => (
                      <option key={st} value={st}>{st}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Input format toggle */}
              <div className="pt-2">
                <div className="flex items-center space-x-4 mb-2 text-xs">
                  <label className="flex items-center space-x-1.5 cursor-pointer font-medium" style={{ color: '#FDF8EC', opacity: 0.8 }}>
                    <input
                      type="radio"
                      name={`input_type_${src.id}`}
                      checked={src.inputType === 'paste'}
                      onChange={() => handleFieldChange(src.id, 'inputType', 'paste')}
                      className="text-[#6B1D2F]"
                    />
                    <span>Paste Document / Transcript Text</span>
                  </label>
                  <label className="flex items-center space-x-1.5 cursor-pointer font-medium" style={{ color: '#FDF8EC', opacity: 0.8 }}>
                    <input
                      type="radio"
                      name={`input_type_${src.id}`}
                      checked={src.inputType === 'file'}
                      onChange={() => handleFieldChange(src.id, 'inputType', 'file')}
                      className="text-[#6B1D2F]"
                    />
                    <span>Upload File (PDF / TXT / JSON)</span>
                  </label>
                </div>

                {src.inputType === 'paste' ? (
                  <textarea
                    rows={4}
                    value={src.pastedText}
                    onChange={(e) => handleFieldChange(src.id, 'pastedText', e.target.value)}
                    placeholder="Paste verbatim source excerpt, interview transcript, or procedural steps here..."
                    className="w-full p-2.5 rounded-lg font-mono text-xs focus:outline-none"
                    style={{ background: '#2D0A16', border: '1px solid #4A1528', color: '#FDF8EC' }}
                  />
                ) : (
                  <div className="border-2 border-dashed rounded-lg p-4 text-center transition-colors" style={{ borderColor: '#4A1528', background: '#150309' }}>
                    <Upload className="w-6 h-6 mx-auto mb-1" style={{ color: '#E8B023', opacity: 0.5 }} />
                    <input
                      type="file"
                      accept=".pdf,.txt,.json"
                      onChange={(e) => handleFieldChange(src.id, 'file', e.target.files[0])}
                      className="text-xs text-slate-500 file:mr-3 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-slate-200 file:text-slate-700 hover:file:bg-slate-300"
                    />
                    {src.file && (
                      <p className="text-xs font-medium mt-1" style={{ color: '#4ade80' }}>
                        Selected: {src.file.name} ({(src.file.size / 1024).toFixed(1)} KB)
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Add Another Source */}
          <button
            type="button"
            onClick={handleAddSourceSlot}
            className="w-full py-2.5 border-2 border-dashed rounded-xl text-xs font-semibold transition-colors flex items-center justify-center space-x-1.5"
            style={{ borderColor: '#4A1528', color: '#E8B023', opacity: 0.7 }}
          >
            <Plus className="w-4 h-4" />
            <span>{t.actions.addAnotherSource}</span>
          </button>

          {/* Hint for multi-source */}
          {sources.length >= 2 && (
            <div className="flex items-start space-x-2 p-3 rounded-lg text-xs" style={{ background: 'rgba(0,100,180,0.12)', border: '1px solid rgba(0,120,220,0.3)', color: '#93c5fd' }}>
              <TrendingUp className="w-3.5 h-3.5 shrink-0 mt-0.5 text-sky-600" />
              <span>
                <strong>Cross-comparison enabled.</strong> After submitting, the engine will compare all {sources.length} sources, detect gaps, compute urgency score, and show you the results inline.
              </span>
            </div>
          )}

          {/* Footer */}
          <div className="pt-4 border-t flex justify-end space-x-3" style={{ borderColor: '#4A1528' }}>
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-xs font-semibold transition-colors"
              style={{ border: '1px solid #4A1528', color: '#FDF8EC', background: 'transparent' }}
            >
              {t.actions.cancel}
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-[#6B1D2F] hover:bg-[#86461b] text-white rounded-lg text-xs font-semibold shadow-xs flex items-center space-x-2"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>{t.actions.submit} ({sources.length})</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
