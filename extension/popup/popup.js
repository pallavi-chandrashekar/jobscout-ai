const OUTCOMES = [
  { value: "hired", label: "🎉 Hired" },
  { value: "interviewed", label: "🤝 Interviewed" },
  { value: "rejected", label: "❌ Rejected" },
  { value: "no_response", label: "😶 No Response" },
  { value: "ghosted", label: "👻 Ghosted" },
  { value: "fake", label: "🚩 Fake" },
];

let selectedOutcome = null;
let currentJobId = null;

function getScoreClass(score) {
  if (score >= 70) return "high";
  if (score >= 40) return "moderate";
  return "low";
}

function getScoreLabel(score) {
  if (score >= 70) return "High Trust";
  if (score >= 40) return "Moderate";
  return "Low Trust";
}

function renderScore(score, confidence) {
  const cls = getScoreClass(score);
  return `
    <div class="score-card ${cls}">
      <div class="score-number">${score}</div>
      <div class="score-label">${getScoreLabel(score)}</div>
      <div class="score-confidence">${confidence} confidence</div>
    </div>
  `;
}

function renderFeedbackForm() {
  const btns = OUTCOMES.map(
    (o) => `<button class="feedback-btn" data-outcome="${o.value}">${o.label}</button>`
  ).join("");

  return `
    <div class="feedback-section">
      <h3>Share your experience</h3>
      <div class="feedback-grid">${btns}</div>
      <button class="submit-btn" id="submit-feedback" disabled>Submit Feedback</button>
      <div id="feedback-status"></div>
    </div>
  `;
}

function renderNoJob() {
  return `<div class="no-job">Navigate to a job posting on LinkedIn, Indeed, or Glassdoor to see its trust score.</div>`;
}

async function init() {
  const content = document.getElementById("main-content");

  // Get current tab URL
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab?.url || "";

  const isJobPage =
    url.includes("linkedin.com/jobs") ||
    url.includes("indeed.com") ||
    url.includes("glassdoor.com/job-listing");

  if (!isJobPage) {
    content.innerHTML = renderNoJob();
    return;
  }

  const jobUrl = url.split("?")[0];
  content.innerHTML = `<div class="no-job">Loading...</div>`;

  // Search for job in our system
  chrome.runtime.sendMessage(
    { type: "API_REQUEST", method: "GET", path: `/job-postings?search=${encodeURIComponent(jobUrl)}&page_size=1` },
    (response) => {
      if (response?.ok && response.data?.items?.length > 0) {
        const job = response.data.items[0];
        currentJobId = job.id;

        // Get trust score
        chrome.runtime.sendMessage(
          { type: "API_REQUEST", method: "GET", path: `/trust-score/${job.id}` },
          (scoreRes) => {
            if (scoreRes?.ok && scoreRes.data) {
              content.innerHTML = renderScore(scoreRes.data.total, scoreRes.data.confidence) + renderFeedbackForm();
              attachFeedbackHandlers();
            } else {
              content.innerHTML = `<div class="score-card no-score"><div class="score-label">Score unavailable</div></div>` + renderFeedbackForm();
              attachFeedbackHandlers();
            }
          }
        );
      } else {
        content.innerHTML = `<div class="score-card no-score"><div class="score-label">Not tracked yet</div><div class="score-confidence">Visit the dashboard to add this job</div></div>`;
      }
    }
  );

  // Dashboard link
  chrome.runtime.sendMessage({ type: "GET_CONFIG" }, (config) => {
    const link = document.getElementById("dashboard-link");
    if (link && config?.apiUrl) {
      link.href = config.apiUrl.replace(":8000", ":3000") + "/dashboard";
      link.addEventListener("click", (e) => {
        e.preventDefault();
        chrome.tabs.create({ url: link.href });
      });
    }
  });
}

function attachFeedbackHandlers() {
  const btns = document.querySelectorAll(".feedback-btn");
  const submitBtn = document.getElementById("submit-feedback");

  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      btns.forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");
      selectedOutcome = btn.dataset.outcome;
      submitBtn.disabled = false;
    });
  });

  submitBtn?.addEventListener("click", () => {
    if (!selectedOutcome || !currentJobId) return;
    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";

    chrome.runtime.sendMessage(
      {
        type: "API_REQUEST",
        method: "POST",
        path: "/job-feedbacks",
        body: { job_id: currentJobId, outcome: selectedOutcome },
      },
      (response) => {
        const statusEl = document.getElementById("feedback-status");
        if (response?.ok) {
          statusEl.className = "status-msg status-success";
          statusEl.textContent = "Thanks for your feedback!";
          submitBtn.textContent = "Submitted";
        } else {
          statusEl.className = "status-msg status-error";
          statusEl.textContent = response?.data?.detail || "Failed to submit. Are you logged in?";
          submitBtn.disabled = false;
          submitBtn.textContent = "Submit Feedback";
        }
      }
    );
  });
}

init();
