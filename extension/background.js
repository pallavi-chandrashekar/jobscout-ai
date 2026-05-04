const DEFAULT_API_URL = "http://localhost:8000";

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ apiUrl: DEFAULT_API_URL, token: "" });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_CONFIG") {
    chrome.storage.local.get(["apiUrl", "token"], (data) => {
      sendResponse({ apiUrl: data.apiUrl || DEFAULT_API_URL, token: data.token || "" });
    });
    return true;
  }

  if (message.type === "SET_TOKEN") {
    chrome.storage.local.set({ token: message.token });
    sendResponse({ success: true });
    return true;
  }

  if (message.type === "API_REQUEST") {
    chrome.storage.local.get(["apiUrl", "token"], async (data) => {
      const url = `${data.apiUrl || DEFAULT_API_URL}${message.path}`;
      const headers = { "Content-Type": "application/json" };
      if (data.token) {
        headers["Authorization"] = `Bearer ${data.token}`;
      }

      try {
        const options = { method: message.method || "GET", headers };
        if (message.body) {
          options.body = JSON.stringify(message.body);
        }
        const response = await fetch(url, options);
        const result = await response.json();
        sendResponse({ ok: response.ok, status: response.status, data: result });
      } catch (err) {
        sendResponse({ ok: false, status: 0, error: err.message });
      }
    });
    return true;
  }
});
