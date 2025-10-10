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
                {/* Sponsors removed - structure preserved for future use */}
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
                {/* Sponsors removed - structure preserved for future use */}
            </aside>

            {/* 💬 GPT Assistant */}
            <GPTChatAssistant />
        </div>
    );
}

export default App;
