import { useState } from 'react';

const API_BASE = 'http://localhost:8000';

const EXPERIENCE_OPTIONS = [
    { value: 'beginner', label: '🌱 Beginner', desc: '0-2 years' },
    { value: 'intermediate', label: '🌿 Intermediate', desc: '3-7 years' },
    { value: 'experienced', label: '🌳 Experienced', desc: '8+ years' },
];

const RISK_OPTIONS = [
    { value: 'conservative', label: '🛡 Conservative', desc: 'Low risk, steady returns' },
    { value: 'moderate', label: '⚖ Moderate', desc: 'Balanced risk-reward' },
    { value: 'aggressive', label: '🚀 Aggressive', desc: 'High risk, high reward' },
];

const LAND_OPTIONS = [
    'Under 1 acre',
    '1-2 acres',
    '2-5 acres',
    '5-10 acres',
    '10+ acres',
];

const CAPITAL_OPTIONS = [
    'Under ₹50,000',
    '₹50,000 - ₹2,00,000',
    '₹2,00,000 - ₹5,00,000',
    '₹5,00,000 - ₹10,00,000',
    '₹10,00,000+',
];

function ToggleGroup({ options, value, onChange }) {
    return (
        <div className="gp-toggle-group">
            {options.map(opt => (
                <button
                    key={opt.value}
                    type="button"
                    className={`gp-toggle-btn ${value === opt.value ? 'gp-toggle-active' : ''}`}
                    onClick={() => onChange(opt.value)}
                >
                    <span className="gp-toggle-label">{opt.label}</span>
                    <span className="gp-toggle-desc">{opt.desc}</span>
                </button>
            ))}
        </div>
    );
}

function SchemeCard({ scheme }) {
    return (
        <div className="gp-scheme-card">
            <div className="gp-scheme-header">
                <h4 className="gp-scheme-title">{scheme.title}</h4>
                {scheme.eligible && <span className="gp-badge gp-badge-eligible">✓ Eligible</span>}
                {scheme.eligible === false && <span className="gp-badge gp-badge-ineligible">✗ Not Eligible</span>}
            </div>
            {scheme.ministry && <div className="gp-scheme-ministry">{scheme.ministry}</div>}
            <p className="gp-scheme-desc">{scheme.description}</p>
            <div className="gp-scheme-details">
                {scheme.eligibility && (
                    <div className="gp-scheme-detail">
                        <span className="gp-detail-icon">👤</span>
                        <span>{scheme.eligibility}</span>
                    </div>
                )}
                {scheme.benefit && (
                    <div className="gp-scheme-detail">
                        <span className="gp-detail-icon">💰</span>
                        <span className="gp-detail-highlight">{scheme.benefit}</span>
                    </div>
                )}
            </div>
            {scheme.apply_url && scheme.apply_url !== 'Contact local agriculture office' && (
                <a href={scheme.apply_url} target="_blank" rel="noopener noreferrer" className="gp-scheme-link">
                    Apply Online →
                </a>
            )}
        </div>
    );
}

function TechCard({ tech }) {
    const priorityClass = (tech.priority || 'Medium').toLowerCase();
    return (
        <div className="gp-tech-card">
            <div className="gp-tech-header">
                <div>
                    <h4 className="gp-tech-title">{tech.name}</h4>
                    {tech.category && <span className="gp-tech-category">{tech.category}</span>}
                </div>
                <span className={`gp-badge gp-badge-priority-${priorityClass}`}>
                    {tech.priority || 'Medium'}
                </span>
            </div>
            <p className="gp-tech-reason">{tech.reasoning}</p>
            <div className="gp-tech-meta">
                {tech.investment && (
                    <div className="gp-tech-stat">
                        <span className="gp-tech-stat-label">Investment</span>
                        <span className="gp-tech-stat-value">{tech.investment}</span>
                    </div>
                )}
                {tech.roi_period && (
                    <div className="gp-tech-stat">
                        <span className="gp-tech-stat-label">ROI Period</span>
                        <span className="gp-tech-stat-value">{tech.roi_period}</span>
                    </div>
                )}
            </div>
        </div>
    );
}

export default function FarmerGrowthPlanner() {
    const [experienceLevel, setExperienceLevel] = useState('beginner');
    const [riskAppetite, setRiskAppetite] = useState('conservative');
    const [landSize, setLandSize] = useState('1-2 acres');
    const [availableCapital, setAvailableCapital] = useState('Under ₹50,000');
    const [irrigation, setIrrigation] = useState(false);
    const [coldStorage, setColdStorage] = useState(false);
    const [region, setRegion] = useState('');
    const [primaryCrop, setPrimaryCrop] = useState('');

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`${API_BASE}/api/growth/roadmap`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    experience_level: experienceLevel,
                    land_size: landSize,
                    available_capital: availableCapital,
                    risk_appetite: riskAppetite,
                    irrigation,
                    cold_storage: coldStorage,
                    region: region || null,
                    primary_crop: primaryCrop || null,
                }),
            });
            if (!res.ok) {
                const err = await res.json().catch(() => ({ detail: 'Request failed' }));
                throw new Error(err.detail || 'Request failed');
            }
            const data = await res.json();
            setResult(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    const strategy = result?.economic_strategy;
    const schemes = result?.subsidy_schemes || [];
    const techs = result?.technology_advisor || [];
    const warnings = result?.risk_warnings || [];

    return (
        <div className="gp-page">
            {/* ── Header ── */}
            <div className="gp-header">
                <div className="gp-header-left">
                    <div className="gp-header-badge"><span className="gp-dot" /> AI-Powered</div>
                    <h1 className="gp-title">Farmer Growth Planner</h1>
                    <p className="gp-subtitle">Get a personalised profit roadmap with government schemes, technology recommendations, and economic strategy</p>
                </div>
            </div>

            {/* ── Onboarding Form ── */}
            <div className="gp-form-section">
                <div className="gp-form-grid">
                    {/* Experience */}
                    <div className="gp-form-block gp-form-block--full">
                        <label className="gp-form-label">👨‍🌾 Farming Experience</label>
                        <ToggleGroup options={EXPERIENCE_OPTIONS} value={experienceLevel} onChange={setExperienceLevel} />
                    </div>

                    {/* Risk */}
                    <div className="gp-form-block gp-form-block--full">
                        <label className="gp-form-label">📊 Risk Appetite</label>
                        <ToggleGroup options={RISK_OPTIONS} value={riskAppetite} onChange={setRiskAppetite} />
                    </div>

                    {/* Land Size */}
                    <div className="gp-form-block">
                        <label className="gp-form-label">🌾 Land Size</label>
                        <select className="gp-select" value={landSize} onChange={e => setLandSize(e.target.value)}>
                            {LAND_OPTIONS.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                        </select>
                    </div>

                    {/* Capital */}
                    <div className="gp-form-block">
                        <label className="gp-form-label">💰 Available Capital</label>
                        <select className="gp-select" value={availableCapital} onChange={e => setAvailableCapital(e.target.value)}>
                            {CAPITAL_OPTIONS.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                        </select>
                    </div>

                    {/* Region */}
                    <div className="gp-form-block">
                        <label className="gp-form-label">📍 Region <span className="gp-optional">(optional)</span></label>
                        <input className="gp-input" type="text" value={region} onChange={e => setRegion(e.target.value)} placeholder="e.g. Kerala, Maharashtra" />
                    </div>

                    {/* Primary Crop */}
                    <div className="gp-form-block">
                        <label className="gp-form-label">🌿 Primary Crop <span className="gp-optional">(optional)</span></label>
                        <input className="gp-input" type="text" value={primaryCrop} onChange={e => setPrimaryCrop(e.target.value)} placeholder="e.g. Banana, Tomato, Rice" />
                    </div>

                    {/* Infrastructure */}
                    <div className="gp-form-block gp-form-block--full">
                        <label className="gp-form-label">🏗 Infrastructure</label>
                        <div className="gp-checkbox-row">
                            <label className="gp-checkbox-label">
                                <input type="checkbox" checked={irrigation} onChange={e => setIrrigation(e.target.checked)} />
                                <span className="gp-checkbox-custom" />
                                <span>Irrigation Facility</span>
                            </label>
                            <label className="gp-checkbox-label">
                                <input type="checkbox" checked={coldStorage} onChange={e => setColdStorage(e.target.checked)} />
                                <span className="gp-checkbox-custom" />
                                <span>Cold Storage Access</span>
                            </label>
                        </div>
                    </div>
                </div>

                <button className="gp-generate-btn" onClick={handleGenerate} disabled={loading}>
                    {loading ? (
                        <><span className="gp-spinner" /> Generating Your Roadmap…</>
                    ) : (
                        <>🚀 Generate My Profit Roadmap</>
                    )}
                </button>
            </div>

            {/* ── Error ── */}
            {error && (
                <div className="gp-error-banner">
                    <span>⚠ {error}</span>
                    <button className="gp-retry-btn" onClick={handleGenerate}>Retry</button>
                </div>
            )}

            {/* ── Results ── */}
            {result && !loading && (
                <div className="gp-results">
                    {/* Economic Strategy */}
                    {strategy && (
                        <div className="gp-strategy-card">
                            <div className="gp-strategy-header">
                                <span className="gp-strategy-icon">📈</span>
                                <div>
                                    <h3 className="gp-strategy-title">{strategy.title || 'Your Growth Roadmap'}</h3>
                                    <p className="gp-strategy-summary">{strategy.summary}</p>
                                </div>
                                {strategy.estimated_income_boost && (
                                    <div className="gp-income-boost">
                                        <span className="gp-boost-label">Est. Income Boost</span>
                                        <span className="gp-boost-value">{strategy.estimated_income_boost}</span>
                                    </div>
                                )}
                            </div>

                            <div className="gp-timeline">
                                {strategy.year1_actions?.length > 0 && (
                                    <div className="gp-timeline-phase">
                                        <div className="gp-timeline-marker gp-marker-y1">
                                            <span className="gp-marker-dot" />
                                            <span className="gp-marker-label">Year 1</span>
                                        </div>
                                        <ul className="gp-timeline-items">
                                            {strategy.year1_actions.map((a, i) => <li key={i}>{a}</li>)}
                                        </ul>
                                    </div>
                                )}
                                {strategy.year2_actions?.length > 0 && (
                                    <div className="gp-timeline-phase">
                                        <div className="gp-timeline-marker gp-marker-y2">
                                            <span className="gp-marker-dot" />
                                            <span className="gp-marker-label">Year 2</span>
                                        </div>
                                        <ul className="gp-timeline-items">
                                            {strategy.year2_actions.map((a, i) => <li key={i}>{a}</li>)}
                                        </ul>
                                    </div>
                                )}
                                {strategy.year3_target && (
                                    <div className="gp-timeline-phase">
                                        <div className="gp-timeline-marker gp-marker-y3">
                                            <span className="gp-marker-dot" />
                                            <span className="gp-marker-label">Year 3 Target</span>
                                        </div>
                                        <div className="gp-year3-target">{strategy.year3_target}</div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Subsidy Schemes */}
                    {schemes.length > 0 && (
                        <div className="gp-section">
                            <h3 className="gp-section-title"><span>🏛</span> Government Subsidy Schemes</h3>
                            <div className="gp-schemes-grid">
                                {schemes.map((s, i) => <SchemeCard key={i} scheme={s} />)}
                            </div>
                        </div>
                    )}

                    {/* Technology Advisor */}
                    {techs.length > 0 && (
                        <div className="gp-section">
                            <h3 className="gp-section-title"><span>⚙</span> Technology Adoption Advisor</h3>
                            <div className="gp-tech-grid">
                                {techs.map((t, i) => <TechCard key={i} tech={t} />)}
                            </div>
                        </div>
                    )}

                    {/* Risk Warnings */}
                    {warnings.length > 0 && (
                        <div className="gp-warnings">
                            <h4 className="gp-warnings-title">⚠ Risk Considerations</h4>
                            <ul className="gp-warnings-list">
                                {warnings.map((w, i) => <li key={i}>{w}</li>)}
                            </ul>
                        </div>
                    )}
                </div>
            )}

            {/* ── Empty state ── */}
            {!result && !loading && !error && (
                <div className="gp-empty-state">
                    <div className="gp-empty-icon">🗺️</div>
                    <h3>Your personalized roadmap awaits</h3>
                    <p>Fill in your farming profile above and click "Generate" to receive AI-powered recommendations tailored to your situation.</p>
                </div>
            )}
        </div>
    );
}
