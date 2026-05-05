"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import api from "@/lib/api";
import type { JobApplication, JobPosting } from "@/lib/types";

interface AppWithJob extends JobApplication {
  job?: JobPosting;
}

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<AppWithJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const res = await api.get<JobApplication[]>("/job-applications");
        // Fetch job details for each application
        const enriched = await Promise.all(
          res.data.map(async (app) => {
            try {
              const jobRes = await api.get<JobPosting>(`/job-postings/${app.job_id}`);
              return { ...app, job: jobRes.data };
            } catch {
              return app as AppWithJob;
            }
          })
        );
        setApplications(enriched);
      } catch (err) {
        console.error("Failed to fetch applications", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  const statusColor = (status: string) => {
    switch (status) {
      case "applied": return "bg-blue-100 text-blue-700";
      case "interviewing": return "bg-yellow-100 text-yellow-700";
      case "offered": return "bg-green-100 text-green-700";
      case "rejected": return "bg-red-100 text-red-700";
      default: return "bg-gray-100 text-gray-700";
    }
  };

  const downloadFile = (text: string, filename: string) => {
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">My Applications</h1>

      {loading ? (
        <div className="py-12 text-center text-gray-500">Loading...</div>
      ) : applications.length === 0 ? (
        <div className="rounded-xl border border-dashed border-gray-300 py-16 text-center">
          <p className="text-lg font-medium text-gray-600">No applications yet</p>
          <p className="mt-1 text-sm text-gray-400">Find a job and click Apply Now to track it here</p>
        </div>
      ) : (
        <div className="space-y-3">
          {applications.map((app) => {
            const isOpen = expanded === app.id;
            const hasResume = !!app.tailored_resume;
            const hasCover = !!app.cover_letter;
            const company = app.job?.company || "Unknown";

            return (
              <div key={app.id} className="rounded-lg border border-gray-200 bg-white">
                <div className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="min-w-0 flex-1">
                      <Link href={`/dashboard/jobs/${app.job_id}`}>
                        <h3 className="font-semibold text-gray-900 hover:text-blue-600">
                          {app.job?.title || "Job"}
                        </h3>
                      </Link>
                      <p className="text-sm text-gray-600">{company}</p>
                      <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-gray-500">
                        <span className={`rounded-full px-2 py-0.5 font-medium ${statusColor(app.status)}`}>
                          {app.status}
                        </span>
                        <span>Applied {app.applied_date ? new Date(app.applied_date).toLocaleDateString() : "-"}</span>
                        {hasResume && (
                          <span className="rounded-full bg-green-50 px-2 py-0.5 text-green-700">
                            Resume saved
                          </span>
                        )}
                        {hasCover && (
                          <span className="rounded-full bg-purple-50 px-2 py-0.5 text-purple-700">
                            Cover letter saved
                          </span>
                        )}
                      </div>
                    </div>
                    {(hasResume || hasCover) && (
                      <button
                        onClick={() => setExpanded(isOpen ? null : app.id)}
                        className="ml-4 rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-50"
                      >
                        {isOpen ? "Hide" : "View Resume"}
                      </button>
                    )}
                  </div>
                </div>

                {isOpen && (
                  <div className="space-y-3 border-t border-gray-200 bg-gray-50 p-4">
                    {hasResume && (
                      <div>
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-semibold text-gray-700">Tailored Resume</h4>
                          <button
                            onClick={() => downloadFile(app.tailored_resume!, `resume_${company.replace(/\s+/g, "_")}.txt`)}
                            className="rounded bg-white px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
                          >
                            Download
                          </button>
                        </div>
                        <div className="mt-2 max-h-64 overflow-y-auto whitespace-pre-wrap rounded border border-gray-200 bg-white p-3 text-xs text-gray-700">
                          {app.tailored_resume}
                        </div>
                      </div>
                    )}
                    {hasCover && (
                      <div>
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-semibold text-gray-700">Cover Letter</h4>
                          <button
                            onClick={() => downloadFile(app.cover_letter!, `cover_letter_${company.replace(/\s+/g, "_")}.txt`)}
                            className="rounded bg-white px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
                          >
                            Download
                          </button>
                        </div>
                        <div className="mt-2 max-h-64 overflow-y-auto whitespace-pre-wrap rounded border border-gray-200 bg-white p-3 text-xs text-gray-700">
                          {app.cover_letter}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
