import React, { useState } from "react";

export default function GPTChatAssistant() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const [showDisclaimer, setShowDisclaimer] = useState(false);
  const [disclaimerAcknowledged, setDisclaimerAcknowledged] = useState(false);

  const BACKEND_BASE = "https://whatsitcost.onrender.com";

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

      if (typeof data.response === "string") {
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
              {messages.map((msg, i) => (
                <div
                  key={i}
                  style={{
                    backgroundColor: msg.role === "user" ? "#e0f2fe" : "#f1f5f9",
                    padding: "10px 14px",
                    borderRadius: "10px",
                    alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                    maxWidth: "80%",
                  }}
                >
                  {msg.content}
                </div>
              ))}
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
