import { FormEvent, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

type Props = {
  organizationId: number;
};

type AskResponse = {
  session_id: number;
  answer: string;
  citations: Array<{ document_name: string; snippet: string; page?: number }>;
};

export function ChatPage({ organizationId }: Props) {
  const [question, setQuestion] = useState("");
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [lastResponse, setLastResponse] = useState<AskResponse | null>(null);

  const sessions = useQuery({
    queryKey: ["chat_sessions", organizationId],
    queryFn: async () => {
      const response = await api.get(`/chat/sessions?organization=${organizationId}`);
      return response.data;
    },
    enabled: Boolean(organizationId),
  });

  const ask = useMutation({
    mutationFn: async () => {
      const response = await api.post("/chat/ask", {
        organization: organizationId,
        question,
        session_id: sessionId ?? undefined,
        language: "ar",
      });
      return response.data as AskResponse;
    },
    onSuccess: (data) => {
      setSessionId(data.session_id);
      setLastResponse(data);
      setQuestion("");
    },
  });

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!question.trim()) return;
    ask.mutate();
  };

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="bg-white rounded shadow p-4">
        <h3 className="font-semibold mb-2">Sessions</h3>
        <div className="space-y-1">
          {(sessions.data ?? []).map((item: any) => (
            <button
              key={item.id}
              onClick={() => setSessionId(item.id)}
              className={`w-full text-left p-2 rounded ${sessionId === item.id ? "bg-slate-200" : "hover:bg-slate-100"}`}
            >
              {item.title}
            </button>
          ))}
        </div>
      </div>

      <div className="col-span-2 bg-white rounded shadow p-4 space-y-4">
        <h2 className="text-xl font-semibold">AI Assistant (RAG)</h2>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            className="flex-1 border p-2 rounded"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="اسأل سؤالا عن بيانات أعمالك..."
          />
          <button className="bg-slate-900 text-white px-4 rounded" type="submit">
            Ask
          </button>
        </form>
        {lastResponse ? (
          <div className="space-y-4">
            <div className="bg-slate-50 border rounded p-3">
              <p className="font-semibold">Answer</p>
              <p>{lastResponse.answer}</p>
            </div>
            <div>
              <p className="font-semibold mb-2">Citations</p>
              <div className="space-y-2">
                {lastResponse.citations.map((citation, index) => (
                  <div className="border rounded p-2 bg-white" key={index}>
                    <div className="text-sm font-medium">{citation.document_name}</div>
                    <div className="text-xs text-slate-600">{citation.snippet}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
