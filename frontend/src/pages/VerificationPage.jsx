import React, { useState, useEffect } from 'react';
import { ShieldCheck, Check, X, RefreshCw, Sparkles, Quote, BookOpen, User, Calendar, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';

export default function VerificationPage({ lang = 'en', onSelectBranch }) {
  const [pendingGaps, setPendingGaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedGap, setSelectedGap] = useState(null);
  const [reviewerNotes, setReviewerNotes] = useState('');
  const [actionSuccess, setActionSuccess] = useState(null);
  const t = translations[lang];

  const fetchPending = () => {
    setLoading(true);
    api.getGaps({ verification_status: 'PENDING' })
      .then((data) => {
        setPendingGaps(data);
        if (data.length > 0) {
          setSelectedGap(data[0]);
        } else {
          setSelectedGap(null);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load pending verifications:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchPending();
  }, []);

  const handleVerify = async () => {
    if (!selectedGap) return;
    try {
      await api.verifyGap(selectedGap.id, reviewerNotes || 'Verified by human cultural reviewer.');
      setActionSuccess(`Knowledge element "${selectedGap.element_name}" verified and preserved!`);
      setReviewerNotes('');
      setTimeout(() => setActionSuccess(null), 3500);
      fetchPending();
    } catch (err) {
      alert(`Verification failed: ${err.message}`);
    }
  };

  const handleReject = async () => {
    if (!selectedGap) return;
    try {
      await api.rejectGap(selectedGap.id, reviewerNotes || 'Insufficient historical substantiation.');
      setActionSuccess(`Knowledge element marked as rejected.`);
      setReviewerNotes('');
      setTimeout(() => setActionSuccess(null), 3500);
      fetchPending();
    } catch (err) {
      alert(`Rejection failed: ${err.message}`);
    }
  };

  const handleRequestEvidence = async () => {
    if (!selectedGap) return;
    try {
      await api.requestEvidenceGap(selectedGap.id, reviewerNotes || 'Field verification requested.');
      setActionSuccess(`Dispatched to community collection backlog.`);
      setReviewerNotes('');
      setTimeout(() => setActionSuccess(null), 3500);
      fetchPending();
    } catch (err) {
      alert(`Request failed: ${err.message}`);
    }
  };

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="border-b border-slate-200 pb-5">
        <div className="flex items-center space-x-2">
          <div className="p-2 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
              {lang === 'ta' ? 'மனித சரிபார்ப்பு மையம்' : 'Human-in-the-Loop Cultural Verification Portal'}
            </h1>
            <p className="text-xs text-slate-500">
              {lang === 'ta'
                ? 'AI முன்மொழிந்த மறுகட்டமைப்புகளை நிபுணத்துவ ஆய்வாளர்கள் சரிபார்க்கும் தளம். சரிபார்க்கப்பட்டவை மட்டுமே பாதுகாக்கப்படும்.'
                : 'AI flags potential gaps and drafts cautious hypotheses. Cultural researchers hold the final decision authority.'}
            </p>
          </div>
        </div>
      </div>

      {actionSuccess && (
        <div className="p-3 bg-emerald-50 border border-emerald-300 text-emerald-900 rounded-xl text-xs font-semibold flex items-center space-x-2 shadow-xs">
          <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{actionSuccess}</span>
        </div>
      )}

      {loading ? (
        <div className="p-12 text-center text-xs text-slate-500">Loading pending verifications...</div>
      ) : pendingGaps.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <ShieldCheck className="w-10 h-10 text-emerald-600 mx-auto" />
          <h3 className="text-base font-bold text-slate-900 font-serif-title">
            All Gaps Verified & Processed
          </h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            There are currently no pending items requiring human verification. Verified knowledge is safely recorded in Preserved Cultural Knowledge.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Queue List */}
          <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs h-fit">
            <div className="p-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center text-xs font-bold text-slate-700">
              <span>Pending Review ({pendingGaps.length})</span>
              <span className="text-amber-800 text-2xs font-extrabold uppercase">Requires Human Eye</span>
            </div>

            <div className="divide-y divide-slate-100 max-h-[640px] overflow-y-auto">
              {pendingGaps.map((gap) => {
                const isSelected = selectedGap?.id === gap.id;
                return (
                  <div
                    key={gap.id}
                    onClick={() => setSelectedGap(gap)}
                    className={`p-4 cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-amber-50/80 border-l-4 border-[#6B1D2F]'
                        : 'hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between text-2xs font-semibold text-slate-500">
                      <span>{gap.branch_name}</span>
                      <span className="px-1.5 py-0.5 rounded bg-rose-100 text-rose-800 font-bold">
                        {gap.urgency_score}/100 Urgency
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-slate-900 mt-1">
                      {gap.element_name}
                    </h4>

                    <p className="text-2xs text-slate-500 mt-1 line-clamp-2">
                      {gap.details}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Decision Workspace */}
          {selectedGap && (
            <div className="lg:col-span-8 bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-6">
              {/* Header */}
              <div className="border-b border-slate-100 pb-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded border border-amber-200">
                    {selectedGap.tradition_name} &bull; {selectedGap.branch_name}
                  </span>
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-800">
                    Urgency Score: {selectedGap.urgency_score}/100
                  </span>
                </div>

                <h2 className="mt-2 text-xl font-bold text-slate-900 font-serif-title">
                  {selectedGap.element_name}
                </h2>
                <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                  {selectedGap.details}
                </p>
              </div>

              {/* Evidence-Based Cautious Reconstruction */}
              <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200 space-y-2">
                <div className="flex items-center space-x-2 text-amber-900 text-xs font-bold uppercase tracking-wider">
                  <Sparkles className="w-4 h-4 text-amber-600" />
                  <span>Evidence-Based Cautious Reconstruction Candidate</span>
                </div>
                <blockquote className="text-xs text-amber-950 font-medium leading-relaxed italic bg-white/70 p-3 rounded-lg border border-amber-200/50">
                  "{selectedGap.reconstruction_hypothesis}"
                </blockquote>
                <div className="flex items-center justify-between text-2xs text-amber-900">
                  <span>Confidence: <strong>{selectedGap.reconstruction_confidence}</strong></span>
                  <span className="italic">*Subject to human decision</span>
                </div>
              </div>

              {/* Evidences */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Documentary Evidence Attestation
                </h4>
                <div className="space-y-2">
                  {selectedGap.evidences?.map((ev) => (
                    <div
                      key={ev.id}
                      className={`p-3 rounded-lg border text-xs ${
                        ev.presence_status === 'present'
                          ? 'bg-slate-50 border-slate-200'
                          : 'bg-rose-50/40 border-rose-200'
                      }`}
                    >
                      <div className="flex justify-between items-center font-semibold text-slate-800">
                        <span>{ev.source_title}</span>
                        <span className="text-2xs font-bold">
                          {ev.presence_status === 'present' ? `Attested (p. ${ev.page_number})` : 'Unmentioned'}
                        </span>
                      </div>
                      <div className="text-2xs text-slate-500 mt-0.5">
                        {ev.author} &bull; {ev.year}
                      </div>
                      {ev.quote && (
                        <p className="mt-1 text-xs text-slate-600 italic border-l-2 border-slate-300 pl-2">
                          "{ev.quote}"
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Reviewer Notes & Action Buttons */}
              <div className="pt-4 border-t border-slate-200 space-y-3">
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
                  Human Reviewer Commentary & Preservational Notes
                </label>
                <textarea
                  rows={3}
                  value={reviewerNotes}
                  onChange={(e) => setReviewerNotes(e.target.value)}
                  placeholder="Record justification, field notes, or lineage verification citations..."
                  className="w-full p-3 bg-slate-50 rounded-xl border border-slate-300 text-xs focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
                />

                <div className="flex flex-wrap items-center justify-end gap-3 pt-2">
                  <button
                    onClick={handleReject}
                    className="px-4 py-2 bg-slate-100 hover:bg-rose-50 text-slate-700 hover:text-rose-700 border border-slate-300 rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                  >
                    <X className="w-3.5 h-3.5" />
                    <span>{t.actions.reject}</span>
                  </button>

                  <button
                    onClick={handleRequestEvidence}
                    className="px-4 py-2 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition-colors"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>{t.actions.requestEvidence}</span>
                  </button>

                  <button
                    onClick={handleVerify}
                    className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center space-x-2 shadow-xs transition-colors"
                  >
                    <Check className="w-4 h-4" />
                    <span>{t.actions.verify} &rarr; Preserve</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
