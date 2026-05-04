"use client";

import type { TrustScoreDetail } from "@/lib/types";

interface Props {
  detail: TrustScoreDetail;
}

function ScoreBar({ label, score, max, color }: { label: string; score: number; max: number; color: string }) {
  const pct = Math.round((score / max) * 100);
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span className="text-gray-600">{label}</span>
        <span className="font-medium">{score}/{max}</span>
      </div>
      <div className="h-2 rounded-full bg-gray-200">
        <div className={`h-2 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export default function TrustScoreBreakdown({ detail }: Props) {
  return (
    <div className="space-y-3 rounded-lg border border-gray-200 bg-white p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Trust Score Breakdown</h3>
        <span className="text-2xl font-bold text-gray-900">{detail.total}/100</span>
      </div>
      <div className="text-xs text-gray-500">
        Confidence: <span className="font-medium capitalize">{detail.confidence}</span>
      </div>
      <div className="space-y-2 pt-2">
        <ScoreBar label="Freshness" score={detail.freshness_score} max={25} color="bg-blue-500" />
        <ScoreBar label="Community Feedback" score={detail.feedback_score} max={35} color="bg-purple-500" />
        <ScoreBar label="Company Verified" score={detail.company_score} max={15} color="bg-green-500" />
        <ScoreBar label="Posting Quality" score={detail.quality_score} max={25} color="bg-orange-500" />
      </div>
    </div>
  );
}
