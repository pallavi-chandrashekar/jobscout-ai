"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";
import type { JobPosting, PaginatedResponse } from "@/lib/types";
import JobCard from "@/components/jobs/JobCard";

export default function DashboardPage() {
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(0);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);

  // Scrape form
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("");
  const [remote, setRemote] = useState(false);
  const [scraping, setScraping] = useState(false);
  const [scrapeMsg, setScrapeMsg] = useState("");

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const params: Record<string, string | number> = { page, page_size: 20 };
      if (filter) params.search = filter;
      const res = await api.get<PaginatedResponse<JobPosting>>("/job-postings", { params });
      setJobs(res.data.items);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch (err) {
      console.error("Failed to fetch jobs", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchJobs(); }, [page, filter]);

  const handleScrape = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setScraping(true);
    setScrapeMsg("");
    try {
      const res = await api.post("/job-search/scrape", {
        query: query.trim(),
        location: location.trim() || null,
        remote,
        results_wanted: 25,
      });
      setScrapeMsg(res.data.message);
      setPage(1);
      setFilter("");
      await fetchJobs();
    } catch (err: any) {
      setScrapeMsg(err?.response?.data?.detail || "Scrape failed. Try again.");
    } finally {
      setScraping(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      {/* Search & Scrape */}
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">Find Jobs</h1>
        <p className="mt-1 text-sm text-gray-500">
          Search real job postings from LinkedIn, Indeed, and Glassdoor
        </p>

        <form onSubmit={handleScrape} className="mt-4 space-y-3">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Job title or keywords (e.g. Data Engineer)"
              required
              className="col-span-1 rounded-lg border border-gray-200 px-4 py-2.5 text-sm focus:border-blue-500 focus:outline-none sm:col-span-2"
            />
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Location (e.g. San Francisco)"
              className="rounded-lg border border-gray-200 px-4 py-2.5 text-sm focus:border-blue-500 focus:outline-none"
            />
          </div>
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 text-sm text-gray-600">
              <input
                type="checkbox"
                checked={remote}
                onChange={(e) => setRemote(e.target.checked)}
                className="rounded border-gray-300"
              />
              Remote only
            </label>
            <button
              type="submit"
              disabled={scraping || !query.trim()}
              className="rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-blue-700 disabled:opacity-50"
            >
              {scraping ? "Searching..." : "Search Jobs"}
            </button>
          </div>
        </form>

        {scrapeMsg && (
          <div className="mt-3 rounded-lg bg-blue-50 px-4 py-2.5 text-sm text-blue-700">
            {scrapeMsg}
          </div>
        )}
      </div>

      {/* Filter existing results */}
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-gray-700">{total} jobs in database</p>
        <input
          type="text"
          value={filter}
          onChange={(e) => { setFilter(e.target.value); setPage(1); }}
          placeholder="Filter by title or company..."
          className="w-64 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
        />
      </div>

      {/* Job listings */}
      {loading ? (
        <div className="py-12 text-center text-gray-500">Loading...</div>
      ) : jobs.length === 0 ? (
        <div className="rounded-xl border border-dashed border-gray-300 py-16 text-center">
          <p className="text-lg font-medium text-gray-600">No jobs yet</p>
          <p className="mt-1 text-sm text-gray-400">
            Search for jobs above to get started
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      )}

      {/* Pagination */}
      {pages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm text-gray-500">
            Page {page} of {pages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(pages, p + 1))}
            disabled={page === pages}
            className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
