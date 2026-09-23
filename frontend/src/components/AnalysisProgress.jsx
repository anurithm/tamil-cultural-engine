import React, { useEffect, useState } from 'react';
import { CheckCircle2, Loader2, Sparkles } from 'lucide-react';

const STAGES = [
  { id: 1, label: 'Ingesting sources & page streams' },
  { id: 2, label: 'Extracting knowledge elements & entities' },
  { id: 3, label: 'Normalizing terminology & synonym mapping' },
  { id: 4, label: 'Identifying sequential process steps' },
  { id: 5, label: 'Cross-source comparative matrix generation' },
  { id: 6, label: 'Matching textual evidence & citations' },
  { id: 7, label: 'Detecting potential gaps & missing steps' },
  { id: 8, label: 'Calculating urgency risk heuristic' },
  { id: 9, label: 'Synthesizing evidence-based cautious reconstruction' },
];

export default function AnalysisProgress({ onComplete, lang = 'en' }) {
  const [currentStage, setCurrentStage] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStage((prev) => {
        if (prev < STAGES.length) {
          return prev + 1;
        } else {
          clearInterval(interval);
          if (onComplete) {
            setTimeout(onComplete, 400);
          }
          return prev;
        }
      });
    }, 280);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-5">
        <div className="text-center space-y-1">
          <div className="w-12 h-12 rounded-full bg-amber-50 text-[#6B1D2F] mx-auto flex items-center justify-center border border-amber-200">
            <Sparkles className="w-6 h-6 animate-pulse" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 font-serif-title">
            {lang === 'ta' ? 'கலாச்சார பகுப்பாய்வு இயங்குகிறது' : 'Running Cultural Analysis Pipeline'}
          </h3>
          <p className="text-xs text-slate-500">
            {lang === 'ta'
              ? 'உண்மையான இயற்கை மொழி செயலாக்க ஒப்பீட்டு இயந்திரம் இயங்குகிறது...'
              : 'Generic NLP engine executing cross-source corroboration...'}
          </p>
        </div>

        <div className="space-y-2 py-2">
          {STAGES.map((st) => {
            const isDone = st.id < currentStage;
            const isCurrent = st.id === currentStage;

            return (
              <div
                key={st.id}
                className={`flex items-center space-x-3 text-xs transition-all duration-200 ${
                  isDone
                    ? 'text-emerald-700 font-medium'
                    : isCurrent
                    ? 'text-slate-900 font-bold'
                    : 'text-slate-400'
                }`}
              >
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 text-[#6B1D2F] animate-spin shrink-0" />
                ) : (
                  <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0" />
                )}
                <span>{st.label}</span>
              </div>
            );
          })}
        </div>

        <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
          <div
            className="bg-[#6B1D2F] h-full transition-all duration-300"
            style={{ width: `${(currentStage / STAGES.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}
