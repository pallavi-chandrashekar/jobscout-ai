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
import ResumeTailor from "@/components/jobs/ResumeTailor";

export default function JobDetailPage() {
  const params = useParams();
  const jobId = params.id as string;

  const [job, setJob] = useState<JobPosting | null>(null);
  const [trustDetail, setTrustDetail] = useState<TrustScoreDetail | null>(null);
  const [feedbackAgg, setFeedbackAgg] = useState<FeedbackAggregation | null>(null);
  const [loading, setLoading] = useState(true);
  const [tailoredResume, setTailoredResume] = useState<string | null>(null);
  const [coverLetter, setCoverLetter] = useState<string | null>(null);
  const [applyStatus, setApplyStatus] = useState<string>("");

  const fetchData = useCallback(async () => {
    try {
      const jobRes = await api.get<JobPosting>(`/job-postings/${jobId}`);
      setJob(jobRes.data);
    } catch (err) {
      console.error("Failed to fetch job", err);
    }
    try {
      const trustRes = await api.get<TrustScoreDetail>(`/trust-score/${jobId}`);
      setTrustDetail(trustRes.data);
    } catch (err) {
      console.error("Failed to fetch trust score", err);
    }
    try {
      const feedbackRes = await api.get<FeedbackAggregation>(`/job-feedbacks/aggregation/${jobId}`);
      setFeedbackAgg(feedbackRes.data);
    } catch (err) {
      console.error("Failed to fetch feedback", err);
    }
    setLoading(false);
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
          <div className="mt-4">
            <div className="flex gap-3">
              <button
                onClick={async () => {
                  try {
                    await api.post("/job-applications", {
                      job_id: job.id,
                      tailored_resume: tailoredResume,
                      cover_letter: coverLetter,
                    });
                    if (tailoredResume || coverLetter) {
                      setApplyStatus("Applied — your tailored resume was saved with this application.");
                    } else {
                      setApplyStatus("Applied — no resume attached. Tailor a resume below first if you want it saved.");
                    }
                  } catch {
                    setApplyStatus("Failed to track application");
                  }
                  window.open(job.url, "_blank");
                }}
                className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-700"
              >
                Apply Now
              </button>
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-lg border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
              >
                View Original
              </a>
              {(tailoredResume || coverLetter) && (
                <span className="flex items-center text-xs text-green-700">
                  ✓ Tailored {tailoredResume && "resume"}{tailoredResume && coverLetter && " + "}{coverLetter && "cover letter"} ready
                </span>
              )}
            </div>
            {applyStatus && (
              <p className="mt-2 text-xs text-gray-600">{applyStatus}</p>
            )}
          </div>
        )}
      </div>

      {/* Trust Score Breakdown */}
      {trustDetail && <TrustScoreBreakdown detail={trustDetail} />}

      {/* Crowd Signals */}
      {feedbackAgg && <CrowdSignals data={feedbackAgg} />}

      {/* Feedback Form */}
      <FeedbackForm jobId={jobId} onSubmitted={fetchData} />

      {/* Resume Tailor */}
      <ResumeTailor
        jobId={jobId}
        jobTitle={job.title || undefined}
        company={job.company || undefined}
        onGenerated={(resume, cover) => {
          setTailoredResume(resume);
          setCoverLetter(cover);
          setApplyStatus("");
        }}
      />

      {/* Outreach Generator */}
      <OutreachGenerator jobId={jobId} jobTitle={job.title || undefined} />
    </div>
  );
}
