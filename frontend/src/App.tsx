import { useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { SidebarLayout } from "@/components/SidebarLayout";
import { LoginPage } from "@/pages/LoginPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { DocumentsPage } from "@/pages/DocumentsPage";
import { ChatPage } from "@/pages/ChatPage";
import { AuditPage } from "@/pages/AuditPage";

function AppShell() {
  const { user } = useAuth();
  const [organizationId, setOrganizationId] = useState<number | null>(null);

  useEffect(() => {
    if (!organizationId && user?.memberships?.length) {
      setOrganizationId(user.memberships[0].organization_id);
    }
  }, [user, organizationId]);

  if (!organizationId) {
    return <div className="p-8">No organization membership found.</div>;
  }

  return (
    <SidebarLayout organizationId={organizationId} setOrganizationId={setOrganizationId}>
      <Routes>
        <Route path="/" element={<DashboardPage organizationId={organizationId} />} />
        <Route path="/documents" element={<DocumentsPage organizationId={organizationId} />} />
        <Route path="/chat" element={<ChatPage organizationId={organizationId} />} />
        <Route path="/audit" element={<AuditPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </SidebarLayout>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
