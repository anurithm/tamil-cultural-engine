import React from 'react';
import {
  LayoutDashboard,
  Compass,
  FileText,
  ScanText,
  GitCompare,
  Quote,
  ShieldCheck,
  Archive,
  Network,
  BookOpen
} from 'lucide-react';
import { translations } from '../i18n/translations';

export default function Sidebar({ activeTab, setActiveTab, lang, stats }) {
  const t = translations[lang];

  const menuItems = [
    { id: 'dashboard', label: t.nav.dashboard, icon: LayoutDashboard },
    { id: 'traditions', label: t.nav.traditions, icon: Compass, count: stats?.total_traditions },
    { id: 'sources', label: t.nav.sources, icon: FileText, count: stats?.total_sources },
    { id: 'knowledge', label: t.nav.knowledge, icon: ScanText, count: stats?.total_elements },
    { id: 'gaps', label: t.nav.gaps, icon: GitCompare, count: stats?.total_gaps, alert: true },
    { id: 'evidence', label: t.nav.evidence, icon: Quote },
    { id: 'verification', label: t.nav.verification, icon: ShieldCheck, count: stats?.total_pending, badgeColor: 'bg-amber-100 text-amber-800' },
    { id: 'preserved', label: t.nav.preserved, icon: Archive, count: stats?.total_verified, badgeColor: 'bg-emerald-100 text-emerald-800' },
    { id: 'graph', label: t.nav.graph, icon: Network },
    { id: 'glossary', label: t.nav.glossary, icon: BookOpen }
  ];

  return (
    <aside className="w-full md:w-64 bg-white border-b md:border-r border-slate-200 flex md:flex-col shrink-0 min-h-auto md:min-h-[calc(100vh-5.5rem)] overflow-x-auto">
      <div className="p-2 md:p-4 flex md:flex-col space-x-2 md:space-x-0 md:space-y-1">
        <div className="px-3 py-2 text-2xs font-bold uppercase tracking-wider text-slate-400">
          {lang === 'ta' ? 'முதன்மை வழிசெலுத்தல்' : 'Research Modules'}
        </div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-[#6B1D2F] text-white shadow-xs font-semibold'
                  : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon
                  className={`w-4 h-4 ${
                    isActive ? 'text-amber-300' : 'text-slate-400'
                  }`}
                />
                <span className={lang === 'ta' ? 'tamil-font' : ''}>
                  {item.label}
                </span>
              </div>
              {item.count !== undefined && item.count > 0 && (
                <span
                  className={`px-1.5 py-0.5 text-xs rounded-md font-semibold ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : item.badgeColor || (item.alert ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-600')
                  }`}
                >
                  {item.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Subtle research disclaimer card */}
      <div className="mt-auto p-4 border-t border-slate-100 bg-slate-50/70 m-3 rounded-lg text-xs text-slate-500 space-y-1">
        <p className="font-semibold text-slate-700 flex items-center space-x-1">
          <span>AUREX’26 Engine</span>
        </p>
        <p className="text-2xs text-slate-500 leading-relaxed">
          {lang === 'ta'
            ? 'அறிவு இழப்பு மதிப்பீடு மாதிரி மட்டுமே; வரலாற்று ஆய்வுக்கும் சரிபார்ப்பிற்கும் உட்பட்டது.'
            : 'AI-assisted gap comparison for preservation prioritization.'}
        </p>
      </div>
    </aside>
  );
}
