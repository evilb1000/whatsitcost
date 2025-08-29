import React from "react";
import MaterialTrends from "./components/MaterialTrends.jsx";
import GPTChatAssistant from "./components/GPTChatAssistant.jsx"; // ⬅️ import the assistant

function App() {
    return (
        <div className="min-h-screen bg-gray-100 text-gray-900 px-6 py-8">
            <div className="max-w-6xl mx-auto">
                <MaterialTrends />
            </div>

            {/* 💬 GPT Assistant */}
            <GPTChatAssistant />
        </div>
    );
}

export default App;
