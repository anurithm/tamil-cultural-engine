import React, { useState, useEffect } from 'react';
import { BookOpen, Search, Filter, BookMarked } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';

export default function GlossaryPage({ lang = 'en' }) {
  const [terms, setTerms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDomain, setSelectedDomain] = useState('ALL');
  const t = translations[lang];

  useEffect(() => {
    let mounted = true;
    api.getGlossary()
      .then((data) => {
        if (mounted) {
          setTerms(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error('Failed to load glossary:', err);
        if (mounted) setLoading(false);
      });

    return () => { mounted = false; };
  }, []);

  const domainsList = Array.from(new Set(terms.map((t) => t.domain_name).filter(Boolean)));

  const filteredTerms = terms.filter((item) => {
    if (selectedDomain !== 'ALL' && item.domain_name !== selectedDomain) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        item.tamil_term.toLowerCase().includes(q) ||
        item.transliteration.toLowerCase().includes(q) ||
        item.english_meaning.toLowerCase().includes(q) ||
        item.branch_name.toLowerCase().includes(q)
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
            <div className="p-2 rounded-lg bg-amber-50 text-amber-800 border border-amber-200">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
                {lang === 'ta' ? 'பாரம்பரிய கலைச்சொற்களஞ்சியம்' : 'Tamil Heritage Cultural Glossary'}
              </h1>
              <p className="text-xs text-slate-500">
                {lang === 'ta'
                  ? '7 மரபு களங்களிலும் ஆய்வு செய்யப்பட்ட தமிழ் கலைச்சொற்கள், ஒலிபெயர்ப்பு மற்றும் விளக்கங்கள்.'
                  : 'Bilingual terminology, transliterations, and meanings extracted from archival texts and live sources.'}
              </p>
            </div>
          </div>
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

      {/* Domain Filters */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-1">
        <button
          onClick={() => setSelectedDomain('ALL')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
            selectedDomain === 'ALL'
              ? 'bg-[#6B1D2F] text-white shadow-xs'
              : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
          }`}
        >
          All Domains ({terms.length})
        </button>
        {domainsList.map((d) => (
          <button
            key={d}
            onClick={() => setSelectedDomain(d)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
              selectedDomain === d
                ? 'bg-[#6B1D2F] text-white shadow-xs'
                : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
            }`}
          >
            {d}
          </button>
        ))}
      </div>

      {/* Glossary Table */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-100/70 border-b border-slate-200 text-xs font-semibold text-slate-600 uppercase tracking-wider">
              <tr>
                <th className="px-5 py-3.5 min-w-[160px]">Tamil Term</th>
                <th className="px-4 py-3.5 min-w-[140px]">Transliteration</th>
                <th className="px-5 py-3.5 min-w-[280px]">Meaning / Definition</th>
                <th className="px-4 py-3.5 min-w-[160px]">Domain & Branch</th>
                <th className="px-4 py-3.5 min-w-[140px]">Source</th>
                <th className="px-3 py-3.5 text-center min-w-[100px]">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {loading ? (
                <tr>
                  <td colSpan="6" className="p-8 text-center text-slate-400">Loading glossary terms...</td>
                </tr>
              ) : filteredTerms.length === 0 ? (
                <tr>
                  <td colSpan="6" className="p-8 text-center text-slate-400">No terms match your search.</td>
                </tr>
              ) : (
                filteredTerms.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-3.5 font-bold text-amber-950 tamil-font text-base">
                      {t.tamil_term}
                    </td>
                    <td className="px-4 py-3.5 font-semibold text-slate-800">
                      {t.transliteration}
                    </td>
                    <td className="px-5 py-3.5 text-slate-700 leading-relaxed">
                      {t.english_meaning}
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="font-semibold text-slate-900">{t.domain_name}</div>
                      <div className="text-3xs text-slate-500">{t.branch_name}</div>
                    </td>
                    <td className="px-4 py-3.5 text-slate-500 text-2xs truncate max-w-[160px]">
                      {t.source_title}
                    </td>
                    <td className="px-3 py-3.5 text-center">
                      <span
                        className={`px-2 py-0.5 rounded text-3xs font-extrabold uppercase tracking-wider ${
                          t.is_live
                            ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                            : 'bg-amber-100 text-amber-800 border border-amber-300'
                        }`}
                      >
                        {t.is_live ? 'LIVE' : 'DEMO'}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
