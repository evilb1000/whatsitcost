import React from "react";
import MaterialTrends from "./components/MaterialTrends.jsx";
import GPTChatAssistant from "./components/GPTChatAssistant.jsx"; // ⬅️ import the assistant

function App() {
    return (
        <div>
            <MaterialTrends />
            {/* 💬 GPT Assistant */}
            <GPTChatAssistant />
        </div>
    );
}

export default App;
