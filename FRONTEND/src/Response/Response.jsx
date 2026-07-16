import React, { useState } from "react";

const Query = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState({});

  // Replace this with the collection name you received
  const collection = localStorage.getItem("collection");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(localStorage.getItem("file_id"))
    const file_id=localStorage.getItem("file_id")
    try {
      const res = await fetch("http://127.0.0.1:5000/uploadQuery", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: query,
          file_id: file_id,
        }),
      });

      const data = await res.json();
      if (res.ok) {
          setResponse(data);
      } else {
          console.error(data.error);
          setResponse({});
      }
      console.log(data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <button type="submit">Ask</button>
      </form>

      <hr />

      {response.documents?.map((doc, index) => (
        <div key={index}>
          <p>{doc.text}</p>
          <small>Score: {doc.score}</small>
          <hr />
        </div>
      ))}
      <div>
        <h1>THE AI RESPONSE FOR YOUR QUERY</h1>
        <p>{response.ai_response}</p>
      </div>
    </div>
  );
};

export default Query;