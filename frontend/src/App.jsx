import React, { useEffect, useState } from "react";
import MaterialTrends from "./components/MaterialTrends.jsx";
import GPTChatAssistant from "./components/GPTChatAssistant.jsx"; // ⬅️ import the assistant

function App() {
    const [railSpacer, setRailSpacer] = useState(0);

    useEffect(() => {
        const updateSpacer = () => {
            const el = document.getElementById("gridStart");
            if (!el) return;
            // Recompute on scroll/resize (sticky uses viewport)
            const top = el.getBoundingClientRect().top; // viewport-relative
            setRailSpacer(Math.max(0, Math.round(top)));
        };
        const rafUpdate = () => requestAnimationFrame(updateSpacer);
        updateSpacer();
        window.addEventListener("resize", rafUpdate);
        window.addEventListener("scroll", rafUpdate, { passive: true });
        const t1 = setTimeout(updateSpacer, 150);
        const t2 = setTimeout(updateSpacer, 350);
        return () => {
            window.removeEventListener("resize", rafUpdate);
            window.removeEventListener("scroll", rafUpdate);
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
                    gap: '16px'
                }}
            >
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
                <MaterialTrends />
            </main>

            {/* Right sponsor rail */}
            <aside style={{ position: 'static', marginTop: `${railSpacer}px`, backgroundColor: '#BE6428', padding: '0 24px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', gap: '16px' }}>
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
