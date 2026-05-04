"use client";

import { useState } from "react";
import api from "@/lib/api";

const OUTCOMES = [
  { value: "hired", label: "Hired", emoji: "🎉" },
  { value: "interviewed", label: "Interviewed", emoji: "🤝" },
  { value: "rejected", label: "Rejected", emoji: "❌" },
  { value: "no_response", label: "No Response", emoji: "😶" },
  { value: "ghosted", label: "Ghosted", emoji: "👻" },
  { value: "fake", label: "Fake/Scam", emoji: "🚩" },
];

interface Props {
  jobId: string;
  onSubmitted?: () => void;
}

export default function FeedbackForm({ jobId, onSubmitted }: Props) {
  const [outcome, setOutcome] = useState("");
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!outcome) return;
    setLoading(true);
    try {
      await api.post("/job-feedbacks", {
        job_id: jobId,
        outcome,
        comment: comment || undefined,
      });
      setSuccess(true);
      setOutcome("");
      setComment("");
      onSubmitted?.();
    } catch (err) {
      console.error("Failed to submit feedback", err);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="rounded-lg border border-green-200 bg-green-50 p-4 text-sm text-green-700">
        Thanks for your feedback! It helps other job seekers.
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-lg border border-gray-200 bg-white p-4">
      <h3 className="font-semibold text-gray-900">Share Your Experience</h3>
      <div className="grid grid-cols-3 gap-2">
        {OUTCOMES.map((o) => (
          <button
            key={o.value}
            type="button"
            onClick={() => setOutcome(o.value)}
            className={`rounded-lg border px-3 py-2 text-sm transition-colors ${
              outcome === o.value
                ? "border-blue-500 bg-blue-50 text-blue-700"
                : "border-gray-200 hover:bg-gray-50"
            }`}
          >
            {o.emoji} {o.label}
          </button>
        ))}
      </div>
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Optional comment..."
        className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
        rows={2}
      />
      <button
        type="submit"
        disabled={!outcome || loading}
        className="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Submitting..." : "Submit Feedback"}
      </button>
    </form>
  );
}
