import { useState } from 'react';

const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'vision', label: 'Vision Agent', icon: '👁️' },
    { id: 'climate', label: 'Climate Agent', icon: '🌡️' },
    { id: 'satellite', label: 'Satellite Agent', icon: '🛰️' },
    { id: 'orchestration', label: 'Orchestration Engine', icon: '⚙️' },
    { id: 'recommendations', label: 'Action Recommendations', icon: '📋' },
];

export default function Sidebar({ activeNav, onNavChange }) {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">
                <div className="sidebar-brand-icon">🧬</div>
                <h1>Disease Intel</h1>
                <p>Multi-Agent Platform</p>
            </div>

            <nav className="sidebar-nav">
                <div className="sidebar-section-label">Navigation</div>
                {navItems.map((item) => (
                    <div
                        key={item.id}
                        className={`nav-item ${activeNav === item.id ? 'active' : ''}`}
                        onClick={() => onNavChange(item.id)}
                    >
                        <span className="nav-icon">{item.icon}</span>
                        <span>{item.label}</span>
                    </div>
                ))}
            </nav>

            <div className="sidebar-footer">
                <div className="sidebar-status">
                    <span className="status-dot"></span>
                    <span>All Systems Operational</span>
                </div>
            </div>
        </aside>
    );
}
