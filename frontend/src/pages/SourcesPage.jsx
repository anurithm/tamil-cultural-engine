import React, { useState, useEffect } from 'react';
import { FileText, Search, ExternalLink, BookOpen, User, Calendar, ShieldAlert } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';

export default function SourcesPage({ onSelectBranch, lang = 'en' }) {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all'); // 'all', 'live', 'demo'
  const [searchQuery, setSearchQuery] = useState('');
  const t = translations[lang];

  useEffect(() => {
    let mounted = true;
    api.getSources()
      .then((data) => {
        if (mounted) {
          setSources(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error('Failed to load sources:', err);
        if (mounted) setLoading(false);
      });

    return () => { mounted = false; };
  }, []);

  const filteredSources = sources.filter((s) => {
    if (filterType === 'live' && !s.is_live) return false;
    if (filterType === 'demo' && s.is_live) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        s.title.toLowerCase().includes(q) ||
        s.author.toLowerCase().includes(q) ||
        s.source_type.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
            {lang === 'ta' ? 'மூலப்பதிவுகள் நூலகம்' : 'Documentary Sources Archive'}
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            {lang === 'ta'
              ? 'நேரடி பயனர் பதிவேற்றங்கள் மற்றும் வரலாற்று மாதிரி நூல்களின் முழு தொகுப்பு.'
              : 'Surveyed archival manuscripts, oral interview transcripts, and live user-uploaded sources.'}
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
        <button
          onClick={() => setFilterType('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            filterType === 'all'
              ? 'bg-[#6B1D2F] text-white shadow-xs'
              : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
          }`}
        >
          All Sources ({sources.length})
        </button>
        <button
          onClick={() => setFilterType('live')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            filterType === 'live'
              ? 'bg-emerald-600 text-white shadow-xs'
              : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
          }`}
        >
          {t.liveBadge} ({sources.filter((s) => s.is_live).length})
        </button>
        <button
          onClick={() => setFilterType('demo')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            filterType === 'demo'
              ? 'bg-amber-600 text-white shadow-xs'
              : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
          }`}
        >
          Demo Sample Records ({sources.filter((s) => !s.is_live).length})
        </button>
      </div>

      {/* Grid of Sources */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-44 bg-slate-200/50 rounded-xl animate-pulse"></div>
          ))}
        </div>
      ) : filteredSources.length === 0 ? (
        <div className="bg-white rounded-xl border border-slate-200 p-8 text-center text-sm text-slate-500">
          No sources found matching your criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSources.map((src) => (
            <div
              key={src.id}
              className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs hover:border-slate-300 transition-all flex flex-col justify-between space-y-3"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <span
                    className={`px-2 py-0.5 rounded text-2xs font-extrabold uppercase tracking-wider ${
                      src.is_live
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                        : 'bg-amber-100 text-amber-800 border border-amber-300'
                    }`}
                  >
                    {src.is_live ? t.liveBadge : 'SAMPLE RECORD'}
                  </span>
                  <span className="text-3xs text-slate-400 font-mono">
                    {src.total_pages || 1} pgs
                  </span>
                </div>

                <h3 className="mt-2 text-sm font-bold text-slate-900 line-clamp-2">
                  {src.title}
                </h3>

                <div className="mt-2 space-y-1 text-2xs text-slate-500">
                  <div className="flex items-center space-x-1.5">
                    <User className="w-3.5 h-3.5 text-slate-400" />
                    <span>{src.author || 'Unknown'}</span>
                  </div>
                  <div className="flex items-center space-x-1.5">
                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                    <span>{src.year} &bull; {src.source_type}</span>
                  </div>
                  {src.publisher && (
                    <div className="flex items-center space-x-1.5">
                      <BookOpen className="w-3.5 h-3.5 text-slate-400" />
                      <span className="truncate">{src.publisher}</span>
                    </div>
                  )}
                </div>

                {src.description && (
                  <p className="mt-2 text-2xs text-slate-600 line-clamp-2 italic">
                    "{src.description}"
                  </p>
                )}
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-2xs text-slate-400">
                  Lang: {src.language || 'Tamil / English'}
                </span>
                <button
                  onClick={() => onSelectBranch(src.branch_id)}
                  className="text-xs font-semibold text-[#6B1D2F] hover:underline"
                >
                  Analyze Branch &rarr;
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
