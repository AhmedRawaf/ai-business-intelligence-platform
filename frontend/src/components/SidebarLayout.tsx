import type { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { useLang } from "@/context/LangContext";
import { t } from "@/lib/i18n";

type Props = {
  children: ReactNode;
  organizationId: number | null;
  setOrganizationId: (id: number) => void;
};

export function SidebarLayout({ children, organizationId, setOrganizationId }: Props) {
  const { user, logout } = useAuth();
  const { lang, setLang } = useLang();
  const location = useLocation();

  const nav = [
    { to: "/", label: t("dashboard", lang) },
    { to: "/documents", label: t("documents", lang) },
    { to: "/chat", label: t("chat", lang) },
    { to: "/audit", label: t("audit", lang) },
  ];

  return (
    <div className="min-h-screen bg-slate-100 flex">
      <aside className="w-72 bg-slate-900 text-slate-100 p-4">
        <h1 className="text-lg font-bold mb-4">AI BI Platform</h1>
        <div className="mb-4">
          <label className="text-xs text-slate-300">{t("datasets", lang)}</label>
          <select
            className="w-full mt-1 p-2 rounded text-slate-900"
            value={organizationId ?? ""}
            onChange={(e) => setOrganizationId(Number(e.target.value))}
          >
            {user?.memberships.map((membership) => (
              <option value={membership.organization_id} key={membership.organization_id}>
                {membership.organization_name} ({membership.role})
              </option>
            ))}
          </select>
        </div>
        <nav className="space-y-1">
          {nav.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`block p-2 rounded ${location.pathname === item.to ? "bg-slate-700" : "hover:bg-slate-800"}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="mt-6 space-y-2">
          <button className="w-full bg-slate-700 p-2 rounded" onClick={() => setLang(lang === "ar" ? "en" : "ar")}>
            {lang === "ar" ? "English" : "العربية"}
          </button>
          <button className="w-full bg-rose-700 p-2 rounded" onClick={logout}>
            {t("logout", lang)}
          </button>
        </div>
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
