"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import type { JobPosting, TrustScoreDetail, FeedbackAggregation } from "@/lib/types";
import TrustScoreBadge from "@/components/jobs/TrustScoreBadge";
import TrustScoreBreakdown from "@/components/jobs/TrustScoreBreakdown";
import FeedbackForm from "@/components/jobs/FeedbackForm";
import CrowdSignals from "@/components/signals/CrowdSignals";
import OutreachGenerator from "@/components/outreach/OutreachGenerator";

export default function JobDetailPage() {
  const params = useParams();
  const jobId = params.id as string;

  const [job, setJob] = useState<JobPosting | null>(null);
  const [trustDetail, setTrustDetail] = useState<TrustScoreDetail | null>(null);
  const [feedbackAgg, setFeedbackAgg] = useState<FeedbackAggregation | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const [jobRes, trustRes, feedbackRes] = await Promise.all([
        api.get<JobPosting>(`/job-postings/${jobId}`),
        api.get<TrustScoreDetail>(`/trust-score/${jobId}`),
        api.get<FeedbackAggregation>(`/job-feedbacks/aggregation/${jobId}`),
      ]);
      setJob(jobRes.data);
      setTrustDetail(trustRes.data);
      setFeedbackAgg(feedbackRes.data);
    } catch (err) {
      console.error("Failed to fetch job details", err);
    } finally {
      setLoading(false);
    }
  }, [jobId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  if (loading) return <div className="py-12 text-center text-gray-500">Loading...</div>;
  if (!job) return <div className="py-12 text-center text-gray-500">Job not found</div>;

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {/* Header */}
      <div className="rounded-lg border border-gray-200 bg-white p-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{job.title || "Untitled Position"}</h1>
            <p className="mt-1 text-lg text-gray-600">{job.company || "Unknown Company"}</p>
            <div className="mt-2 flex flex-wrap gap-3 text-sm text-gray-500">
              {job.location && <span>{job.location}</span>}
              {job.source && <span className="capitalize">{job.source}</span>}
              {(job.salary_min || job.salary_max) && (
                <span>
                  {job.salary_min && `$${(job.salary_min / 1000).toFixed(0)}k`}
                  {job.salary_min && job.salary_max && " - "}
                  {job.salary_max && `$${(job.salary_max / 1000).toFixed(0)}k`}
                </span>
              )}
            </div>
          </div>
          <TrustScoreBadge score={job.trust_score} size="lg" />
        </div>
        {job.description && (
          <div className="mt-4 border-t pt-4 text-sm text-gray-700 whitespace-pre-wrap">
            {job.description}
          </div>
        )}
        {job.url && (
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-block text-sm font-medium text-blue-600 hover:text-blue-700"
          >
            View Original Posting
          </a>
        )}
      </div>

      {/* Trust Score Breakdown */}
      {trustDetail && <TrustScoreBreakdown detail={trustDetail} />}

      {/* Crowd Signals */}
      {feedbackAgg && <CrowdSignals data={feedbackAgg} />}

      {/* Feedback Form */}
      <FeedbackForm jobId={jobId} onSubmitted={fetchData} />

      {/* Outreach Generator */}
      <OutreachGenerator jobId={jobId} jobTitle={job.title || undefined} />
    </div>
  );
}
