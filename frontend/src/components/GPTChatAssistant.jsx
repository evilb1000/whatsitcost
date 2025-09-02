import React, { useState, useRef, useEffect } from "react";

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
        console.log("📊 Chart data received:", data.chartData);
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
            padding: "20px",
            boxSizing: "border-box",
            isolation: "isolate",
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(255, 255, 255, 0.85)",
              borderRadius: "16px",
              width: "100%",
              maxWidth: "1600px",
              height: "90vh",
              padding: "24px",
              boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
              fontSize: "18px",
              fontFamily: "josefin-sans, sans-serif",
              color: "#1e293b",
              display: "flex",
              flexDirection: "column",
              position: "relative",
              overflow: "hidden",
              isolation: "isolate",
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
                overflowX: "hidden",
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
                  const { title, points, metric, material, series } = msg.content.payload || {};
                  return (
                    <div key={i} style={{ ...baseStyle, width: "100%", maxWidth: "100%" }}>
                      <div style={{ fontWeight: "bold", marginBottom: "6px" }}>{title || `${material} — ${metric}`}</div>
                      <div style={{ width: "100%" }}>
                        {/* Simple inline SVG line chart (no extra deps) */}
                        {Array.isArray(series) && series.length > 0 ? (
                          <MiniMultiLineChart series={series} height={200} />
                        ) : (
                          <MiniLineChart data={points || []} height={160} material={material} />
                        )}
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

function MiniLineChart({ data, width = "100%", height = 180, padding = 56, material = "Material" }) {
  // Guard
  if (!Array.isArray(data) || data.length === 0) {
    return <div style={{ fontStyle: "italic", color: "#64748b" }}>No data for chart.</div>;
  }

  // CSV Export function
  const exportToCSV = () => {
    const csvContent = [
      "Date,MoM Percentage",
      ...data.map(d => `${d.date},${d.value}`)
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${material.replace(/[^a-zA-Z0-9]/g, '_')}_trendline.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  // Map to x,y in SVG space
  const xs = data.map((_, i) => i);
  const ys = data.map((d) => Number(d.value));

  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const ySpan = maxY - minY || 1;

  const containerRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(typeof width === 'number' ? width : 800);

  useEffect(() => {
    if (!containerRef.current) return;
    const node = containerRef.current;
    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = Math.floor(entry.contentRect.width);
        if (w && w !== containerWidth) setContainerWidth(w);
      }
    });
    ro.observe(node);
    // initialize
    const w0 = Math.floor(node.getBoundingClientRect().width);
    if (w0) setContainerWidth(w0);
    return () => ro.disconnect();
  }, []);

  const chartWidth = typeof width === 'number' ? width : containerWidth;
  const innerW = chartWidth - padding * 2;
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

  // Y axis ticks
  const numTicks = 5;
  const tickVals = Array.from({ length: numTicks }, (_, i) => minY + (i * ySpan) / (numTicks - 1));
  const yToSvg = (v) => padding + (1 - (v - minY) / ySpan) * innerH;

  return (
    <div ref={containerRef}>
      {/* Download Button */}
      <div style={{ marginBottom: "8px", display: "flex", justifyContent: "flex-start" }}>
        <button
          onClick={exportToCSV}
          style={{
            backgroundColor: "#16a34a",
            color: "white",
            padding: "6px 12px",
            borderRadius: "6px",
            border: "none",
            fontSize: "12px",
            fontFamily: "josefin-sans, sans-serif",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "4px"
          }}
        >
          📊 Download
        </button>
      </div>
      
      <svg width={chartWidth} height={height} style={{ background: "white", borderRadius: 8, border: "1px solid #e2e8f0" }}>
        {/* Y grid and ticks */}
        {tickVals.map((tv, i) => (
          <g key={i}>
            <line x1={padding} x2={chartWidth - padding} y1={yToSvg(tv)} y2={yToSvg(tv)} stroke="#eef2f7" />
            <text x={padding - 12} y={yToSvg(tv) + 3} fontSize="10" fill={Number(tv) < 0 ? "#dc2626" : "#64748b"} textAnchor="end">
              {Number(tv).toFixed(2)}%
            </text>
          </g>
        ))}

        {/* Zero line emphasis */}
        {showZero && <line x1={padding} x2={chartWidth - padding} y1={zeroY} y2={zeroY} stroke="#cbd5e1" strokeDasharray="4 4" />}

        {/* Data line */}
        <polyline fill="none" stroke="#2563eb" strokeWidth="2" points={pointsStr} />

        {/* Axis label */}
        <text x={padding} y={padding - 6} fontSize="10" fontWeight="bold" fill="#64748b">Month Over Month Percentage Change In Pricing Series</text>

        {/* X labels: first and last date */}
        <text x={padding} y={height - 4} fontSize="10" fill="#64748b">
          {data[0]?.date}
        </text>
        <text x={chartWidth - padding} y={height - 4} fontSize="10" fill="#64748b" textAnchor="end">
          {data[data.length - 1]?.date}
        </text>
      </svg>
    </div>
  );
}

function MiniMultiLineChart({ series, width = "100%", height = 220, padding = 56 }) {
  const colors = ["#2563eb", "#16a34a", "#dc2626", "#7c3aed"];
  const clean = (series || []).filter((s) => Array.isArray(s.points) && s.points.length > 0);
  if (clean.length === 0) {
    return <div style={{ fontStyle: "italic", color: "#64748b" }}>No data for chart.</div>;
  }

  // CSV Export function for multi-series
  const exportToCSV = () => {
    // Get all unique dates across all series
    const allDates = [...new Set(clean.flatMap(s => s.points.map(p => p.date)))].sort();
    
    // Create header with material names
    const headers = ["Date", ...clean.map(s => s.material || "Unknown Material")];
    
    // Create rows
    const rows = allDates.map(date => {
      const row = [date];
      clean.forEach(s => {
        const point = s.points.find(p => p.date === date);
        row.push(point ? point.value : "");
      });
      return row.join(",");
    });
    
    const csvContent = [headers.join(","), ...rows].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `multi_series_trendlines.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  // Determine global min/max across all series
  const allValues = clean.flatMap((s) => s.points.map((p) => Number(p.value)));
  const minY = Math.min(...allValues);
  const maxY = Math.max(...allValues);
  const ySpan = maxY - minY || 1;

  const containerRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(typeof width === 'number' ? width : 1000);

  useEffect(() => {
    if (!containerRef.current) return;
    const node = containerRef.current;
    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = Math.floor(entry.contentRect.width);
        if (w && w !== containerWidth) setContainerWidth(w);
      }
    });
    ro.observe(node);
    const w0 = Math.floor(node.getBoundingClientRect().width);
    if (w0) setContainerWidth(w0);
    return () => ro.disconnect();
  }, []);

  const maxLen = Math.max(...clean.map((s) => s.points.length));
  const chartWidth = typeof width === 'number' ? width : containerWidth;
  const innerW = chartWidth - padding * 2;
  const innerH = height - padding * 2;

  const toXY = (len, idx, val) => {
    const x = padding + (idx / Math.max(1, len - 1)) * innerW;
    const y = padding + (1 - (Number(val) - minY) / ySpan) * innerH;
    return `${x},${y}`;
  };

  // Y axis ticks
  const numTicks = 5;
  const tickVals = Array.from({ length: numTicks }, (_, i) => minY + (i * ySpan) / (numTicks - 1));
  const yToSvg = (v) => padding + (1 - (v - minY) / ySpan) * innerH;

  // Legend
  const legend = (
    <div style={{ display: "flex", gap: 12, marginBottom: 6, flexWrap: "wrap" }}>
      {clean.map((s, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 12, height: 12, background: colors[i % colors.length], display: "inline-block", borderRadius: 2 }} />
          <span style={{ fontSize: 12, color: "#334155" }}>{s.material || "Unknown Material"}</span>
        </div>
      ))}
    </div>
  );

  // Labels (first/last date from longest series)
  const firstDate = clean.find((s) => s.points.length === maxLen)?.points[0]?.date || clean[0].points[0].date;
  const lastDate = clean.find((s) => s.points.length === maxLen)?.points[maxLen - 1]?.date || clean[0].points.slice(-1)[0].date;

  return (
    <div ref={containerRef}>
      {/* Download Button */}
      <div style={{ marginBottom: "8px", display: "flex", justifyContent: "flex-start" }}>
        <button
          onClick={exportToCSV}
          style={{
            backgroundColor: "#16a34a",
            color: "white",
            padding: "6px 12px",
            borderRadius: "6px",
            border: "none",
            fontSize: "12px",
            fontFamily: "josefin-sans, sans-serif",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "4px"
          }}
        >
          📊 Download
        </button>
      </div>
      
      {legend}
      <svg width={chartWidth} height={height} style={{ background: "white", borderRadius: 8, border: "1px solid #e2e8f0" }}>
        {/* Y grid and ticks */}
        {tickVals.map((tv, i) => (
          <g key={i}>
            <line x1={padding} x2={chartWidth - padding} y1={yToSvg(tv)} y2={yToSvg(tv)} stroke="#eef2f7" />
            <text x={padding - 12} y={yToSvg(tv) + 3} fontSize="10" fill={Number(tv) < 0 ? "#dc2626" : "#64748b"} textAnchor="end">
              {Number(tv).toFixed(2)}%
            </text>
          </g>
        ))}
        {clean.map((s, i) => {
          const pts = s.points
            .map((p, idx) => toXY(s.points.length, idx, p.value))
            .join(" ");
          return <polyline key={i} fill="none" stroke={colors[i % colors.length]} strokeWidth="2" points={pts} />;
        })}
        {minY <= 0 && maxY >= 0 && (
          <line x1={padding} x2={chartWidth - padding} y1={padding + (1 - (0 - minY) / ySpan) * innerH} y2={padding + (1 - (0 - minY) / ySpan) * innerH} stroke="#e2e8f0" strokeDasharray="4 4" />
        )}
        {/* Axis label */}
        <text x={padding} y={padding - 6} fontSize="10" fontWeight="bold" fill="#64748b">Month Over Month Percentage Change In Pricing Series</text>
        <text x={padding} y={height - 4} fontSize="10" fill="#64748b">{firstDate}</text>
        <text x={chartWidth - padding} y={height - 4} fontSize="10" fill="#64748b" textAnchor="end">{lastDate}</text>
      </svg>
    </div>
  );
}
