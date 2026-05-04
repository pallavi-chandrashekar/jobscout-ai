"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";
import type { OutreachTemplate } from "@/lib/types";

export default function OutreachPage() {
  const [templates, setTemplates] = useState<OutreachTemplate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get<OutreachTemplate[]>("/outreach/templates");
        setTemplates(res.data);
      } catch (err) {
        console.error("Failed to fetch templates", err);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  const copyMessage = (msg: string) => {
    navigator.clipboard.writeText(msg);
  };

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Outreach Messages</h1>
        <p className="text-sm text-gray-500">
          Generate messages from any job detail page. Your history appears here.
        </p>
      </div>

      {loading ? (
        <div className="py-12 text-center text-gray-500">Loading...</div>
      ) : templates.length === 0 ? (
        <div className="py-12 text-center text-gray-500">
          No outreach messages yet. Go to a job posting and generate one.
        </div>
      ) : (
        <div className="space-y-4">
          {templates.map((t) => (
            <div key={t.id} className="rounded-lg border border-gray-200 bg-white p-4">
              <div className="flex items-center justify-between text-xs text-gray-500">
                <div className="flex gap-2">
                  {t.outreach_type && (
                    <span className="rounded bg-gray-100 px-2 py-0.5 capitalize">
                      {t.outreach_type.replace("_", " ")}
                    </span>
                  )}
                  {t.tone && (
                    <span className="rounded bg-gray-100 px-2 py-0.5 capitalize">{t.tone}</span>
                  )}
                  {t.provider && (
                    <span className="rounded bg-blue-50 px-2 py-0.5 text-blue-600">{t.provider}</span>
                  )}
                </div>
                <button
                  onClick={() => copyMessage(t.message)}
                  className="rounded bg-white px-2 py-1 text-xs font-medium text-blue-600 hover:bg-blue-50"
                >
                  Copy
                </button>
              </div>
              <div className="mt-2 whitespace-pre-wrap text-sm text-gray-800">{t.message}</div>
              {t.created_at && (
                <div className="mt-2 text-xs text-gray-400">
                  {new Date(t.created_at).toLocaleString()}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
