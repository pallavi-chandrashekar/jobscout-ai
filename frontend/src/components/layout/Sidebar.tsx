"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Job Feed", icon: "🔍" },
  { href: "/dashboard/applications", label: "My Applications", icon: "📋" },
  { href: "/dashboard/outreach", label: "Outreach", icon: "✉️" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-gray-200 bg-white">
      <div className="border-b border-gray-200 p-4">
        <h1 className="text-xl font-bold text-gray-900">JobScout AI</h1>
        <p className="text-xs text-gray-500">Find real jobs, skip the fakes</p>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors ${
                active
                  ? "bg-blue-50 font-medium text-blue-700"
                  : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-gray-200 p-4">
        <div className="text-sm font-medium text-gray-700">{user?.name || user?.email}</div>
        <button
          onClick={logout}
          className="mt-2 text-xs text-gray-500 hover:text-gray-700"
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}
