import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function AuditPage() {
  const query = useQuery({
    queryKey: ["audit"],
    queryFn: async () => {
      const response = await api.get("/audit");
      return response.data;
    },
  });

  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-xl font-semibold mb-2">Audit Logs</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left">
            <th className="p-2">Time</th>
            <th className="p-2">Actor</th>
            <th className="p-2">Organization</th>
            <th className="p-2">Action</th>
            <th className="p-2">Target</th>
          </tr>
        </thead>
        <tbody>
          {(query.data ?? []).map((log: any) => (
            <tr className="border-b" key={log.id}>
              <td className="p-2">{new Date(log.created_at).toLocaleString()}</td>
              <td className="p-2">{log.actor_name}</td>
              <td className="p-2">{log.organization_name || "-"}</td>
              <td className="p-2">{log.action}</td>
              <td className="p-2">
                {log.target_type}:{log.target_id}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
