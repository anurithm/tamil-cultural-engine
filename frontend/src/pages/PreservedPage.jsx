import React, { useState, useEffect } from 'react';
import { Archive, Search, ShieldCheck, CheckCircle2, Calendar, FileText, Download } from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';

export default function PreservedPage({ lang = 'en' }) {
  const [preservedList, setPreservedList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const t = translations[lang];

  useEffect(() => {
    let mounted = true;
    api.getPreserved()
      .then((data) => {
        if (mounted) {
          setPreservedList(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error('Failed to load preserved knowledge:', err);
        if (mounted) setLoading(false);
      });

    return () => { mounted = false; };
  }, []);

  const filtered = preservedList.filter((item) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      item.title.toLowerCase().includes(q) ||
      item.branch_name.toLowerCase().includes(q) ||
      item.reconstructed_text.toLowerCase().includes(q)
    );
  });

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-5">
        <div>
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200">
              <Archive className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
                {lang === 'ta' ? 'பாதுகாக்கப்பட்ட கலாச்சார அறிவு' : 'Preserved Cultural Knowledge Repository'}
              </h1>
              <p className="text-xs text-slate-500">
                {lang === 'ta'
                  ? 'மனித ஆய்வாளர்களால் சரிபார்க்கப்பட்ட நம்பகமான பாரம்பரிய அறிவு களஞ்சியம்.'
                  : 'Immutable digital archive of cultural knowledge verified by cultural historians and practitioners.'}
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

      {loading ? (
        <div className="p-12 text-center text-xs text-slate-500">Loading preserved records...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <ShieldCheck className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-700">No Preserved Records Yet</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Gaps must be reviewed and verified by a human cultural researcher in the Verification Portal before entering this preserved repository.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-2xl border border-emerald-200/80 p-6 shadow-xs flex flex-col justify-between space-y-4 relative overflow-hidden"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold border border-emerald-300 flex items-center space-x-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>VERIFIED CULTURAL KNOWLEDGE</span>
                  </span>
                  <span className="text-2xs text-slate-400 flex items-center space-x-1">
                    <Calendar className="w-3 h-3" />
                    <span>{new Date(item.verification_date).toLocaleDateString()}</span>
                  </span>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-slate-900 font-serif-title">
                    {item.title}
                  </h3>
                  {item.tamil_title && (
                    <p className="text-xs font-semibold text-amber-900 tamil-font mt-0.5">
                      {item.tamil_title}
                    </p>
                  )}
                  <p className="text-2xs text-slate-500 mt-1 uppercase tracking-wider font-semibold">
                    {item.tradition_name} &bull; {item.branch_name}
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-50 text-xs text-slate-800 leading-relaxed border border-slate-200/60 italic">
                  "{item.reconstructed_text}"
                </div>

                {item.verifier_notes && (
                  <div className="text-2xs text-slate-500 space-y-0.5">
                    <strong className="text-slate-700">Verifier Annotation:</strong>
                    <p className="italic text-slate-600">"{item.verifier_notes}"</p>
                  </div>
                )}
              </div>

              <div className="pt-3 border-t border-slate-100 flex justify-between items-center text-xs">
                <span className="text-2xs text-slate-400 capitalize">
                  Category: {item.category.replace('_', ' ')}
                </span>
                <span className="text-emerald-700 font-bold text-2xs uppercase tracking-wider">
                  Authenticated Archival Entry
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
