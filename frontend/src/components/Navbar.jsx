import React from 'react';
import { Globe, Shield, Sparkles, BookMarked, AlertCircle } from 'lucide-react';
import { translations } from '../i18n/translations';

export default function Navbar({ lang, setLang, isLiveMode, onReloadDemo }) {
  const t = translations[lang];

  return (
    <header className="bg-[#F8E7C9]/95 backdrop-blur-md border-b-2 border-[#064e3b]/20 sticky top-0 z-30 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Brand & Identity */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-lg bg-[#6B1D2F] flex items-center justify-center text-[#064e3b] shadow-sm border border-amber-500/20">
              <BookMarked className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-serif-title font-bold text-lg text-[#064e3b] font-extrabold tracking-wide font-serif tracking-tight">
                  {lang === 'ta' ? 'தமிழ் மறையும் அறிவு கண்டறிதல்' : 'Tamil Vanishing Knowledge Detector'}
                </span>
                <span className="hidden md:inline-flex items-center px-2 py-0.5 text-xs font-semibold rounded-full bg-amber-50 text-amber-800 border border-amber-200">
                  {t.eventBadge}
                </span>
              </div>
              <p className="text-xs text-[#064e3b] font-medium">
                {t.subTitle} &bull; <span className="italic">{lang === 'ta' ? 'அறிவு இழப்பு தடுப்பு கட்டமைப்பு' : 'Cultural Memory Engine'}</span>
              </p>
            </div>
          </div>

          {/* Center/Right Controls */}
          <div className="flex items-center space-x-3">
            {/* Live vs Demo Badge */}
            {isLiveMode ? (
              <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-300 shadow-2xs">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse mr-1.5"></span>
                {t.liveAnalysisBadge}
              </span>
            ) : (
              <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-300">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mr-1.5"></span>
                {t.demoBadge}
              </span>
            )}

            {/* Language Switcher */}
            <div className="flex items-center rounded-lg border border-slate-200 bg-slate-50 p-0.5 text-xs font-medium">
              <button
                onClick={() => setLang('en')}
                className={`px-2.5 py-1 rounded-md transition-colors ${
                  lang === 'en'
                    ? 'bg-white text-[#064e3b] font-extrabold tracking-wide font-serif shadow-xs font-semibold'
                    : 'text-[#064e3b] hover:text-[#064e3b] font-extrabold tracking-wide font-serif'
                }`}
              >
                English
              </button>
              <button
                onClick={() => setLang('ta')}
                className={`px-2.5 py-1 rounded-md transition-colors tamil-font ${
                  lang === 'ta'
                    ? 'bg-white text-[#064e3b] font-extrabold tracking-wide font-serif shadow-xs font-semibold'
                    : 'text-[#064e3b] hover:text-[#064e3b] font-extrabold tracking-wide font-serif'
                }`}
              >
                தமிழ்
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Philosophical banner */}
      <div className="bg-[#064e3b] text-white px-4 py-1.5 text-xs text-center font-medium border-t border-[#064e3b]/20 flex items-center justify-center space-x-2">
        <Sparkles className="w-3.5 h-3.5 text-[#064e3b] shrink-0" />
        <span className={lang === 'ta' ? 'tamil-font' : ''}>
          “{t.corePhilosophy}”
        </span>
      </div>
    </header>
  );
}
