import React, { useState } from "react";

export default function GPTChatAssistant() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const [showDisclaimer, setShowDisclaimer] = useState(false);
  const [disclaimerAcknowledged, setDisclaimerAcknowledged] = useState(false);

  const BACKEND_BASE = typeof window !== "undefined" && window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://whatsitcost.onrender.com";

  const handleSend = async () => {
    if (!input.trim()) return;

    // Intercept if disclaimer not yet accepted
    if (!disclaimerAcknowledged) {
      setShowDisclaimer(true);
      return;
    }

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    const chatPayload = {
      prompt: input,
    };

    console.log("🚀 Sending payload to backend:", chatPayload);

    try {
      const response = await fetch(`${BACKEND_BASE}/gpt`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(chatPayload),
      });

      const data = await response.json();
      console.log("🧠 Received response from backend:", data);

      if (data.chartData) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: { type: "chart", payload: data.chartData } },
        ]);
      } else if (typeof data.response === "string") {
        setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
      } else {
        console.error("❌ Malformed GPT response:", data);
      }
    } catch (error) {
      console.error("❌ GPT chat error:", error);
    }
  };

  return (
    <>
      <button
        onClick={() => {
          setOpen(true);
          if (!disclaimerAcknowledged) setShowDisclaimer(true);
        }}
        style={{
          position: "fixed",
          bottom: "24px",
          right: "24px",
          backgroundColor: "#2563eb",
          color: "white",
          padding: "14px 20px",
          borderRadius: "9999px",
          fontSize: "16px",
          zIndex: 9999,
          fontFamily: "josefin-sans, sans-serif",
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
          cursor: "pointer",
          transition: "all 0.2s ease-in-out",
        }}
        onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#1e40af")}
        onMouseOut={(e) => (e.currentTarget.style.backgroundColor = "#2563eb")}
      >
        Ask the AI
      </button>

      {showDisclaimer && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            backgroundColor: "rgba(0,0,0,0.6)",
            backdropFilter: "blur(6px)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 999999,
          }}
        >
          <div
            style={{
              backgroundColor: "white",
              padding: "32px",
              borderRadius: "20px",
              maxWidth: "500px",
              textAlign: "center",
              boxShadow: "0 20px 50px rgba(0,0,0,0.3)",
              fontFamily: "josefin-sans, sans-serif",
            }}
          >
            <h2 style={{ fontSize: "22px", marginBottom: "16px" }}>⚠️ Disclaimer</h2>
            <p style={{ fontSize: "16px", marginBottom: "24px" }}>
              The AI can be wrong. Always do your own research before making decisions.
            </p>
            <div style={{ display: "flex", justifyContent: "center", gap: "20px" }}>
              <button
                onClick={() => {
                  setDisclaimerAcknowledged(true);
                  setShowDisclaimer(false);
                }}
                style={{
                  backgroundColor: "#2563eb",
                  color: "white",
                  padding: "10px 20px",
                  borderRadius: "8px",
                  border: "none",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                Acknowledge
              </button>
              <button
                onClick={() => {
                  setShowDisclaimer(false);
                  setOpen(false);
                }}
                style={{
                  backgroundColor: "#e2e8f0",
                  color: "#1e293b",
                  padding: "10px 20px",
                  borderRadius: "8px",
                  border: "none",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                Go Back
              </button>
            </div>
          </div>
        </div>
      )}

      {open && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            backgroundColor: "rgba(0,0,0,0.3)",
            backdropFilter: "blur(8px)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 99999,
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(255, 255, 255, 0.85)",
              borderRadius: "16px",
              width: "100%",
              maxWidth: "600px",
              height: "80vh",
              padding: "24px",
              boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
              fontSize: "18px",
              fontFamily: "josefin-sans, sans-serif",
              display: "flex",
              flexDirection: "column",
              position: "relative",
            }}
          >
            {/* ✕ Close Button */}
            <button
              onClick={() => setOpen(false)}
              style={{
                position: "absolute",
                top: "16px",
                right: "16px",
                background: "#e2e8f0",
                border: "none",
                borderRadius: "9999px",
                padding: "6px 12px",
                fontSize: "14px",
                cursor: "pointer",
                fontWeight: "bold",
                color: "#334155",
                fontFamily: "josefin-sans, sans-serif",
              }}
            >
              ✕
            </button>

            <div style={{ fontWeight: "bold", fontSize: "24px", marginBottom: "16px" }}>
              GPT Assistant
            </div>

            <div
              style={{
                flex: 1,
                overflowY: "auto",
                marginBottom: "16px",
                display: "flex",
                flexDirection: "column",
                gap: "10px",
              }}
            >
              {messages.map((msg, i) => {
                const isUser = msg.role === "user";
                const baseStyle = {
                  backgroundColor: isUser ? "#e0f2fe" : "#f1f5f9",
                  padding: "10px 14px",
                  borderRadius: "10px",
                  alignSelf: isUser ? "flex-end" : "flex-start",
                  maxWidth: "80%",
                };

                if (typeof msg.content === "string") {
                  return (
                    <div key={i} style={baseStyle}>
                      {msg.content}
                    </div>
                  );
                }

                if (msg.content?.type === "chart") {
                  const { title, points, metric, material } = msg.content.payload || {};
                  return (
                    <div key={i} style={{ ...baseStyle, width: "100%", maxWidth: "100%" }}>
                      <div style={{ fontWeight: "bold", marginBottom: "6px" }}>{title || `${material} — ${metric}`}</div>
                      <div style={{ width: "100%", overflowX: "auto" }}>
                        {/* Simple inline SVG line chart (no extra deps) */}
                        <MiniLineChart data={points || []} height={160} />
                      </div>
                    </div>
                  );
                }

                return (
                  <div key={i} style={baseStyle}>
                    {JSON.stringify(msg.content)}
                  </div>
                );
              })}
            </div>

            <div style={{ display: "flex", gap: "10px" }}>
              <input
                style={{
                  flex: 1,
                  padding: "10px 12px",
                  borderRadius: "8px",
                  border: "1px solid #ccc",
                  fontFamily: "josefin-sans, sans-serif",
                }}
                placeholder="Ask something..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
              />
              <button
                onClick={handleSend}
                style={{
                  backgroundColor: "#2563eb",
                  color: "white",
                  padding: "10px 18px",
                  borderRadius: "8px",
                  border: "none",
                  fontFamily: "josefin-sans, sans-serif",
                }}
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

function MiniLineChart({ data, width = 560, height = 160, padding = 16 }) {
  // Guard
  if (!Array.isArray(data) || data.length === 0) {
    return <div style={{ fontStyle: "italic", color: "#64748b" }}>No data for chart.</div>;
  }

  // Map to x,y in SVG space
  const xs = data.map((_, i) => i);
  const ys = data.map((d) => Number(d.value));

  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const ySpan = maxY - minY || 1;

  const innerW = width - padding * 2;
  const innerH = height - padding * 2;

  const pointsStr = data
    .map((d, i) => {
      const x = padding + (i / Math.max(1, data.length - 1)) * innerW;
      const y = padding + (1 - (Number(d.value) - minY) / ySpan) * innerH;
      return `${x},${y}`;
    })
    .join(" ");

  // Horizontal zero line if 0 within range
  const showZero = minY <= 0 && maxY >= 0;
  const zeroY = padding + (1 - (0 - minY) / ySpan) * innerH;

  return (
    <svg width={width} height={height} style={{ background: "white", borderRadius: 8, border: "1px solid #e2e8f0" }}>
      <polyline fill="none" stroke="#2563eb" strokeWidth="2" points={pointsStr} />
      {showZero && <line x1={padding} x2={width - padding} y1={zeroY} y2={zeroY} stroke="#e2e8f0" strokeDasharray="4 4" />}
      {/* Simple axes labels: first and last date */}
      <text x={padding} y={height - 4} fontSize="10" fill="#64748b">
        {data[0]?.date}
      </text>
      <text x={width - padding} y={height - 4} fontSize="10" fill="#64748b" textAnchor="end">
        {data[data.length - 1]?.date}
      </text>
    </svg>
  );
}
