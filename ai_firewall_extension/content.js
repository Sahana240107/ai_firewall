console.log("AI FIREWALL CONTENT SCRIPT LOADED");

function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

async function checkTextWithAPI(text) {
  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    console.log("API response:", data); // 👈 so you can see what backend returns
    return data;
  } catch (error) {
    console.error("AI Firewall API error:", error);
    return null;
  }
}

function showWarning(element) {
  if (element.dataset.firewallWarned) return;
  element.dataset.firewallWarned = "true";
  element.style.outline = "3px solid red";

  const warning = document.createElement("div");
  warning.textContent = "⚠️ AI Firewall: Sensitive content detected!";
  warning.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 999999;
    background: #fff0f0;
    color: red;
    font-weight: bold;
    font-size: 14px;
    padding: 12px 16px;
    border: 2px solid red;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  `;
  warning.className = "ai-firewall-warning";
  document.body.appendChild(warning);

  // auto-dismiss after 4 seconds
  setTimeout(() => {
    warning.remove();
    delete element.dataset.firewallWarned;
    element.style.outline = "";
  }, 4000);
}

const handleInput = debounce(async (event) => {
  const el = event.target;

  const isTypable =
    el.tagName === "INPUT" ||
    el.tagName === "TEXTAREA" ||
    el.isContentEditable;

  if (!isTypable) return;

  const text = (el.value || el.innerText || "").trim();
  console.log("Detected input:", text); // 👈 confirms events are firing

  if (text.length <= 3) return;

  const result = await checkTextWithAPI(text);
  if (result && result.action === "BLOCK") {
    showWarning(el);
  }
}, 600);

// ✅ useCapture: true — catches events BEFORE the page can swallow them
document.addEventListener("input", handleInput, true);
document.addEventListener("keyup", handleInput, true);

// ✅ For Shadow DOM inputs — use MutationObserver to attach listeners directly
function attachToShadowInputs(root) {
  root.querySelectorAll("input, textarea").forEach((el) => {
    if (el.dataset.firewallAttached) return;
    el.dataset.firewallAttached = "true";
    el.addEventListener("input", handleInput, true);
    el.addEventListener("keyup", handleInput, true);
    console.log("AI Firewall attached to:", el);
  });
}

// Watch for dynamically added inputs (like GitHub's search bar)
const observer = new MutationObserver(() => {
  attachToShadowInputs(document);

  // also check shadow roots
  document.querySelectorAll("*").forEach((el) => {
    if (el.shadowRoot) attachToShadowInputs(el.shadowRoot);
  });
});

observer.observe(document.body, { childList: true, subtree: true });

// Run once immediately on load
attachToShadowInputs(document);