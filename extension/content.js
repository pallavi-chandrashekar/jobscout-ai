(function () {
  "use strict";

  const BADGE_ID = "jobscout-trust-badge";

  function getCurrentJobUrl() {
    const url = window.location.href;
    if (url.includes("linkedin.com/jobs")) return url.split("?")[0];
    if (url.includes("indeed.com")) return url.split("?")[0];
    if (url.includes("glassdoor.com/job-listing")) return url.split("?")[0];
    return null;
  }

  function getScoreColor(score) {
    if (score >= 70) return { bg: "#dcfce7", text: "#166534", border: "#bbf7d0", label: "High Trust" };
    if (score >= 40) return { bg: "#fef9c3", text: "#854d0e", border: "#fde68a", label: "Moderate" };
    return { bg: "#fee2e2", text: "#991b1b", border: "#fecaca", label: "Low Trust" };
  }

  function createBadge(score, confidence) {
    const existing = document.getElementById(BADGE_ID);
    if (existing) existing.remove();

    const colors = getScoreColor(score);
    const badge = document.createElement("div");
    badge.id = BADGE_ID;
    badge.className = "jobscout-badge";
    badge.innerHTML = `
      <div class="jobscout-badge-inner" style="background:${colors.bg};border:1px solid ${colors.border};color:${colors.text}">
        <span class="jobscout-badge-score">${score}</span>
        <span class="jobscout-badge-label">${colors.label}</span>
        <span class="jobscout-badge-confidence">${confidence} confidence</span>
      </div>
    `;

    badge.addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "GET_CONFIG" }, (config) => {
        if (config.apiUrl) {
          window.open(`${config.apiUrl.replace(":8000", ":3000")}/dashboard`, "_blank");
        }
      });
    });

    return badge;
  }

  function createSubmitButton(jobUrl) {
    const existing = document.getElementById(BADGE_ID);
    if (existing) existing.remove();

    const btn = document.createElement("div");
    btn.id = BADGE_ID;
    btn.className = "jobscout-badge";
    btn.innerHTML = `
      <div class="jobscout-badge-inner jobscout-submit-btn">
        <span>JobScout AI</span>
        <span class="jobscout-badge-label">Check Trust Score</span>
      </div>
    `;

    btn.addEventListener("click", () => {
      btn.querySelector(".jobscout-badge-inner").innerHTML = `<span>Checking...</span>`;
      submitAndCheck(jobUrl, btn);
    });

    return btn;
  }

  async function submitAndCheck(jobUrl, badgeElement) {
    const title = document.title || "";
    const company = extractCompany();

    chrome.runtime.sendMessage(
      {
        type: "API_REQUEST",
        method: "POST",
        path: "/job-postings",
        body: {
          url: jobUrl,
          title: title.slice(0, 200),
          company: company,
          source: detectSource(),
          is_active: true,
        },
      },
      (response) => {
        if (response && response.ok && response.data) {
          fetchAndDisplayScore(response.data.id);
        } else if (response && response.status === 400) {
          // Already exists — try to find it
          chrome.runtime.sendMessage(
            { type: "API_REQUEST", method: "GET", path: `/job-postings?search=${encodeURIComponent(jobUrl)}` },
            (searchRes) => {
              if (searchRes?.ok && searchRes.data?.items?.length > 0) {
                fetchAndDisplayScore(searchRes.data.items[0].id);
              } else {
                badgeElement.querySelector(".jobscout-badge-inner").innerHTML = `<span>Could not check</span>`;
              }
            }
          );
        }
      }
    );
  }

  function fetchAndDisplayScore(jobId) {
    chrome.runtime.sendMessage(
      { type: "API_REQUEST", method: "GET", path: `/trust-score/${jobId}` },
      (response) => {
        if (response?.ok && response.data) {
          const { total, confidence } = response.data;
          const badge = createBadge(total, confidence);
          injectBadge(badge);
        }
      }
    );
  }

  function extractCompany() {
    const host = window.location.hostname;
    if (host.includes("linkedin.com")) {
      const el = document.querySelector(".job-details-jobs-unified-top-card__company-name a");
      return el?.textContent?.trim() || null;
    }
    if (host.includes("indeed.com")) {
      const el = document.querySelector("[data-company-name]") || document.querySelector(".jobsearch-CompanyInfoContainer a");
      return el?.textContent?.trim() || null;
    }
    return null;
  }

  function detectSource() {
    const host = window.location.hostname;
    if (host.includes("linkedin")) return "linkedin";
    if (host.includes("indeed")) return "indeed";
    if (host.includes("glassdoor")) return "glassdoor";
    return "other";
  }

  function injectBadge(badge) {
    const host = window.location.hostname;
    let target;

    if (host.includes("linkedin.com")) {
      target = document.querySelector(".job-details-jobs-unified-top-card__job-title") ||
               document.querySelector("h1") ||
               document.querySelector(".jobs-details__main-content");
    } else if (host.includes("indeed.com")) {
      target = document.querySelector(".jobsearch-JobInfoHeader-title") ||
               document.querySelector("h1");
    } else if (host.includes("glassdoor.com")) {
      target = document.querySelector("[data-test='job-title']") ||
               document.querySelector("h1");
    }

    if (target) {
      target.parentElement.insertBefore(badge, target.nextSibling);
    } else {
      document.body.appendChild(badge);
    }
  }

  function init() {
    const jobUrl = getCurrentJobUrl();
    if (!jobUrl) return;

    // Check if job already exists in our system
    chrome.runtime.sendMessage(
      { type: "API_REQUEST", method: "GET", path: `/job-postings?search=${encodeURIComponent(jobUrl)}&page_size=1` },
      (response) => {
        if (response?.ok && response.data?.items?.length > 0) {
          const job = response.data.items[0];
          if (job.trust_score !== null && job.trust_score !== undefined) {
            const badge = createBadge(job.trust_score, "cached");
            injectBadge(badge);
          } else {
            fetchAndDisplayScore(job.id);
          }
        } else {
          const btn = createSubmitButton(jobUrl);
          injectBadge(btn);
        }
      }
    );
  }

  // LinkedIn uses SPA navigation — watch for URL changes
  let lastUrl = location.href;
  const observer = new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      setTimeout(init, 1500);
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });

  // Initial load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => setTimeout(init, 1500));
  } else {
    setTimeout(init, 1500);
  }
})();
