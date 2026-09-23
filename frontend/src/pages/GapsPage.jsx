import React, { useState, useEffect } from 'react';
import { GitCompare, Search, AlertTriangle, ShieldCheck, Check, X, RefreshCw, Eye, Sparkles } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';
import EvidenceTrail from '../components/EvidenceTrail';

export default function GapsPage({ onSelectBranch, lang = 'en' }) {
  const [gaps, setGaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedGap, setSelectedGap] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const t = translations[lang];

  const fetchGaps = () => {
    setLoading(true);
    api.getGaps()
      .then((data) => {
        setGaps(data);
        if (data.length > 0 && !selectedGap) {
          setSelectedGap(data[0]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load gaps:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchGaps();
  }, []);

  const handleVerify = async (gapId) => {
    try {
      await api.verifyGap(gapId, 'Verified from global gaps queue.');
      fetchGaps();
    } catch (err) {
      alert(`Verification error: ${err.message}`);
    }
  };

  const handleReject = async (gapId) => {
    try {
      await api.rejectGap(gapId, 'Rejected from global gaps queue.');
      fetchGaps();
    } catch (err) {
      alert(`Rejection error: ${err.message}`);
    }
  };

  const handleRequestEvidence = async (gapId) => {
    try {
      await api.requestEvidenceGap(gapId, 'Evidence requested from global queue.');
      fetchGaps();
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const filteredGaps = gaps.filter((g) => {
    if (statusFilter !== 'ALL' && g.verification_status !== statusFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        g.element_name.toLowerCase().includes(q) ||
        g.branch_name.toLowerCase().includes(q) ||
        g.description.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
            <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
              {lang === 'ta' ? 'அறிவு இடைவெளிகள் கண்டறிதல்' : 'Potential Knowledge Gaps Queue'}
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            {lang === 'ta'
              ? 'ஒப்பீட்டு பகுப்பாய்வில் கண்டறியப்பட்ட விடுபட்ட கூறுகள் மற்றும் செய்முறை படிகள்.'
              : 'Cross-source comparative gaps detected across all cultural domains, ranked by preservation urgency.'}
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t.actions.searchPlaceholder}
            className="w-full pl-9 pr-4 py-2 bg-white rounded-xl border border-slate-300 text-xs focus:outline-none focus:ring-1 focus:ring-[#6B1D2F]"
          />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center space-x-2">
        {['ALL', 'PENDING', 'VERIFIED', 'NEEDS_MORE_EVIDENCE', 'REJECTED'].map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-colors ${
              statusFilter === st
                ? 'bg-[#6B1D2F] text-white shadow-xs'
                : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
            }`}
          >
            {st.replace(/_/g, ' ').toLowerCase()}
          </button>
        ))}
      </div>

      {/* Split View: Gaps Table on Left, Evidence Inspector on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
          <div className="p-4 border-b border-slate-200 bg-slate-50 flex items-center justify-between text-xs font-bold text-slate-700">
            <span>Detected Items ({filteredGaps.length})</span>
            <span>Urgency Rank</span>
          </div>

          {loading ? (
            <div className="p-8 text-center text-xs text-slate-500">Loading gaps...</div>
          ) : filteredGaps.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500">No gaps found.</div>
          ) : (
            <div className="divide-y divide-slate-100 max-h-[680px] overflow-y-auto">
              {filteredGaps.map((g) => {
                const isSelected = selectedGap?.id === g.id;
                return (
                  <div
                    key={g.id}
                    onClick={() => setSelectedGap(g)}
                    className={`p-4 cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-amber-50/70 border-l-4 border-[#6B1D2F]'
                        : 'hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <span className="text-3xs uppercase tracking-wider font-extrabold text-slate-500">
                          {g.branch_name}
                        </span>
                        <h4 className="text-sm font-bold text-slate-900 mt-0.5">
                          {g.element_name}
                        </h4>
                        <p className="text-2xs text-slate-500 line-clamp-1 mt-0.5">
                          {g.details}
                        </p>
                      </div>

                      <div className="text-right shrink-0">
                        <span className="text-xs font-extrabold px-2 py-0.5 rounded bg-rose-100 text-rose-800">
                          {g.urgency_score}/100
                        </span>
                        <div className="text-3xs text-slate-400 mt-1 capitalize">
                          {g.verification_status}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Detail Pane */}
        <div className="lg:col-span-7">
          <EvidenceTrail
            gap={selectedGap}
            onVerify={handleVerify}
            onReject={handleReject}
            onRequestEvidence={handleRequestEvidence}
            lang={lang}
          />
        </div>
      </div>
    </div>
  );
}
