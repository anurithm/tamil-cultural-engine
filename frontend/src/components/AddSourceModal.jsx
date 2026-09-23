import React, { useState } from 'react';
import { Upload, FileText, Plus, Trash2, X, CheckCircle, AlertCircle } from 'lucide-react';
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
      inputType: 'paste', // 'file' or 'paste'
      file: null,
      pastedText: ''
    }
  ]);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  if (!isOpen) return null;

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
    setSources(
      sources.map((s) => (s.id === id ? { ...s, [field]: value } : s))
    );
  };

  const handleSubmitAll = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    setIsSubmitting(true);

    try {
      // Validate all sources
      for (let i = 0; i < sources.length; i++) {
        const s = sources[i];
        if (!s.title.trim()) {
          throw new Error(`Source ${i + 1} requires a Title.`);
        }
        if (s.inputType === 'paste' && !s.pastedText.trim()) {
          throw new Error(`Source ${i + 1} has no pasted text content.`);
        }
        if (s.inputType === 'file' && !s.file) {
          throw new Error(`Source ${i + 1} has no file selected.`);
        }
      }

      // Submit each source
      const results = [];
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

        const res = await fetch('/api/sources/upload', {
          method: 'POST',
          body: formData
        });

        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || `Failed to ingest Source: ${s.title}`);
        }
        const created = await res.json();
        results.push(created);
      }

      setSuccessMsg(
        lang === 'ta'
          ? `${results.length} நேரடி மூலப்பதிவு(கள்) வெற்றிகரமாக இணைக்கப்பட்டன!`
          : `Successfully ingested ${results.length} live source(s)!`
      );

      setTimeout(() => {
        if (onSourceAdded) onSourceAdded(results);
        onClose();
      }, 1000);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-3xl w-full p-6 shadow-2xl border border-slate-200 my-8 max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-start pb-4 border-b border-slate-200">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 rounded text-2xs font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300">
                {t.liveBadge}
              </span>
              <span className="text-xs text-slate-500">
                Branch: <strong className="text-slate-800">{branchName}</strong>
              </span>
            </div>
            <h2 className="text-xl font-bold text-slate-900 mt-1 font-serif-title">
              {lang === 'ta' ? '+ நேரடி மூலப்பதிவுகளைச் சேர்க்க' : 'Add Live Cultural Sources'}
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              {lang === 'ta'
                ? 'PDF, TXT, JSON அல்லது நேரடியாக உரையை ஒட்டவும். பல மூலங்களை ஒரே நேரத்தில் சேர்க்கலாம்.'
                : 'Upload authentic research documents (PDF, TXT, JSON) or paste transcript text for comparative analysis.'}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-700 p-1.5 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Feedback alerts */}
        {error && (
          <div className="mt-4 p-3 bg-rose-50 border border-rose-200 text-rose-800 text-xs rounded-lg flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}
        {successMsg && (
          <div className="mt-4 p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs rounded-lg flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Dynamic Multi-source Form */}
        <form onSubmit={handleSubmitAll} className="mt-4 space-y-6 overflow-y-auto pr-1 flex-1">
          {sources.map((src, index) => (
            <div
              key={src.id}
              className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-3 relative group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center space-x-1.5">
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
                  <label className="block text-slate-700 font-semibold mb-1">
                    Document Title *
                  </label>
                  <input
                    type="text"
                    required
                    value={src.title}
                    onChange={(e) => handleFieldChange(src.id, 'title', e.target.value)}
                    placeholder="e.g. Field Ethnography of Thanjavur..."
                    className="w-full px-3 py-2 bg-white rounded-lg border border-slate-300 focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Author / Informant
                  </label>
                  <input
                    type="text"
                    value={src.author}
                    onChange={(e) => handleFieldChange(src.id, 'author', e.target.value)}
                    placeholder="e.g. Dr. K. Meenakshisundaram"
                    className="w-full px-3 py-2 bg-white rounded-lg border border-slate-300 focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                  />
                </div>
              </div>

              {/* Year, Publisher, Type */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Year / Era
                  </label>
                  <input
                    type="text"
                    value={src.year}
                    onChange={(e) => handleFieldChange(src.id, 'year', e.target.value)}
                    placeholder="e.g. 1978 or 2024"
                    className="w-full px-3 py-2 bg-white rounded-lg border border-slate-300 focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Publisher / Archive
                  </label>
                  <input
                    type="text"
                    value={src.publisher}
                    onChange={(e) => handleFieldChange(src.id, 'publisher', e.target.value)}
                    placeholder="e.g. Saraswathi Mahal Library"
                    className="w-full px-3 py-2 bg-white rounded-lg border border-slate-300 focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Source Type
                  </label>
                  <select
                    value={src.source_type}
                    onChange={(e) => handleFieldChange(src.id, 'source_type', e.target.value)}
                    className="w-full px-3 py-2 bg-white rounded-lg border border-slate-300 focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                  >
                    {SOURCE_TYPES.map((st) => (
                      <option key={st} value={st}>
                        {st}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Input format toggle (File upload vs Paste text) */}
              <div className="pt-2">
                <div className="flex items-center space-x-4 mb-2 text-xs">
                  <label className="flex items-center space-x-1.5 cursor-pointer font-medium text-slate-700">
                    <input
                      type="radio"
                      name={`input_type_${src.id}`}
                      checked={src.inputType === 'paste'}
                      onChange={() => handleFieldChange(src.id, 'inputType', 'paste')}
                      className="text-[#6B1D2F]"
                    />
                    <span>Paste Document / Transcript Text</span>
                  </label>
                  <label className="flex items-center space-x-1.5 cursor-pointer font-medium text-slate-700">
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
                    className="w-full p-2.5 bg-white rounded-lg border border-slate-300 font-mono text-xs focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                  />
                ) : (
                  <div className="border-2 border-dashed border-slate-300 rounded-lg p-4 text-center hover:bg-slate-100/50 transition-colors">
                    <Upload className="w-6 h-6 text-slate-400 mx-auto mb-1" />
                    <input
                      type="file"
                      accept=".pdf,.txt,.json"
                      onChange={(e) => handleFieldChange(src.id, 'file', e.target.files[0])}
                      className="text-xs text-slate-500 file:mr-3 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-slate-200 file:text-slate-700 hover:file:bg-slate-300"
                    />
                    {src.file && (
                      <p className="text-xs text-emerald-700 font-medium mt-1">
                        Selected: {src.file.name} ({(src.file.size / 1024).toFixed(1)} KB)
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Add Another Source button */}
          <button
            type="button"
            onClick={handleAddSourceSlot}
            className="w-full py-2.5 border-2 border-dashed border-slate-300 rounded-xl text-xs font-semibold text-slate-600 hover:text-[#6B1D2F] hover:border-[#6B1D2F] transition-colors flex items-center justify-center space-x-1.5"
          >
            <Plus className="w-4 h-4" />
            <span>{t.actions.addAnotherSource}</span>
          </button>

          {/* Footer Submit */}
          <div className="pt-4 border-t border-slate-200 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-100"
            >
              {t.actions.cancel}
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 bg-[#6B1D2F] hover:bg-[#86461b] text-white rounded-lg text-xs font-semibold shadow-xs flex items-center space-x-2"
            >
              {isSubmitting ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Ingesting Sources...</span>
                </>
              ) : (
                <>
                  <Upload className="w-3.5 h-3.5" />
                  <span>{t.actions.submit} ({sources.length})</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
