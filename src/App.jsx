import { useState } from 'react';
import { AppProvider, useAppState } from './context/AppContext';
import Sidebar from './components/layout/Sidebar';
import MainContent from './components/layout/MainContent';
import LocationBar from './components/ui/LocationBar';
import VisionAgentPanel from './components/panels/VisionAgentPanel';
import ClimateAgentPanel from './components/panels/ClimateAgentPanel';
import SatelliteAgentPanel from './components/panels/SatelliteAgentPanel';
import OrchestrationPanel from './components/panels/OrchestrationPanel';
import RecommendationPanel from './components/panels/RecommendationPanel';

const pageConfig = {
  dashboard: { title: 'Disease Intelligence Dashboard', subtitle: 'Real-time multi-agent monitoring & analysis' },
  vision: { title: 'Vision Detection Agent', subtitle: 'CNN-based leaf disease classification & analysis' },
  climate: { title: 'Climate Risk Agent', subtitle: 'Weather-based outbreak prediction engine' },
  satellite: { title: 'Satellite Health Agent', subtitle: 'NDVI & vegetation stress analysis' },
  orchestration: { title: 'Orchestration Engine', subtitle: 'Multi-agent consensus & conflict resolution' },
  recommendations: { title: 'Action Recommendations', subtitle: 'AI-synthesized intervention strategies' },
};

function DashboardView() {
  return (
    <>
      <LocationBar />
      <div className="panel-grid">
        <VisionAgentPanel />
        <ClimateAgentPanel />
        <SatelliteAgentPanel />
      </div>
      <div className="panel-grid">
        <OrchestrationPanel />
      </div>
      <div className="panel-grid">
        <RecommendationPanel />
      </div>
    </>
  );
}

function SinglePanelView({ panel }) {
  return (
    <>
      {(panel === 'climate' || panel === 'satellite') && <LocationBar />}
      <div className="panel-grid">
        {panel === 'vision' && <VisionAgentPanel />}
        {panel === 'climate' && <ClimateAgentPanel />}
        {panel === 'satellite' && <SatelliteAgentPanel />}
        {panel === 'orchestration' && <OrchestrationPanel />}
        {panel === 'recommendations' && <RecommendationPanel />}
      </div>
    </>
  );
}

function AppContent() {
  const [activeNav, setActiveNav] = useState('dashboard');
  const config = pageConfig[activeNav];

  return (
    <div className="app-layout">
      <Sidebar activeNav={activeNav} onNavChange={setActiveNav} />
      <MainContent title={config.title} subtitle={config.subtitle}>
        {activeNav === 'dashboard' ? <DashboardView /> : <SinglePanelView panel={activeNav} />}
      </MainContent>
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}
