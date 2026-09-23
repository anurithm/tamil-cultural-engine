import React, { useState, useEffect } from 'react';
import {
  Compass,
  FileText,
  Upload,
  Play,
  Network,
  AlertTriangle,
  ShieldCheck,
  CheckCircle2,
  BookOpen,
  ArrowLeft,
  Sparkles,
  Info
} from 'lucide-react';
import { api } from '../services/api';
import { translations } from '../i18n/translations';
import ComparisonTable from '../components/ComparisonTable';
import EvidenceTrail from '../components/EvidenceTrail';
import UrgencyGauge from '../components/UrgencyGauge';
import AddSourceModal from '../components/AddSourceModal';
import AnalysisProgress from '../components/AnalysisProgress';
import KnowledgeGraphView from '../components/KnowledgeGraphView';

export default function BranchDetail({
  branchId = 'karagattam',
  onBack,
  onOpenVerification,
  lang = 'en'
}) {
  const [branchData, setBranchData] = useState(null);
  const [matrixData, setMatrixData] = useState(null);
  const [gaps, setGaps] = useState([]);
  const [selectedGap, setSelectedGap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddSource, setShowAddSource] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeView, setActiveView] = useState('comparison'); // 'comparison', 'evidence', 'graph'
  const [updateNotification, setUpdateNotification] = useState(null);

  const t = translations[lang];

  const loadAllBranchData = async () => {
    try {
      setLoading(true);
      const [bRes, cRes, gRes] = await Promise.all([
        api.getBranch(branchId),
        api.getBranchComparison(branchId),
        api.getGaps({ branch_id: branchId })
      ]);
      setBranchData(bRes);
      setMatrixData(cRes);
      setGaps(gRes);
      if (gRes.length > 0) {
        setSelectedGap(gRes[0]);
      }
    } catch (err) {
      console.error('Failed to load branch details:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllBranchData();
  }, [branchId]);

  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      const res = await api.analyzeBranch(branchId);
      // Reload updated comparison and gaps
      await loadAllBranchData();
      setUpdateNotification(
        lang === 'ta'
          ? 'கலாச்சார ஒப்பீட்டு பகுப்பாய்வு வெற்றிகரமாக புதுப்பிக்கப்பட்டது.'
          : 'Cultural comparison analysis completed and knowledge base updated.'
      );
      setTimeout(() => setUpdateNotification(null), 4000);
    } catch (err) {
      alert(`Analysis error: ${err.message}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleVerifyGap = async (gapId) => {
    try {
      await api.verifyGap(gapId, 'Approved in branch inspection view.');
      await loadAllBranchData();
      setUpdateNotification(
        lang === 'ta'
          ? 'அறிவு கூறு சரிபார்க்கப்பட்டு பாதுகாக்கப்பட்ட அறிவில் சேர்க்கப்பட்டது.'
          : 'Knowledge element verified and added to Preserved Cultural Knowledge.'
      );
      setTimeout(() => setUpdateNotification(null), 4000);
    } catch (err) {
      alert(`Verification error: ${err.message}`);
    }
  };

  const handleRejectGap = async (gapId) => {
    try {
      await api.rejectGap(gapId, 'Rejected during branch inspection.');
      await loadAllBranchData();
    } catch (err) {
      alert(`Rejection error: ${err.message}`);
    }
  };

  const handleRequestEvidence = async (gapId) => {
    try {
      await api.requestEvidenceGap(gapId, 'Requested community archival evidence.');
      await loadAllBranchData();
    } catch (err) {
      alert(`Error requesting evidence: ${err.message}`);
    }
  };

  if (loading || !branchData) {
    return (
      <div className="p-8 space-y-6 max-w-7xl mx-auto">
        <div className="h-32 bg-slate-200/60 rounded-2xl animate-pulse"></div>
        <div className="h-96 bg-slate-200/40 rounded-2xl animate-pulse"></div>
      </div>
    );
  }

  // Check if there is any unmentioned missing step
  const missingSteps = matrixData?.rows?.filter((r) => r.is_missing_step) || [];

  return (
    <div className="p-6 sm:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Back button */}
      <button
        onClick={onBack}
        className="inline-flex items-center space-x-1.5 text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        <span>{lang === 'ta' ? 'பாரம்பரிய மரபுகளுக்கு திரும்பு' : 'Back to Traditions'}</span>
      </button>

      {/* Dynamic Update Notification */}
      {updateNotification && (
        <div className="p-3 bg-emerald-50 border border-emerald-300 text-emerald-900 rounded-xl text-xs font-semibold flex items-center space-x-2 shadow-xs animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{updateNotification}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-xs text-slate-500 font-medium">
              <span>{branchData.tradition_name}</span>
              <span>&bull;</span>
              <span className="text-amber-900 tamil-font font-semibold">
                {branchData.tradition_tamil_name}
              </span>
              {branchData.is_live && (
                <span className="px-2 py-0.5 rounded text-2xs font-extrabold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  {t.liveBadge}
                </span>
              )}
            </div>

            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 font-serif-title mt-1">
              {branchData.name}
            </h1>
            <p className="text-sm font-semibold text-amber-900 tamil-font mt-0.5">
              {branchData.tamil_name}
            </p>

            <p className="text-xs text-slate-600 mt-2 max-w-3xl leading-relaxed">
              {lang === 'ta' ? branchData.tamil_description : branchData.description}
            </p>
          </div>

          {/* Actions: Add Live Source & Run Analysis */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setShowAddSource(true)}
              className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-bold rounded-xl text-xs transition-colors flex items-center space-x-1.5 shadow-2xs"
            >
              <Upload className="w-3.5 h-3.5 text-emerald-600" />
              <span>{t.actions.addLiveSource}</span>
            </button>

            <button
              onClick={handleRunAnalysis}
              disabled={isAnalyzing}
              className="px-4 py-2 bg-[#6B1D2F] hover:bg-[#86461b] text-white font-bold rounded-xl text-xs transition-colors flex items-center space-x-1.5 shadow-xs"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{isAnalyzing ? t.actions.analyzing : t.actions.runAnalysis}</span>
            </button>
          </div>
        </div>

        {/* Sources Summary Bar */}
        <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-4 text-xs">
          <div className="flex items-center space-x-4 text-slate-600">
            <span className="flex items-center space-x-1.5">
              <FileText className="w-4 h-4 text-slate-400" />
              <span><strong>{branchData.sources_count}</strong> Sources Surveyed</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <BookOpen className="w-4 h-4 text-slate-400" />
              <span><strong>{branchData.knowledge_count}</strong> Knowledge Elements</span>
            </span>
            <span className="flex items-center space-x-1.5 text-rose-700 font-semibold">
              <AlertTriangle className="w-4 h-4 text-rose-500" />
              <span><strong>{branchData.gaps_count}</strong> Potential Gaps</span>
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <UrgencyGauge
              score={Math.round(branchData.urgency_score)}
              level={branchData.urgency_level}
              compact={true}
              lang={lang}
            />
          </div>
        </div>
      </div>

      {/* Potentially Unmentioned Step Alert Banner */}
      {missingSteps.length > 0 && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-300 text-amber-950 space-y-2">
          <div className="flex items-center space-x-2 font-bold text-xs uppercase tracking-wider text-amber-900">
            <AlertTriangle className="w-4 h-4 text-amber-700" />
            <span>{t.comparison.unmentionedStepAlert}</span>
          </div>
          {missingSteps.map((ms, i) => (
            <div key={i} className="text-xs bg-white/80 p-2.5 rounded-lg border border-amber-200">
              <strong className="text-slate-900">
                Step {ms.step_order || 'N'}: {ms.element_name}
              </strong>
              <p className="text-slate-600 mt-0.5">
                {ms.explanation}
              </p>
            </div>
          ))}
          <p className="text-3xs text-amber-800/80 italic">
            *{t.comparison.cautiousNote}
          </p>
        </div>
      )}

      {/* Navigation Tabs (Comparison Matrix, Evidence Trail, Knowledge Graph) */}
      <div className="flex items-center justify-between border-b border-slate-200">
        <div className="flex space-x-4">
          <button
            onClick={() => setActiveView('comparison')}
            className={`pb-3 text-xs font-bold transition-colors border-b-2 flex items-center space-x-1.5 ${
              activeView === 'comparison'
                ? 'border-[#6B1D2F] text-[#6B1D2F]'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <span>Comparison Matrix</span>
            <span className="px-1.5 py-0.2 rounded bg-slate-100 text-slate-600 text-2xs">
              {matrixData?.rows?.length || 0}
            </span>
          </button>

          <button
            onClick={() => setActiveView('evidence')}
            className={`pb-3 text-xs font-bold transition-colors border-b-2 flex items-center space-x-1.5 ${
              activeView === 'evidence'
                ? 'border-[#6B1D2F] text-[#6B1D2F]'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <span>Evidence Trail & Reconstruction</span>
            <span className="px-1.5 py-0.2 rounded bg-rose-100 text-rose-800 text-2xs">
              {gaps.length}
            </span>
          </button>

          <button
            onClick={() => setActiveView('graph')}
            className={`pb-3 text-xs font-bold transition-colors border-b-2 flex items-center space-x-1.5 ${
              activeView === 'graph'
                ? 'border-[#6B1D2F] text-[#6B1D2F]'
                : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            <Network className="w-3.5 h-3.5" />
            <span>Knowledge Graph</span>
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      {activeView === 'comparison' && (
        <div className="space-y-6">
          <ComparisonTable
            matrixData={matrixData}
            onSelectGap={(gapId) => {
              const target = gaps.find((g) => g.id === gapId);
              if (target) {
                setSelectedGap(target);
                setActiveView('evidence');
              }
            }}
            lang={lang}
          />
        </div>
      )}

      {activeView === 'evidence' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Gaps List on Left */}
          <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-3 h-fit">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Potential Gaps Detected ({gaps.length})
            </h4>
            <div className="space-y-2">
              {gaps.map((g) => {
                const isSelected = selectedGap?.id === g.id;
                return (
                  <button
                    key={g.id}
                    onClick={() => setSelectedGap(g)}
                    className={`w-full text-left p-3 rounded-lg border text-xs transition-all ${
                      isSelected
                        ? 'bg-amber-50/80 border-amber-400 shadow-2xs font-semibold'
                        : 'bg-slate-50/60 border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-slate-900 truncate max-w-[170px]">
                        {g.element_name}
                      </span>
                      <span className="text-3xs font-extrabold px-1.5 py-0.5 rounded bg-rose-100 text-rose-800">
                        {g.urgency_score}/100
                      </span>
                    </div>
                    <div className="text-3xs text-slate-500 mt-1 capitalize">
                      {g.gap_type.replace('_', ' ')} &bull; {g.verification_status}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Evidence Inspector on Right */}
          <div className="lg:col-span-2">
            <EvidenceTrail
              gap={selectedGap}
              onVerify={handleVerifyGap}
              onReject={handleRejectGap}
              onRequestEvidence={handleRequestEvidence}
              lang={lang}
            />
          </div>
        </div>
      )}

      {activeView === 'graph' && (
        <KnowledgeGraphView branchId={branchId} lang={lang} />
      )}

      {/* Add Source Modal */}
      <AddSourceModal
        branchId={branchId}
        branchName={branchData.name}
        isOpen={showAddSource}
        onClose={() => setShowAddSource(false)}
        onSourceAdded={async () => {
          await loadAllBranchData();
          setUpdateNotification(
            lang === 'ta'
              ? 'புதிய நேரடி மூலப்பதிவு வெற்றிகரமாக இணைக்கப்பட்டது. மறுபகுப்பாய்வு இயக்கப்படுகிறது...'
              : 'New live source added. Re-running cultural analysis...'
          );
          setTimeout(() => handleRunAnalysis(), 500);
        }}
        lang={lang}
      />

      {/* Analysis Animated Modal */}
      {isAnalyzing && (
        <AnalysisProgress
          onComplete={() => setIsAnalyzing(false)}
          lang={lang}
        />
      )}
    </div>
  );
}
