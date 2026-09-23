import React, { useState } from 'react';
import { AlertTriangle, Info, ChevronDown, ChevronUp } from 'lucide-react';
import { translations } from '../i18n/translations';

export default function UrgencyGauge({ score = 50, level = 'MEDIUM', factors = {}, lang = 'en', compact = false }) {
  const [showDetails, setShowDetails] = useState(false);
  const t = translations[lang];

  // Color schemes based on score
  const getColor = (s) => {
    if (s >= 85) return { bg: 'bg-rose-500', text: 'text-rose-700', border: 'border-rose-200', fill: '#EF4444' };
    if (s >= 65) return { bg: 'bg-amber-500', text: 'text-amber-700', border: 'border-amber-200', fill: '#F59E0B' };
    if (s >= 40) return { bg: 'bg-sky-500', text: 'text-sky-700', border: 'border-sky-200', fill: '#0EA5E9' };
    return { bg: 'bg-emerald-500', text: 'text-emerald-700', border: 'border-emerald-200', fill: '#10B981' };
  };

  const theme = getColor(score);

  if (compact) {
    return (
      <div className="flex items-center space-x-2">
        <div className="w-16 bg-slate-100 rounded-full h-2 overflow-hidden border border-slate-200">
          <div
            className={`h-full ${theme.bg}`}
            style={{ width: `${Math.min(100, Math.max(5, score))}%` }}
          />
        </div>
        <span className={`text-xs font-bold ${theme.text}`}>
          {score}/100
        </span>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <AlertTriangle className={`w-4 h-4 ${theme.text}`} />
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            {t.urgency.label}
          </h4>
        </div>
        <span
          className={`px-2 py-0.5 rounded text-xs font-bold ${
            level === 'CRITICAL'
              ? 'bg-rose-100 text-rose-800'
              : level === 'HIGH'
              ? 'bg-amber-100 text-amber-800'
              : level === 'MEDIUM'
              ? 'bg-sky-100 text-sky-800'
              : 'bg-emerald-100 text-emerald-800'
          }`}
        >
          {level}
        </span>
      </div>

      {/* Main Score Bar */}
      <div className="mt-3 flex items-baseline justify-between">
        <div className="flex items-baseline space-x-1">
          <span className="text-3xl font-extrabold text-slate-900 tracking-tight font-serif-title">
            {score}
          </span>
          <span className="text-sm font-semibold text-slate-400">/100</span>
        </div>
        <span className="text-xs font-medium text-slate-500">
          {score >= 80 ? (lang === 'ta' ? 'அவசர கவனம் தேவை' : 'Urgent Attention') : (lang === 'ta' ? 'மிதமான இடர்' : 'Moderate Priority')}
        </span>
      </div>

      <div className="mt-2 w-full bg-slate-100 rounded-full h-2.5 overflow-hidden border border-slate-200/80">
        <div
          className={`h-full transition-all duration-700 ease-out ${theme.bg}`}
          style={{ width: `${Math.min(100, Math.max(5, score))}%` }}
        />
      </div>

      {/* Expandable factors breakdown */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="mt-3 w-full flex items-center justify-between text-xs text-slate-500 hover:text-slate-800 font-medium pt-2 border-t border-slate-100"
      >
        <span className="flex items-center space-x-1">
          <Info className="w-3.5 h-3.5 text-slate-400" />
          <span>{lang === 'ta' ? 'இடர் காரணிகள் பகுப்பாய்வு' : 'View Heuristic Factors'}</span>
        </span>
        {showDetails ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>

      {showDetails && (
        <div className="mt-3 space-y-2 pt-2 border-t border-slate-100 text-xs">
          <div className="flex justify-between text-slate-600">
            <span>{lang === 'ta' ? 'மூலங்களின் பற்றாக்குறை:' : 'Source Scarcity:'}</span>
            <span className="font-semibold text-slate-900">{factors?.source_scarcity || 60}%</span>
          </div>
          <div className="flex justify-between text-slate-600">
            <span>{lang === 'ta' ? 'ஆவணப்படுத்தல் இடைவெளி:' : 'Documentation Scarcity:'}</span>
            <span className="font-semibold text-slate-900">{factors?.documentation_scarcity || 50}%</span>
          </div>
          <div className="flex justify-between text-slate-600">
            <span>{lang === 'ta' ? 'ஆதாரத்தின் தொன்மை:' : 'Age of Documentation:'}</span>
            <span className="font-semibold text-slate-900">{factors?.age_of_evidence || 70}%</span>
          </div>
          <div className="flex justify-between text-slate-600">
            <span>{lang === 'ta' ? 'பாரம்பரிய வல்லுநர்கள் இருப்பு:' : 'Practitioner Rarity:'}</span>
            <span className="font-semibold text-slate-900">{factors?.holder_scarcity || 75}%</span>
          </div>
          {factors?.is_missing_step && (
            <div className="p-1.5 rounded bg-amber-50 text-amber-900 text-2xs font-medium border border-amber-200">
              {lang === 'ta' ? '+15 படிநிலை பாதிப்பு காரணி சேர்க்கப்பட்டது' : '+15 Procedural Step Vulnerability Added'}
            </div>
          )}
        </div>
      )}

      {/* Mandatory Disclaimer */}
      <p className="mt-2 text-2xs text-slate-400 italic leading-tight">
        *{t.urgency.disclaimer}
      </p>
    </div>
  );
}
