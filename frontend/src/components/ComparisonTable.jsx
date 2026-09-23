import React, { useState } from 'react';
import { Check, Minus, HelpCircle, AlertTriangle, Eye, Sparkles } from 'lucide-react';
import { translations } from '../i18n/translations';

export default function ComparisonTable({ matrixData, onSelectGap, lang = 'en' }) {
  const [selectedRow, setSelectedRow] = useState(null);
  const t = translations[lang];

  if (!matrixData || !matrixData.rows || matrixData.rows.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center">
        <p className="text-sm text-slate-500">
          {lang === 'ta'
            ? 'ஒப்பீட்டுக்கு போதுமான மூலங்கள் இல்லை. நேரடி மூலப்பதிவை பதிவேற்றவும் அல்லது மாதிரி தரவை ஏற்றவும்.'
            : 'Insufficient source records for cross-comparison. Upload live sources or load demo data.'}
        </p>
      </div>
    );
  }

  const { sources, rows } = matrixData;

  const renderStatusBadge = (status, isMissingStep) => {
    switch (status) {
      case 'CONSISTENT':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5"></span>
            {t.status.consistent}
          </span>
        );
      case 'POTENTIAL_GAP':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mr-1.5"></span>
            {isMissingStep ? (lang === 'ta' ? 'விடுபட்ட படிநிலை' : 'Missing Step') : t.status.potentialGap}
          </span>
        );
      case 'NEW_KNOWLEDGE':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-sky-50 text-sky-700 border border-sky-200">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-500 mr-1.5"></span>
            {t.status.newKnowledge}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mr-1.5"></span>
            {t.status.uncertain}
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
      <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/50 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 font-serif-title">
            {t.comparison.matrixTitle}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            {lang === 'ta'
              ? 'மூலங்களுக்கு இடையிலான ஒப்பீடு மற்றும் ஆவணப்படுத்தல் தொடர்ச்சி பகுப்பாய்வு'
              : 'Cross-source documentary presence matrix across surveyed textual records'}
          </p>
        </div>
        <div className="flex items-center space-x-3 text-xs">
          <span className="flex items-center space-x-1 text-emerald-700 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>{matrixData.consistent_count} {t.status.consistent}</span>
          </span>
          <span className="flex items-center space-x-1 text-rose-700 font-medium">
            <span className="w-2 h-2 rounded-full bg-rose-500"></span>
            <span>{matrixData.potential_gaps_count} {t.status.potentialGap}</span>
          </span>
          <span className="flex items-center space-x-1 text-sky-700 font-medium">
            <span className="w-2 h-2 rounded-full bg-sky-500"></span>
            <span>{matrixData.new_knowledge_count} {t.status.newKnowledge}</span>
          </span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-100/70 border-b border-slate-200 text-xs font-semibold text-slate-600 uppercase tracking-wider">
            <tr>
              <th className="px-5 py-3 min-w-[220px]">
                {t.comparison.elementHeader}
              </th>
              <th className="px-3 py-3 min-w-[110px]">
                {t.comparison.categoryHeader}
              </th>
              {sources.map((src, idx) => (
                <th
                  key={src.id}
                  className="px-3 py-3 text-center min-w-[120px] max-w-[160px]"
                  title={`${src.title} (${src.author}, ${src.year})`}
                >
                  <div className="flex flex-col items-center">
                    <span className="font-bold text-slate-800">S{idx + 1}</span>
                    <span className="text-3xs lowercase font-normal truncate max-w-[110px] text-slate-500">
                      {src.title}
                    </span>
                  </div>
                </th>
              ))}
              <th className="px-4 py-3 min-w-[140px]">
                {t.comparison.statusHeader}
              </th>
              <th className="px-4 py-3 text-right min-w-[90px]">
                Action
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((row, idx) => {
              const isMissingStep = row.is_missing_step;
              const isGap = row.status === 'POTENTIAL_GAP';

              return (
                <tr
                  key={idx}
                  className={`hover:bg-slate-50/80 transition-colors ${
                    isMissingStep
                      ? 'bg-amber-50/30'
                      : isGap
                      ? 'bg-rose-50/20'
                      : ''
                  }`}
                >
                  <td className="px-5 py-3.5">
                    <div className="flex items-start space-x-2">
                      {isMissingStep && (
                        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                      )}
                      <div>
                        <div className="font-semibold text-slate-900 flex items-center space-x-2">
                          <span>{row.element_name}</span>
                          {row.step_order && (
                            <span className="text-3xs px-1.5 py-0.2 rounded bg-slate-200 text-slate-700 font-mono">
                              Step {row.step_order}
                            </span>
                          )}
                        </div>
                        {row.tamil_term && (
                          <div className="text-xs text-amber-900/80 tamil-font font-medium mt-0.5">
                            {row.tamil_term}
                          </div>
                        )}
                        <p className="text-xs text-slate-500 mt-1 line-clamp-1">
                          {row.explanation}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td className="px-3 py-3.5">
                    <span className="text-xs text-slate-600 bg-slate-100 px-2 py-0.5 rounded capitalize">
                      {row.category.replace('_', ' ')}
                    </span>
                  </td>
                  {sources.map((src) => {
                    const presence = row.source_presences[src.id];
                    const isPresent = presence && presence.present;
                    return (
                      <td key={src.id} className="px-3 py-3.5 text-center">
                        {isPresent ? (
                          <span
                            className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-emerald-100 text-emerald-700 font-bold"
                            title={`Documented on p. ${presence.page || 1}: "${presence.quote?.slice(0, 100)}..."`}
                          >
                            <Check className="w-4 h-4" />
                          </span>
                        ) : (
                          <span
                            className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-slate-100 text-slate-400 font-bold"
                            title="Not detected in this source text."
                          >
                            <Minus className="w-4 h-4" />
                          </span>
                        )}
                      </td>
                    );
                  })}
                  <td className="px-4 py-3.5">
                    {renderStatusBadge(row.status, isMissingStep)}
                  </td>
                  <td className="px-4 py-3.5 text-right">
                    <button
                      onClick={() => {
                        setSelectedRow(row);
                        if (row.gap_id && onSelectGap) {
                          onSelectGap(row.gap_id);
                        }
                      }}
                      className="inline-flex items-center space-x-1 text-xs font-semibold text-[#6B1D2F] hover:text-[#86461b] px-2.5 py-1 rounded bg-amber-50 hover:bg-amber-100 transition-colors"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>{t.actions.viewEvidence}</span>
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Row Evidence Modal */}
      {selectedRow && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-xs p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full p-6 shadow-xl border border-slate-200 space-y-4 max-h-[85vh] overflow-y-auto">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs uppercase font-bold text-amber-800 tracking-wider">
                  Knowledge Corroboration Inspector
                </span>
                <h3 className="text-lg font-bold text-slate-900 font-serif-title">
                  {selectedRow.element_name}
                </h3>
                {selectedRow.tamil_term && (
                  <p className="text-sm font-medium text-amber-900 tamil-font">
                    {selectedRow.tamil_term}
                  </p>
                )}
              </div>
              <button
                onClick={() => setSelectedRow(null)}
                className="text-slate-400 hover:text-slate-700 text-sm font-semibold"
              >
                ✕
              </button>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg text-xs text-slate-700 leading-relaxed border border-slate-200">
              <span className="font-semibold text-slate-900">Analysis Note: </span>
              {selectedRow.explanation}
            </div>

            <div className="space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600">
                Source Attestations & Provenance
              </h4>
              {sources.map((src, i) => {
                const p = selectedRow.source_presences[src.id];
                const hasIt = p && p.present;
                return (
                  <div
                    key={src.id}
                    className={`p-3.5 rounded-lg border text-xs ${
                      hasIt
                        ? 'bg-emerald-50/50 border-emerald-200'
                        : 'bg-slate-50 border-slate-200'
                    }`}
                  >
                    <div className="flex items-center justify-between font-semibold">
                      <span className="text-slate-900">
                        S{i + 1}: {src.title}
                      </span>
                      {hasIt ? (
                        <span className="text-emerald-700 font-bold flex items-center space-x-1">
                          <Check className="w-3.5 h-3.5" />
                          <span>Present (p. {p.page || 1})</span>
                        </span>
                      ) : (
                        <span className="text-slate-400 flex items-center space-x-1">
                          <Minus className="w-3.5 h-3.5" />
                          <span>Unmentioned</span>
                        </span>
                      )}
                    </div>
                    <div className="text-2xs text-slate-500 mt-0.5">
                      {src.author} &bull; {src.year} &bull; {src.source_type}
                    </div>
                    {hasIt && p.quote && (
                      <blockquote className="mt-2 pl-3 border-l-2 border-emerald-500 text-slate-700 italic">
                        "{p.quote}"
                      </blockquote>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setSelectedRow(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-lg"
              >
                {t.actions.close}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
