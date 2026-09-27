import React from 'react';
export default function UrgencyGauge({ score, compact = false, lang = 'en' }) {
  const radius = compact ? 18 : 28;
  const stroke = compact ? 4 : 6;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let colorClass = 'text-emerald-500';
  if (score >= 80) colorClass = 'text-rose-500';
  else if (score >= 50) colorClass = 'text-amber-500';

  return (
    <div className={`flex items-center ${compact ? 'space-x-3' : 'space-x-4'}`}>
      <div className="relative inline-flex items-center justify-center">
        <svg height={radius * 2} width={radius * 2} className="transform -rotate-90">
          <circle stroke="currentColor" fill="transparent" strokeWidth={stroke} r={normalizedRadius} cx={radius} cy={radius} className="opacity-20" />
          <circle stroke="currentColor" fill="transparent" strokeWidth={stroke} strokeDasharray={circumference + ' ' + circumference} style={{ strokeDashoffset, transition: 'stroke-dashoffset 1s ease-in-out' }} r={normalizedRadius} cx={radius} cy={radius} className={`${colorClass}`} strokeLinecap="round" />
        </svg>
        <div className={`absolute font-extrabold ${compact ? 'text-xs' : 'text-base'}`}>{Math.round(score)}</div>
      </div>
      {!compact && (
        <div className="flex flex-col">
          <span className="text-xs font-bold uppercase tracking-wider">{lang === 'ta' ? 'அவசர நிலை' : 'Urgency Score'}</span>
          <span className="text-[10px] opacity-70">Based on evidence gaps</span>
        </div>
      )}
    </div>
  );
}
