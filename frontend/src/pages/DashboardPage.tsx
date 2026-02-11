import { useRef } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Bar, BarChart, CartesianGrid, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "@/lib/api";

type Props = {
  organizationId: number;
};

export function DashboardPage({ organizationId }: Props) {
  const fileRef = useRef<HTMLInputElement>(null);
  const queryClient = useQueryClient();
  const analyticsQuery = useQuery({
    queryKey: ["analytics", organizationId],
    queryFn: async () => {
      const response = await api.get(`/kpi/analytics?organization=${organizationId}`);
      return response.data;
    },
    enabled: Boolean(organizationId),
  });

  const datasetMutation = useMutation({
    mutationFn: async (file: File) => {
      const form = new FormData();
      form.append("organization", String(organizationId));
      form.append("source_file", file);
      await api.post("/kpi/datasets", form, { headers: { "Content-Type": "multipart/form-data" } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["analytics", organizationId] });
    },
  });

  const data = analyticsQuery.data;

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded shadow flex items-center justify-between">
        <h2 className="text-xl font-semibold">KPI Dashboard</h2>
        <div>
          <input
            ref={fileRef}
            type="file"
            className="hidden"
            accept=".csv,.xlsx"
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) {
                datasetMutation.mutate(file);
              }
            }}
          />
          <button className="bg-slate-900 text-white px-4 py-2 rounded" onClick={() => fileRef.current?.click()}>
            Upload CSV/XLSX
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <div className="text-slate-500">Total Sales</div>
          <div className="text-2xl font-bold">{data?.summary?.total_sales ?? 0}</div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-slate-500">Records</div>
          <div className="text-2xl font-bold">{data?.summary?.records_count ?? 0}</div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-slate-500">Branches</div>
          <div className="text-2xl font-bold">{data?.summary?.branches_count ?? 0}</div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow h-72">
          <h3 className="font-semibold mb-2">Sales by Branch</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data?.sales_by_branch ?? []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#334155" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white p-4 rounded shadow h-72">
          <h3 className="font-semibold mb-2">Sales by Month</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data?.sales_by_month ?? []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line dataKey="value" stroke="#2563eb" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white p-4 rounded shadow h-72">
          <h3 className="font-semibold mb-2">Sales by Category</h3>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={data?.sales_by_category ?? []} dataKey="value" nameKey="name" outerRadius={90} fill="#14b8a6" />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
