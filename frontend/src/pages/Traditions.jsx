import React, { useState } from 'react';
import { Compass, Search, ArrowRight, ShieldCheck, GitCompare, FileText, Sparkles } from 'lucide-react';
import { translations } from '../i18n/translations';
import UrgencyGauge from '../components/UrgencyGauge';

export default function Traditions({
  traditions = [],
  selectedDomainId,
  onSelectDomain,
  onSelectBranch,
  lang = 'en'
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeDomainFilter, setActiveDomainFilter] = useState(selectedDomainId || 'all');
  const t = translations[lang];

  // Filter traditions & branches
  const filteredTraditions = traditions.filter((tr) => {
    if (activeDomainFilter !== 'all' && tr.id !== activeDomainFilter) return false;
    return true;
  });

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
            {lang === 'ta' ? 'பாரம்பரிய மரபுகள் & களங்கள்' : 'Cultural Traditions & Branches'}
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            {lang === 'ta'
              ? 'அனைத்து 7 களங்களையும் அவற்றின் 38 தனித்துவக் கிளைகளையும் ஆராயுங்கள்.'
              : 'Explore the full taxonomy of 7 domains and 38 branches with live source tracking.'}
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

      {/* Domain Filter Pills */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-2">
        <button
          onClick={() => setActiveDomainFilter('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
            activeDomainFilter === 'all'
              ? 'bg-[#6B1D2F] text-white shadow-xs'
              : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
          }`}
        >
          {lang === 'ta' ? 'அனைத்து களங்களும் (7)' : 'All Domains (7)'}
        </button>
        {traditions.map((trad) => (
          <button
            key={trad.id}
            onClick={() => setActiveDomainFilter(trad.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
              activeDomainFilter === trad.id
                ? 'bg-[#6B1D2F] text-white shadow-xs'
                : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
            }`}
          >
            <span>{trad.name}</span>
          </button>
        ))}
      </div>

      {/* Domains & Branches List */}
      <div className="space-y-8">
        {filteredTraditions.map((trad) => {
          const matchingBranches = trad.branches.filter((b) => {
            if (!searchQuery) return true;
            const q = searchQuery.toLowerCase();
            return (
              b.name.toLowerCase().includes(q) ||
              b.tamil_name.toLowerCase().includes(q) ||
              b.description.toLowerCase().includes(q)
            );
          });

          if (matchingBranches.length === 0) return null;

          return (
            <div
              key={trad.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-5"
            >
              {/* Domain Header */}
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="w-2 h-2 rounded-full bg-[#6B1D2F]"></span>
                    <h2 className="text-xl font-bold text-slate-900 font-serif-title">
                      {trad.name}
                    </h2>
                  </div>
                  <p className="text-xs text-amber-900 tamil-font font-medium mt-0.5">
                    {trad.tamil_name}
                  </p>
                  <p className="text-xs text-slate-500 mt-1 max-w-3xl">
                    {lang === 'ta' ? trad.tamil_description : trad.description}
                  </p>
                </div>

                <div className="flex items-center space-x-4 text-xs font-semibold">
                  <span className="text-slate-600">
                    {trad.branches.length} Branches
                  </span>
                  <span className="text-slate-600">
                    {trad.source_count} Sources
                  </span>
                  <span className="text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                    {trad.gap_count} Gaps
                  </span>
                </div>
              </div>

              {/* Branches Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {matchingBranches.map((branch) => (
                  <div
                    key={branch.id}
                    onClick={() => onSelectBranch(branch.id)}
                    className="p-4 rounded-xl border border-slate-200 hover:border-amber-400 bg-slate-50/50 hover:bg-white cursor-pointer transition-all hover:shadow-xs group flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-start justify-between">
                        <h4 className="font-bold text-slate-900 text-sm group-hover:text-[#6B1D2F] transition-colors">
                          {branch.name}
                        </h4>
                        <span
                          className={`text-3xs font-extrabold px-1.5 py-0.5 rounded ${
                            branch.urgency_level === 'CRITICAL'
                              ? 'bg-rose-100 text-rose-800'
                              : branch.urgency_level === 'HIGH'
                              ? 'bg-amber-100 text-amber-800'
                              : 'bg-emerald-100 text-emerald-800'
                          }`}
                        >
                          {branch.urgency_level}
                        </span>
                      </div>

                      <div className="text-xs text-amber-900/80 tamil-font font-medium mt-0.5">
                        {branch.tamil_name}
                      </div>

                      <p className="text-xs text-slate-500 mt-2 line-clamp-2 leading-relaxed">
                        {lang === 'ta' ? branch.tamil_description : branch.description}
                      </p>
                    </div>

                    <div className="mt-4 pt-3 border-t border-slate-200/60 flex items-center justify-between text-2xs text-slate-600 font-medium">
                      <div className="flex items-center space-x-2">
                        <span>{branch.source_count} Sources</span>
                        <span>&bull;</span>
                        <span className="text-rose-700 font-bold">{branch.gap_count} Gaps</span>
                      </div>
                      <span className="text-[#6B1D2F] font-bold group-hover:translate-x-1 transition-transform flex items-center space-x-1">
                        <span>Explore</span>
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
