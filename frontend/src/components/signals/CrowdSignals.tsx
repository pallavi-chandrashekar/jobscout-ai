"use client";

import type { FeedbackAggregation } from "@/lib/types";

interface Props {
  data: FeedbackAggregation;
}

const OUTCOME_CONFIG: Record<string, { label: string; color: string; emoji: string }> = {
  hired: { label: "Hired", color: "bg-green-500", emoji: "🎉" },
  interviewed: { label: "Interviewed", color: "bg-blue-500", emoji: "🤝" },
  rejected: { label: "Rejected", color: "bg-gray-400", emoji: "❌" },
  no_response: { label: "No Response", color: "bg-yellow-400", emoji: "😶" },
  ghosted: { label: "Ghosted", color: "bg-orange-500", emoji: "👻" },
  fake: { label: "Fake/Scam", color: "bg-red-500", emoji: "🚩" },
};

export default function CrowdSignals({ data }: Props) {
  if (data.total_feedbacks === 0) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-4 text-sm text-gray-500">
        No community feedback yet. Be the first to share your experience!
      </div>
    );
  }

  return (
    <div className="space-y-3 rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Community Signals</h3>
        <span className="text-sm text-gray-500">
          {data.total_feedbacks} report{data.total_feedbacks !== 1 ? "s" : ""} - {data.confidence} confidence
        </span>
      </div>
      {/* Stacked bar */}
      <div className="flex h-4 overflow-hidden rounded-full">
        {Object.entries(data.outcome_counts).map(([outcome, count]) => {
          const config = OUTCOME_CONFIG[outcome];
          const pct = (count / data.total_feedbacks) * 100;
          if (!config || pct === 0) return null;
          return (
            <div
              key={outcome}
              className={`${config.color}`}
              style={{ width: `${pct}%` }}
              title={`${config.label}: ${count}`}
            />
          );
        })}
      </div>
      {/* Legend */}
      <div className="flex flex-wrap gap-3 text-xs">
        {Object.entries(data.outcome_counts).map(([outcome, count]) => {
          const config = OUTCOME_CONFIG[outcome];
          if (!config) return null;
          return (
            <span key={outcome} className="flex items-center gap-1">
              <span className={`inline-block h-2 w-2 rounded-full ${config.color}`} />
              {config.emoji} {config.label}: {count}
            </span>
          );
        })}
      </div>
    </div>
  );
}
