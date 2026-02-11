import { useRef } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

type Props = {
  organizationId: number;
};

export function DocumentsPage({ organizationId }: Props) {
  const fileRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();

  const query = useQuery({
    queryKey: ["documents", organizationId],
    queryFn: async () => {
      const response = await api.get(`/documents?organization=${organizationId}`);
      return response.data;
    },
    enabled: Boolean(organizationId),
    refetchInterval: 6000,
  });

  const upload = useMutation({
    mutationFn: async (file: File) => {
      const form = new FormData();
      form.append("organization", String(organizationId));
      form.append("file", file);
      await api.post("/documents", form, { headers: { "Content-Type": "multipart/form-data" } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents", organizationId] });
    },
  });

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded shadow flex justify-between">
        <h2 className="text-xl font-semibold">Documents</h2>
        <div>
          <input
            ref={fileRef}
            className="hidden"
            type="file"
            accept=".pdf,.docx,.csv,.xlsx"
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) upload.mutate(file);
            }}
          />
          <button className="bg-slate-900 text-white px-4 py-2 rounded" onClick={() => fileRef.current?.click()}>
            Upload
          </button>
        </div>
      </div>
      <div className="bg-white p-4 rounded shadow overflow-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="p-2">Name</th>
              <th className="p-2">Type</th>
              <th className="p-2">Status</th>
              <th className="p-2">Created</th>
              <th className="p-2">Error</th>
            </tr>
          </thead>
          <tbody>
            {(query.data ?? []).map((doc: any) => (
              <tr key={doc.id} className="border-b">
                <td className="p-2">{doc.name}</td>
                <td className="p-2">{doc.content_type}</td>
                <td className="p-2">{doc.status}</td>
                <td className="p-2">{new Date(doc.created_at).toLocaleString()}</td>
                <td className="p-2 text-red-600">{doc.error_message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
