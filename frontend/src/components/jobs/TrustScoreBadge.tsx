"use client";

interface TrustScoreBadgeProps {
  score: number | null;
  size?: "sm" | "md" | "lg";
}

export default function TrustScoreBadge({ score, size = "md" }: TrustScoreBadgeProps) {
  if (score === null || score === undefined) {
    return (
      <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-500">
        No Score
      </span>
    );
  }

  const getColor = (s: number) => {
    if (s >= 70) return "bg-green-100 text-green-800 border-green-200";
    if (s >= 40) return "bg-yellow-100 text-yellow-800 border-yellow-200";
    return "bg-red-100 text-red-800 border-red-200";
  };

  const getLabel = (s: number) => {
    if (s >= 70) return "High Trust";
    if (s >= 40) return "Moderate";
    return "Low Trust";
  };

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
    lg: "text-base px-4 py-1.5",
  };

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border font-semibold ${getColor(score)} ${sizeClasses[size]}`}>
      <span>{score}</span>
      <span className="font-normal">{getLabel(score)}</span>
    </span>
  );
}
