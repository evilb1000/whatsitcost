import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { collection, getDocs } from "firebase/firestore";
import { db } from "../firebase";

function ConsumerDashboard() {
    const navigate = useNavigate();
    const [indicators, setIndicators] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchIndicators() {
            try {
                console.log("Fetching consumer indicators...");
                const snapshot = await getDocs(collection(db, "Consumer Spending Indicators"));
                console.log("Snapshot size:", snapshot.size);
                console.log("Docs:", snapshot.docs);
                
                const data = [];
                snapshot.forEach((doc) => {
                    console.log("Processing doc:", doc.id, doc.data());
                    const indicatorData = doc.data();
                    const latest = indicatorData.observations && indicatorData.observations.length > 0 
                        ? indicatorData.observations[indicatorData.observations.length - 1]
                        : null;
                    
                    data.push({
                        id: doc.id,
                        series_name: indicatorData.series_name,
                        latest: latest
                    });
                });
                
                console.log("Processed data:", data);
                // Sort by series name
                data.sort((a, b) => a.series_name.localeCompare(b.series_name));
                setIndicators(data);
            } catch (error) {
                console.error("Error fetching indicators:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchIndicators();
    }, []);

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '40px', color: 'white' }}>
                <div style={{
                    background: 'linear-gradient(90deg, #1f2937 0%, #334155 100%)',
                    color: 'white',
                    borderRadius: '16px',
                    padding: '20px 16px',
                    boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
                    marginBottom: '12px'
                }}>
                    <h1 style={{ 
                        fontSize: '3.5rem', 
                        fontWeight: '900', 
                        margin: 0,
                        textAlign: 'center',
                        letterSpacing: '0.04em'
                    }}>
                        CONSUMER SPENDING DASHBOARD
                    </h1>
                    <div style={{ textAlign: 'center', marginTop: '20px' }}>
                        <p style={{
                            color: '#e5e7eb',
                            fontWeight: 700,
                            fontSize: '1.25rem',
                            margin: 0
                        }}>
                            Loading consumer indicators...
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div>
            {/* Header */}
            <div style={{
                background: 'linear-gradient(90deg, #1f2937 0%, #334155 100%)',
                color: 'white',
                borderRadius: '16px',
                padding: '20px 16px',
                boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
                marginBottom: '20px'
            }}>
                <h1 style={{ 
                    fontSize: '3.5rem', 
                    fontWeight: '900', 
                    margin: 0,
                    textAlign: 'center',
                    letterSpacing: '0.04em'
                }}>
                    CONSUMER SPENDING DASHBOARD
                </h1>
                <div style={{ textAlign: 'center', marginTop: '6px' }}>
                    <p style={{
                        color: '#e5e7eb',
                        fontWeight: 700,
                        fontSize: '1.25rem',
                        margin: 0
                    }}>
                        Latest Consumer Economic Indicators
                    </p>
                    <p style={{
                        color: '#d1d5db',
                        fontWeight: 600,
                        fontSize: '1rem',
                        margin: '8px 0 0 0'
                    }}>
                        {indicators.length} economic series tracked
                    </p>
                    <button 
                        onClick={() => navigate('/')}
                        style={{
                            marginTop: '12px',
                            background: 'linear-gradient(90deg, #4DAAf8 0%, #3886C8 100%)',
                            border: 'none',
                            borderRadius: '8px',
                            padding: '12px 24px',
                            color: 'white',
                            fontWeight: '700',
                            fontSize: '1rem',
                            cursor: 'pointer',
                            boxShadow: '0 4px 12px rgba(56, 134, 200, 0.3)',
                            transition: 'all 0.2s ease'
                        }}
                        onMouseOver={(e) => {
                            e.target.style.transform = 'translateY(-2px)';
                            e.target.style.boxShadow = '0 6px 16px rgba(56, 134, 200, 0.4)';
                        }}
                        onMouseOut={(e) => {
                            e.target.style.transform = 'translateY(0)';
                            e.target.style.boxShadow = '0 4px 12px rgba(56, 134, 200, 0.3)';
                        }}
                    >
                        ← Back to Material Trends
                    </button>
                </div>
            </div>

            {/* Dashboard Grid */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
                gap: '16px'
            }}>
                {indicators.map((indicator) => (
                    <div
                        key={indicator.id}
                        style={{
                            background: 'rgba(255, 255, 255, 0.35)',
                            backdropFilter: 'blur(20px)',
                            borderRadius: '20px',
                            padding: '24px',
                            border: '1px solid rgba(255, 255, 255, 0.35)',
                            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.25)',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            position: 'relative',
                            overflow: 'hidden'
                        }}
                        onMouseOver={(e) => {
                            e.target.style.transform = 'translateY(-4px) scale(1.02)';
                            e.target.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.35)';
                            e.target.style.background = 'rgba(255, 255, 255, 0.5)';
                            e.target.style.border = '1px solid rgba(255, 255, 255, 0.5)';
                        }}
                        onMouseOut={(e) => {
                            e.target.style.transform = 'translateY(0) scale(1)';
                            e.target.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.25)';
                            e.target.style.background = 'rgba(255, 255, 255, 0.35)';
                            e.target.style.border = '1px solid rgba(255, 255, 255, 0.35)';
                        }}
                    >
                        <h3 style={{
                            fontSize: '1.1rem',
                            fontWeight: '700',
                            color: '#ffffff',
                            margin: '0 0 12px 0',
                            lineHeight: '1.3',
                            textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)'
                        }}>
                            {indicator.series_name}
                        </h3>
                        
                        {indicator.latest ? (
                            <div>
                                <div style={{
                                    fontSize: '1.25rem',
                                    fontWeight: '800',
                                    color: '#ffffff',
                                    marginBottom: '8px',
                                    textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)'
                                }}>
                                    {typeof indicator.latest.value === 'number' 
                                        ? indicator.latest.value.toLocaleString(undefined, {
                                            minimumFractionDigits: indicator.latest.value < 1 ? 2 : 0,
                                            maximumFractionDigits: indicator.latest.value < 1 ? 4 : 2
                                        })
                                        : indicator.latest.value
                                    }
                                </div>
                                
                                <div style={{
                                    fontSize: '0.9rem',
                                    color: 'rgba(255, 255, 255, 0.8)',
                                    marginBottom: '12px',
                                    textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                                }}>
                                    {indicator.latest.date}
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.85rem' }}>
                                    <div style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                                        <strong style={{ color: '#ffffff', textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)' }}>MoM:</strong>
                                        <span style={{ 
                                            color: indicator.latest.mom_change > 0 ? '#ff6b6b' : '#51cf66',
                                            fontWeight: '600',
                                            marginLeft: '4px',
                                            textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                                        }}>
                                            {indicator.latest.mom_change !== null ? `${indicator.latest.mom_change.toFixed(2)}%` : '—'}
                                        </span>
                                    </div>
                                    <div style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                                        <strong style={{ color: '#ffffff', textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)' }}>YoY:</strong>
                                        <span style={{ 
                                            color: indicator.latest.yoy_change > 0 ? '#ff6b6b' : '#51cf66',
                                            fontWeight: '600',
                                            marginLeft: '4px',
                                            textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                                        }}>
                                            {indicator.latest.yoy_change !== null ? `${indicator.latest.yoy_change.toFixed(2)}%` : '—'}
                                        </span>
                                    </div>
                                    <div style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                                        <strong style={{ color: '#ffffff', textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)' }}>12Mo Avg:</strong>
                                        <span style={{ 
                                            color: indicator.latest.mom_12mo_avg > 0 ? '#ff6b6b' : '#51cf66',
                                            fontWeight: '600',
                                            marginLeft: '4px',
                                            textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                                        }}>
                                            {indicator.latest.mom_12mo_avg !== null ? `${indicator.latest.mom_12mo_avg.toFixed(2)}%` : '—'}
                                        </span>
                                    </div>
                                    <div style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                                        <strong style={{ color: '#ffffff', textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)' }}>36Mo Avg:</strong>
                                        <span style={{ 
                                            color: indicator.latest.mom_36mo_avg > 0 ? '#ff6b6b' : '#51cf66',
                                            fontWeight: '600',
                                            marginLeft: '4px',
                                            textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
                                        }}>
                                            {indicator.latest.mom_36mo_avg !== null ? `${indicator.latest.mom_36mo_avg.toFixed(2)}%` : '—'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '0.9rem', textShadow: '0 1px 2px rgba(0, 0, 0, 0.3)' }}>
                                No recent data available
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ConsumerDashboard;