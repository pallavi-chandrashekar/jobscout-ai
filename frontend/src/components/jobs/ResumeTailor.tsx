"use client";

import { useState } from "react";
import api from "@/lib/api";

interface Props {
  jobId: string;
  jobTitle?: string;
  company?: string;
}

interface TailorResult {
  tailored_resume: string;
  cover_letter: string;
  provider: string;
  model: string;
  tokens_used: number;
}

export default function ResumeTailor({ jobId, jobTitle, company }: Props) {
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState<TailorResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"resume" | "cover">("resume");
  const [copied, setCopied] = useState(false);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      setResumeText(ev.target?.result as string);
    };
    reader.readAsText(file);
  };

  const handleTailor = async () => {
    if (!resumeText.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await api.post<TailorResult>("/resume/tailor", {
        job_id: jobId,
        resume_text: resumeText,
      });
      setResult(res.data);
      setActiveTab("resume");
    } catch (err) {
      console.error("Failed to tailor resume", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = (text: string, filename: string) => {
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div>
        <h3 className="text-lg font-semibold text-gray-900">
          Tailor Resume {jobTitle && `for "${jobTitle}"`}
        </h3>
        <p className="text-sm text-gray-500">
          Paste your resume or upload a text file. AI will rewrite it to match this job's requirements and generate a cover letter.
        </p>
      </div>

      {!result ? (
        <>
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Your base resume
            </label>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your resume here..."
              className="w-full rounded-lg border border-gray-200 px-4 py-3 text-sm focus:border-blue-500 focus:outline-none"
              rows={8}
            />
            <div className="mt-2 flex items-center gap-3">
              <label className="cursor-pointer rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50">
                Upload .txt file
                <input
                  type="file"
                  accept=".txt,.md"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
              {resumeText && (
                <span className="text-xs text-gray-400">
                  {resumeText.length} characters
                </span>
              )}
            </div>
          </div>

          <button
            onClick={handleTailor}
            disabled={loading || !resumeText.trim()}
            className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-sm font-medium text-white transition-all hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50"
          >
            {loading ? "AI is tailoring your resume..." : "Tailor Resume + Generate Cover Letter"}
          </button>
        </>
      ) : (
        <>
          {/* Tabs */}
          <div className="flex gap-1 rounded-lg bg-gray-100 p-1">
            <button
              onClick={() => setActiveTab("resume")}
              className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                activeTab === "resume"
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              Tailored Resume
            </button>
            <button
              onClick={() => setActiveTab("cover")}
              className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                activeTab === "cover"
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              Cover Letter
            </button>
          </div>

          {/* Content */}
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>
                Generated by {result.provider} ({result.model}) — {result.tokens_used} tokens
              </span>
              <div className="flex gap-2">
                <button
                  onClick={() =>
                    handleCopy(activeTab === "resume" ? result.tailored_resume : result.cover_letter)
                  }
                  className="rounded bg-white px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
                >
                  {copied ? "Copied!" : "Copy"}
                </button>
                <button
                  onClick={() =>
                    handleDownload(
                      activeTab === "resume" ? result.tailored_resume : result.cover_letter,
                      activeTab === "resume"
                        ? `resume_${company || "tailored"}.txt`
                        : `cover_letter_${company || "tailored"}.txt`
                    )
                  }
                  className="rounded bg-white px-2 py-1 text-xs font-medium text-green-600 hover:bg-green-50"
                >
                  Download
                </button>
              </div>
            </div>
            <div className="mt-3 whitespace-pre-wrap text-sm text-gray-800">
              {activeTab === "resume" ? result.tailored_resume : result.cover_letter}
            </div>
          </div>

          <button
            onClick={() => setResult(null)}
            className="w-full rounded-lg border border-gray-200 px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50"
          >
            Start Over
          </button>
        </>
      )}
    </div>
  );
}
