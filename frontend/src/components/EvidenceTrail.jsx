import React from 'react';
import { Quote, BookOpen, User, Calendar, ShieldCheck, Check, X, RefreshCw, Sparkles } from 'lucide-react';
import { translations } from '../i18n/translations';

export default function EvidenceTrail({ gap, onVerify, onReject, onRequestEvidence, lang = 'en' }) {
  const t = translations[lang];

  if (!gap) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-sm text-slate-500">
        {lang === 'ta'
          ? 'ஆதாரத் தொடரை பார்வையிட ஓர் இடைவெளியை தேர்ந்தெடுக்கவும்.'
          : 'Select a potential knowledge gap to trace historical evidence.'}
      </div>
    );
  }

  const getConfidenceBadge = (conf) => {
    switch (conf) {
      case 'VERIFIED':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'STRONGLY_SUPPORTED':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'POSSIBLE':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-300';
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs space-y-6 p-6">
      {/* Header */}
      <div className="border-b border-slate-100 pb-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider bg-rose-100 text-rose-800 border border-rose-200">
            {gap.status === 'POTENTIAL_GAP' ? t.status.potentialGap : gap.status}
          </span>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-500 font-medium">
              {t.reconstruction.confidenceLabel}:
            </span>
            <span
              className={`px-2 py-0.5 rounded text-xs font-bold border ${getConfidenceBadge(
                gap.reconstruction_confidence
              )}`}
            >
              {gap.reconstruction_confidence}
            </span>
          </div>
        </div>

        <h3 className="mt-2 text-xl font-bold text-slate-900 font-serif-title">
          {gap.element_name}
        </h3>
        <p className="mt-1 text-xs text-slate-600 leading-relaxed">
          {gap.details}
        </p>
      </div>

      {/* Cautious Evidence-Based Reconstruction */}
      <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200/80 space-y-2">
        <div className="flex items-center space-x-2 text-amber-900 font-bold text-xs uppercase tracking-wider">
          <Sparkles className="w-4 h-4 text-amber-600" />
          <span>{t.reconstruction.title}</span>
        </div>
        <p className="text-xs text-amber-950 font-medium leading-relaxed italic bg-white/70 p-3 rounded-lg border border-amber-200/50">
          "{gap.reconstruction_hypothesis || 'Reconstruction hypothesis pending cross-source synthesis.'}"
        </p>
        <p className="text-3xs text-amber-800/80 italic">
          *Note: Synthesized evidence hypothesis. Never presented as definitively established historical fact.
        </p>
      </div>

      {/* Granular Evidences List */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1.5">
          <Quote className="w-4 h-4 text-slate-500" />
          <span>Supporting Document Text & Provenance</span>
        </h4>

        {(!gap.evidences || gap.evidences.length === 0) ? (
          <p className="text-xs text-slate-400 italic">No granular quotes recorded for this item.</p>
        ) : (
          <div className="space-y-3">
            {gap.evidences.map((ev, idx) => {
              const isPresent = ev.presence_status === 'present';
              return (
                <div
                  key={ev.id || idx}
                  className={`p-3.5 rounded-lg border text-xs space-y-2 ${
                    isPresent
                      ? 'bg-slate-50/70 border-slate-200'
                      : 'bg-rose-50/30 border-rose-200/60'
                  }`}
                >
                  <div className="flex items-center justify-between text-slate-800 font-semibold">
                    <span className="flex items-center space-x-2">
                      <BookOpen className="w-3.5 h-3.5 text-slate-500" />
                      <span>{ev.source_title}</span>
                    </span>
                    <span
                      className={`text-2xs font-bold px-2 py-0.5 rounded ${
                        isPresent
                          ? 'bg-emerald-100 text-emerald-800'
                          : 'bg-rose-100 text-rose-800'
                      }`}
                    >
                      {isPresent ? `Attested (p. ${ev.page_number || 1})` : 'Unmentioned in Text'}
                    </span>
                  </div>

                  <div className="flex items-center space-x-4 text-2xs text-slate-500">
                    <span className="flex items-center space-x-1">
                      <User className="w-3 h-3 text-slate-400" />
                      <span>{ev.author || 'Unknown'}</span>
                    </span>
                    <span className="flex items-center space-x-1">
                      <Calendar className="w-3 h-3 text-slate-400" />
                      <span>{ev.year || 'Historical'}</span>
                    </span>
                  </div>

                  {ev.quote && (
                    <blockquote className="mt-1 text-xs text-slate-700 italic border-l-2 border-slate-300 pl-3 py-0.5">
                      "{ev.quote}"
                    </blockquote>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Human Verification Action Bar */}
      <div className="pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
        <div className="text-xs text-slate-500 font-medium">
          Status: <strong className="text-slate-800 uppercase">{gap.verification_status}</strong>
        </div>

        <div className="flex items-center space-x-2">
          {onVerify && (
            <button
              onClick={() => onVerify(gap.id)}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold shadow-2xs transition-colors"
            >
              <Check className="w-3.5 h-3.5" />
              <span>{t.actions.verify}</span>
            </button>
          )}

          {onRequestEvidence && (
            <button
              onClick={() => onRequestEvidence(gap.id)}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 rounded-lg text-xs font-semibold transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>{t.actions.requestEvidence}</span>
            </button>
          )}

          {onReject && (
            <button
              onClick={() => onReject(gap.id)}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-rose-50 text-slate-700 hover:text-rose-700 border border-slate-200 rounded-lg text-xs font-semibold transition-colors"
            >
              <X className="w-3.5 h-3.5" />
              <span>{t.actions.reject}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
