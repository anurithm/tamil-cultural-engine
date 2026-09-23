import React from 'react';
import {
  Compass,
  FileText,
  ScanText,
  GitCompare,
  ShieldCheck,
  Archive,
  Music,
  Sprout,
  Waves,
  Layers,
  Hammer,
  Wheat,
  BookOpen,
  ArrowRight,
  Database,
  Sparkles,
  AlertTriangle
} from 'lucide-react';
import { translations } from '../i18n/translations';
import UrgencyGauge from '../components/UrgencyGauge';

// Map domain IDs to cultural Lucide icons
const DOMAIN_ICONS = {
  'folk-culture': Music,
  'traditional-plants': Sprout,
  'marine-coastal': Waves,
  'weaving-textiles': Layers,
  'traditional-crafts': Hammer,
  'agriculture-farming': Wheat,
  'tamil-literature': BookOpen
};

export default function Dashboard({
  dashboardData,
  loading,
  onSelectDomain,
  onSelectBranch,
  onLoadDemo,
  isReloadingDemo,
  lang = 'en'
}) {
  const t = translations[lang];

  if (loading) {
    return (
      <div className="p-8 space-y-6">
        <div className="h-28 bg-slate-200/60 rounded-2xl animate-pulse"></div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-24 bg-slate-200/50 rounded-xl animate-pulse"></div>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(7)].map((_, i) => (
            <div key={i} className="h-64 bg-slate-200/40 rounded-2xl animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-rose-500" />
        <h2 className="text-xl font-bold text-slate-900">Failed to load Dashboard Data</h2>
        <p className="text-sm text-slate-500 max-w-md">The backend API might not be running or is unreachable. Please ensure the backend server is running on port 8000.</p>
        <button onClick={() => window.location.reload()} className="px-4 py-2 bg-[#6B1D2F] text-white rounded-lg font-semibold text-sm">Retry</button>
      </div>
    );
  }

  const {
    total_traditions,
    total_sources,
    total_elements,
    total_gaps,
    total_pending,
    total_verified,
    traditions = []
  } = dashboardData;

  const statCards = [
    { title: t.dashboard.domainsCount, value: total_traditions, icon: Compass, color: 'text-amber-800', bg: 'bg-amber-50' },
    { title: t.dashboard.sourcesCount, value: total_sources, icon: FileText, color: 'text-blue-800', bg: 'bg-blue-50' },
    { title: t.dashboard.elementsCount, value: total_elements, icon: ScanText, color: 'text-indigo-800', bg: 'bg-indigo-50' },
    { title: t.dashboard.gapsCount, value: total_gaps, icon: GitCompare, color: 'text-rose-800', bg: 'bg-rose-50', alert: true },
    { title: t.dashboard.pendingCount, value: total_pending, icon: ShieldCheck, color: 'text-amber-800', bg: 'bg-amber-50' },
    { title: t.dashboard.verifiedCount, value: total_verified, icon: Archive, color: 'text-emerald-800', bg: 'bg-emerald-50' },
  ];

  return (
    <div className="p-6 sm:p-8 space-y-8 max-w-7xl mx-auto">
      {/* Hero Banner */}
      <div className="bg-gradient-to-r from-[#6B1D2F] via-[#7D2439] to-[#8C2C42] rounded-2xl p-6 sm:p-8 text-white shadow-md relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/10 text-amber-200 text-xs font-semibold backdrop-blur-xs border border-white/10">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>{t.eventBadge}</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-serif-title text-amber-50">
            {t.dashboard.title}
          </h1>

          <p className="text-sm text-amber-100/90 leading-relaxed font-light">
            {t.dashboard.overview}
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <button
              onClick={onLoadDemo}
              disabled={isReloadingDemo}
              className="px-4 py-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold rounded-lg text-xs shadow-sm transition-all flex items-center space-x-2"
            >
              <Database className="w-4 h-4" />
              <span>{isReloadingDemo ? t.dashboard.loadingDemo : t.dashboard.loadDemoBtn}</span>
            </button>
            <span className="text-2xs text-amber-200/80 italic">
              *{t.demoDisclaimer}
            </span>
          </div>
        </div>

        {/* Decorative background watermark */}
        <div className="absolute right-4 -bottom-8 opacity-10 pointer-events-none select-none">
          <Compass className="w-64 h-64 text-white" />
        </div>
      </div>

      {/* 6 Top Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
        {statCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div
              key={idx}
              className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition-all"
            >
              <div className="flex items-center justify-between">
                <span className={`p-2 rounded-lg ${card.bg} ${card.color}`}>
                  <Icon className="w-4 h-4" />
                </span>
                {card.alert && (
                  <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                )}
              </div>
              <div className="mt-3">
                <span className="text-2xl font-extrabold text-slate-900 font-serif-title">
                  {card.value}
                </span>
                <p className="text-xs font-medium text-slate-500 mt-0.5 line-clamp-1">
                  {card.title}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* 7 Cultural Domains Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-900 font-serif-title">
              {lang === 'ta' ? '7 கலாச்சார பாரம்பரிய களங்கள்' : '7 Cultural Heritage Domains'}
            </h2>
            <p className="text-xs text-slate-500">
              {lang === 'ta'
                ? 'ஒவ்வொரு களமும் பல கிளைகளையும் ஆவணப்படுத்தப்பட்ட ஒப்பீட்டுத் தரவையும் கொண்டுள்ளது.'
                : 'Click any domain to explore branches, uploaded real sources, and detected potential gaps.'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {traditions.map((trad) => {
            const Icon = DOMAIN_ICONS[trad.id] || Compass;
            return (
              <div
                key={trad.id}
                className="heritage-card bg-white rounded-2xl border border-slate-200 p-6 flex flex-col justify-between shadow-2xs relative group"
              >
                <div>
                  {/* Card Header */}
                  <div className="flex items-start justify-between">
                    <div className="w-12 h-12 rounded-xl bg-amber-50 text-[#6B1D2F] border border-amber-200 flex items-center justify-center shadow-xs">
                      <Icon className="w-6 h-6" />
                    </div>
                    <span
                      className={`px-2 py-0.5 rounded text-2xs font-extrabold tracking-wider ${
                        trad.urgency_level === 'CRITICAL'
                          ? 'bg-rose-100 text-rose-800'
                          : trad.urgency_level === 'HIGH'
                          ? 'bg-amber-100 text-amber-800'
                          : 'bg-emerald-100 text-emerald-800'
                      }`}
                    >
                      {trad.urgency_level} URGENCY
                    </span>
                  </div>

                  {/* Title & Tamil Name */}
                  <div className="mt-4">
                    <h3 className="text-lg font-bold text-slate-900 font-serif-title group-hover:text-[#6B1D2F] transition-colors">
                      {trad.name}
                    </h3>
                    <p className="text-xs font-semibold text-amber-900 tamil-font mt-0.5">
                      {trad.tamil_name}
                    </p>
                  </div>

                  {/* Description */}
                  <p className="text-xs text-slate-500 mt-2 leading-relaxed line-clamp-2">
                    {lang === 'ta' ? trad.tamil_description : trad.description}
                  </p>

                  {/* Domain Metrics */}
                  <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-slate-50 p-2 rounded-lg">
                      <span className="font-bold text-slate-900">{trad.branch_count}</span>
                      <p className="text-3xs text-slate-500 uppercase mt-0.5">Branches</p>
                    </div>
                    <div className="bg-slate-50 p-2 rounded-lg">
                      <span className="font-bold text-slate-900">{trad.source_count}</span>
                      <p className="text-3xs text-slate-500 uppercase mt-0.5">Sources</p>
                    </div>
                    <div className="bg-rose-50/70 p-2 rounded-lg border border-rose-100">
                      <span className="font-bold text-rose-800">{trad.gap_count}</span>
                      <p className="text-3xs text-rose-600 uppercase mt-0.5">Gaps</p>
                    </div>
                  </div>

                  {/* Urgency Meter */}
                  <div className="mt-3">
                    <UrgencyGauge
                      score={Math.round(trad.urgency_score)}
                      compact={true}
                      lang={lang}
                    />
                  </div>
                </div>

                {/* Card Action Button */}
                <div className="mt-5 pt-3 border-t border-slate-100">
                  <button
                    onClick={() => onSelectDomain(trad.id)}
                    className="w-full py-2.5 px-4 bg-slate-900 hover:bg-[#6B1D2F] text-white rounded-xl text-xs font-semibold transition-all flex items-center justify-center space-x-2 group-hover:shadow-xs"
                  >
                    <span>{t.dashboard.exploreBtn}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
