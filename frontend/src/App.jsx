import React, { useLayoutEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MaterialTrends from "./components/MaterialTrends.jsx";
import ConsumerDashboard from "./components/ConsumerDashboard.jsx";
import GPTChatAssistant from "./components/GPTChatAssistant.jsx"; // ⬅️ import the assistant

function App() {
    const [railSpacer, setRailSpacer] = useState(220); // seed so first paint is close
    const [measured, setMeasured] = useState(false);


    useLayoutEffect(() => {
        const updateSpacer = () => {
            const el = document.getElementById("gridStart");
            if (!el) return;
            // Recompute on scroll/resize (sticky uses viewport)
            const top = el.getBoundingClientRect().top; // viewport-relative
            setRailSpacer(Math.max(0, Math.round(top)));
            setMeasured(true);
        };
        const rafUpdate = () => requestAnimationFrame(updateSpacer);
        updateSpacer();
        window.addEventListener("resize", rafUpdate);
        window.addEventListener("scroll", rafUpdate, { passive: true });
        window.addEventListener("load", updateSpacer, { once: true });
        // Ensure fonts/layout shifts are accounted for
        if (document?.fonts?.ready) {
            // eslint-disable-next-line @typescript-eslint/no-floating-promises
            document.fonts.ready.then(updateSpacer);
        }
        const t1 = setTimeout(updateSpacer, 150);
        const t2 = setTimeout(updateSpacer, 350);
        return () => {
            window.removeEventListener("resize", rafUpdate);
            window.removeEventListener("scroll", rafUpdate);
            window.removeEventListener("load", updateSpacer);
            clearTimeout(t1);
            clearTimeout(t2);
        };
    }, []);
    return (
        <div
            style={{
                display: 'grid',
                gridTemplateColumns: '1fr minmax(980px, 1100px) 1fr',
                gap: '32px',
                minHeight: '100vh',
                backgroundColor: '#BE6428',
                padding: '0 32px'
            }}
        >
            {/* Left sponsor rail */}
            <aside
                style={{
                    position: 'static',
                    marginTop: `${railSpacer}px`,
                    backgroundColor: '#BE6428',
                    padding: '0 24px',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'flex-start',
                    gap: '16px',
                    opacity: measured ? 1 : 0,
                    transition: 'opacity 120ms ease-out'
                }}
            >
                {/* Sponsored label */}
                <div style={{
                    width: '100%',
                    textAlign: 'center',
                    color: '#f1f5f9',
                    letterSpacing: '0.08em',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    fontSize: '0.9rem',
                    background: 'rgba(56,134,200,0.18)',
                    borderRadius: '10px',
                    padding: '8px 10px 10px',
                    marginBottom: '6px',
                    boxShadow: '0 4px 10px rgba(0,0,0,0.15)'
                }}>
                    Sponsored by
                    <div style={{
                        height: '3px',
                        width: '60%',
                        margin: '6px auto 0',
                        borderRadius: '6px',
                        background: 'linear-gradient(90deg,#4DAAf8 0%, #3886C8 100%)'
                    }} />
                </div>
                <a href="https://www.studio1049.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/Studio%201049.png"
                        alt="Studio 1049"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://www.mbawpa.org/" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/MBA_Logo2025.PNG"
                        alt="Master Builders' Association"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://www.mosites.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/Mosites.webp"
                        alt="Mosites Construction"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://tedco.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/tedco.png"
                        alt="TEDCO Construction"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://amartinigc.com/" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/amartini-logo2x.png"
                        alt="A. Martini & Co."
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://www.jendoco.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/jendoco.jpeg"
                        alt="Jendoco Construction"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://www.landau-bldg.com/" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/landua-logo-trans.png"
                        alt="Landau Building Company"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
                <a href="https://ryconinc.com/" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img
                        src="/sponsors/rycon-logo.webp"
                        alt="Rycon Construction"
                        style={{ width: '520px', maxWidth: '100%', height: 'auto', borderRadius: '6px' }}
                    />
                </a>
            </aside>

            {/* Center content */}
            <main style={{ maxWidth: '1100px', margin: '0 auto' }}>
                <Router>
                    <Routes>
                        <Route path="/" element={<MaterialTrends />} />
                        <Route path="/consumer" element={<ConsumerDashboard />} />
                    </Routes>
                </Router>
            </main>

            {/* Right sponsor rail */}
            <aside style={{ position: 'static', marginTop: `${railSpacer}px`, backgroundColor: '#BE6428', padding: '0 24px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', gap: '16px', opacity: measured ? 1 : 0, transition: 'opacity 120ms ease-out' }}>
                {/* Sponsored label */}
                <div style={{
                    width: '100%',
                    textAlign: 'center',
                    color: '#f1f5f9',
                    letterSpacing: '0.08em',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    fontSize: '0.9rem',
                    background: 'rgba(56,134,200,0.18)',
                    borderRadius: '10px',
                    padding: '8px 10px 10px',
                    marginBottom: '6px',
                    boxShadow: '0 4px 10px rgba(0,0,0,0.15)'
                }}>
                    Sponsored by
                    <div style={{
                        height: '3px',
                        width: '60%',
                        margin: '6px auto 0',
                        borderRadius: '6px',
                        background: 'linear-gradient(90deg,#4DAAf8 0%, #3886C8 100%)'
                    }} />
                </div>
                <a href="https://www.mascaroconstruction.com/" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/ico-mascaro.png" alt="Mascaro Construction" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                <a href="https://www.massarocg.com/" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/massaro.avif" alt="Massaro Construction Group" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                <a href="https://pjdick.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp_pittsburgh" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/pj dick.jpg" alt="PJ Dick" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                <a href="https://volpatt.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/volpattlogo.jpg" alt="Volpatt Construction" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                <a href="https://www.fjbusse.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/Busse.webp" alt="F.J. Busse Company" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                <a href="https://www.turnerconstruction.com/locations/pittsburgh" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/turner.png" alt="Turner Construction" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                <a href="https://www.burchick.com" target="_blank" rel="noopener noreferrer" style={{ display: 'block' }}>
                    <img src="/sponsors/burchick_construction_logo.png.webp" alt="Burchick Construction" style={{ width: '360px', height: 'auto', borderRadius: '6px', display: 'block' }} />
                </a>
                {/* Mosites moved to left rail */}
            </aside>

            {/* 💬 GPT Assistant */}
            <GPTChatAssistant />
        </div>
    );
}

export default App;
