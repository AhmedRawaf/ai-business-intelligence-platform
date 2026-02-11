import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { useLang } from "@/context/LangContext";
import { t } from "@/lib/i18n";

export function LoginPage() {
  const { login } = useAuth();
  const { lang } = useLang();
  const navigate = useNavigate();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin12345");
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    try {
      await login(username, password);
      navigate("/");
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-md space-y-3">
        <h1 className="text-2xl font-bold">{t("login", lang)}</h1>
        <input
          className="w-full border p-2 rounded"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          placeholder={t("username", lang)}
        />
        <input
          className="w-full border p-2 rounded"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder={t("password", lang)}
        />
        {error ? <p className="text-red-600 text-sm">{error}</p> : null}
        <button className="w-full bg-slate-900 text-white p-2 rounded">{t("login", lang)}</button>
      </form>
    </div>
  );
}
