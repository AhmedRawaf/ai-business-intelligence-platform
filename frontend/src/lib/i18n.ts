export type Lang = "ar" | "en";

type Dictionary = Record<string, { ar: string; en: string }>;

const dict: Dictionary = {
  login: { ar: "تسجيل الدخول", en: "Login" },
  username: { ar: "اسم المستخدم", en: "Username" },
  password: { ar: "كلمة المرور", en: "Password" },
  dashboard: { ar: "لوحة المؤشرات", en: "Dashboard" },
  documents: { ar: "المستندات", en: "Documents" },
  chat: { ar: "المساعد الذكي", en: "AI Assistant" },
  audit: { ar: "سجل التدقيق", en: "Audit Logs" },
  datasets: { ar: "البيانات", en: "Datasets" },
  logout: { ar: "تسجيل الخروج", en: "Logout" },
};

export const t = (key: string, lang: Lang): string => dict[key]?.[lang] || key;
