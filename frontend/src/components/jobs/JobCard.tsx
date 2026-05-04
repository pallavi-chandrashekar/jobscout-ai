"use client";

import Link from "next/link";
import type { JobPosting } from "@/lib/types";
import TrustScoreBadge from "./TrustScoreBadge";

interface Props {
  job: JobPosting;
}

export default function JobCard({ job }: Props) {
  return (
    <Link href={`/dashboard/jobs/${job.id}`}>
      <div className="rounded-lg border border-gray-200 bg-white p-4 transition-shadow hover:shadow-md">
        <div className="flex items-start justify-between">
          <div className="min-w-0 flex-1">
            <h3 className="truncate font-semibold text-gray-900">{job.title || "Untitled Position"}</h3>
            <p className="mt-1 text-sm text-gray-600">{job.company || "Unknown Company"}</p>
            <div className="mt-2 flex flex-wrap gap-2 text-xs text-gray-500">
              {job.location && <span>{job.location}</span>}
              {job.source && (
                <>
                  <span>-</span>
                  <span className="capitalize">{job.source}</span>
                </>
              )}
              {(job.salary_min || job.salary_max) && (
                <>
                  <span>-</span>
                  <span>
                    {job.salary_min && `$${(job.salary_min / 1000).toFixed(0)}k`}
                    {job.salary_min && job.salary_max && " - "}
                    {job.salary_max && `$${(job.salary_max / 1000).toFixed(0)}k`}
                  </span>
                </>
              )}
            </div>
          </div>
          <div className="ml-4 flex-shrink-0">
            <TrustScoreBadge score={job.trust_score} />
          </div>
        </div>
      </div>
    </Link>
  );
}
