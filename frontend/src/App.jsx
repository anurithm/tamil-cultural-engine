import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Chatbot from './components/Chatbot';
import Dashboard from './pages/Dashboard';
import Traditions from './pages/Traditions';
import BranchDetail from './pages/BranchDetail';
import SourcesPage from './pages/SourcesPage';
import GapsPage from './pages/GapsPage';
import VerificationPage from './pages/VerificationPage';
import PreservedPage from './pages/PreservedPage';
import GlossaryPage from './pages/GlossaryPage';
import KnowledgeGraphView from './components/KnowledgeGraphView';
import { api } from './services/api';

export default function App() {
  const [lang, setLang] = useState('en');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [loadingDashboard, setLoadingDashboard] = useState(true);
  const [isReloadingDemo, setIsReloadingDemo] = useState(false);
  const [selectedDomainId, setSelectedDomainId] = useState(null);
  const [selectedBranchId, setSelectedBranchId] = useState('karagattam');
  const [toast, setToast] = useState(null);

  const fetchDashboard = async () => {
    try {
      setLoadingDashboard(true);
      const data = await api.getDashboard();
      setDashboardData(data);
    } catch (err) {
      console.error('Failed to load dashboard:', err);
    } finally {
      setLoadingDashboard(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const handleLoadDemo = async () => {
    setIsReloadingDemo(true);
    try {
      const res = await api.loadDemoData();
      await fetchDashboard();
      setToast(res.message || 'Demo dataset reloaded successfully!');
      setTimeout(() => setToast(null), 4000);
    } catch (err) {
      alert(`Error reloading demo: ${err.message}`);
    } finally {
      setIsReloadingDemo(false);
    }
  };

  const handleSelectDomain = (domainId) => {
    setSelectedDomainId(domainId);
    setActiveTab('traditions');
  };

  const handleSelectBranch = (branchId) => {
    setSelectedBranchId(branchId);
    setActiveTab('branch-detail');
  };

  return (
    <div className="min-h-screen bg-[#F8E7C9] text-[#064e3b] flex flex-col">
      {/* Top Navbar */}
      <Navbar
        lang={lang}
        setLang={setLang}
        isLiveMode={dashboardData?.is_live_mode || false}
        onReloadDemo={handleLoadDemo}
      />

      {/* Global Toast */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 bg-slate-900 text-amber-200 px-4 py-2.5 rounded-xl shadow-lg border border-amber-400/30 text-xs font-semibold flex items-center space-x-2 animate-in slide-in-from-bottom">
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>{toast}</span>
        </div>
      )}

      {/* Main Layout */}
      <div className="flex flex-col md:flex-row flex-1">
        {/* Sidebar */}
        <Sidebar
          activeTab={activeTab === 'branch-detail' ? 'traditions' : activeTab}
          setActiveTab={(tab) => {
            setActiveTab(tab);
            if (tab === 'traditions') {
              setSelectedDomainId(null);
            }
          }}
          lang={lang}
          stats={dashboardData}
        />

        {/* Viewport Content */}
        <main className="flex-1 overflow-x-hidden pb-12">
          {activeTab === 'dashboard' && (
            <Dashboard
              dashboardData={dashboardData}
              loading={loadingDashboard}
              onSelectDomain={handleSelectDomain}
              onSelectBranch={handleSelectBranch}
              onLoadDemo={handleLoadDemo}
              isReloadingDemo={isReloadingDemo}
              lang={lang}
            />
          )}

          {activeTab === 'traditions' && (
            <Traditions
              traditions={dashboardData?.traditions || []}
              selectedDomainId={selectedDomainId}
              onSelectDomain={setSelectedDomainId}
              onSelectBranch={handleSelectBranch}
              lang={lang}
            />
          )}

          {activeTab === 'branch-detail' && (
            <BranchDetail
              branchId={selectedBranchId}
              onBack={() => setActiveTab('traditions')}
              onOpenVerification={() => setActiveTab('verification')}
              lang={lang}
            />
          )}

          {activeTab === 'sources' && (
            <SourcesPage
              onSelectBranch={handleSelectBranch}
              lang={lang}
            />
          )}

          {activeTab === 'knowledge' && (
            <BranchDetail
              branchId={selectedBranchId}
              onBack={() => setActiveTab('dashboard')}
              lang={lang}
            />
          )}

          {activeTab === 'gaps' && (
            <GapsPage
              onSelectBranch={handleSelectBranch}
              lang={lang}
            />
          )}

          {activeTab === 'evidence' && (
            <GapsPage
              onSelectBranch={handleSelectBranch}
              lang={lang}
            />
          )}

          {activeTab === 'verification' && (
            <VerificationPage
              lang={lang}
              onSelectBranch={handleSelectBranch}
            />
          )}

          {activeTab === 'preserved' && (
            <PreservedPage
              lang={lang}
            />
          )}

          {activeTab === 'graph' && (
            <div className="p-6 sm:p-8 max-w-7xl mx-auto space-y-4">
              <h1 className="text-2xl font-bold text-slate-900 font-serif-title">
                {lang === 'ta' ? 'அறிவு வரைபடம்' : 'Cultural Knowledge Graph'}
              </h1>
              <KnowledgeGraphView
                branchId={selectedBranchId}
                lang={lang}
              />
            </div>
          )}

          {activeTab === 'glossary' && (
            <GlossaryPage
              lang={lang}
            />
          )}
        </main>
        <Chatbot lang={lang} />
      </div>
    </div>
  );
}
