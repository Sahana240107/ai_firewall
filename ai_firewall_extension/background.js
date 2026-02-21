chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CHECK_TEXT") {
    fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message.text }),
    })
      .then((res) => res.json())
      .then((data) => sendResponse({ result: data }))
      .catch((err) => {
        console.error("Background fetch error:", err);
        sendResponse({ result: null });
      });

    return true; // keep message channel open for async response
  }
});