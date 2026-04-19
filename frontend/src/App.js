import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState(null);

  // SEND MESSAGE
  const sendMessage = async () => {
    if (!message) return;

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message,
      });

      setMessages((prev) => [
        ...prev,
        { role: "user", text: message },
        { role: "ai", text: res.data.reply },
      ]);

      setMessage("");
    } catch (err) {
      console.error(err);
    }
  };

  // UPLOAD PDF
  const uploadPDF = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setMessages((prev) => [
        ...prev,
        { role: "ai", text: res.data.reply },
      ]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="app">
      <h1>🤖 Demo-Gowtham-AI agent</h1>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role}>
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type message..."
        />

        <button onClick={sendMessage}>Send</button>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={uploadPDF}>Upload</button>
      </div>
    </div>
  );
}

export default App;