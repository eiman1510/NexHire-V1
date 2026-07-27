import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import AppShell from "./layouts/AppShell";
import LoginPage from "./pages/auth/LoginPage";
import SignupPage from "./pages/auth/SignupPage";
// import CandidateDashboard from "./pages/candidate/CandidateDashboard";
// import CandidateJobs from "./pages/candidate/CandidateJobs";
// import CandidateApplications from "./pages/candidate/CandidateApplications";
import HrDashboard from "./pages/hr/HrDashboard";
import HrJobs from "./pages/hr/HrJobs";
import HrPipeline from "./pages/hr/HrPipeline";
import NotFoundPage from "./pages/NotFoundPage";
import FullPageLoader from "./components/ui/FullPageLoader";

function ProtectedRoute({ role, children }) {
  const { isAuthenticated, role: userRole, isRestoring } = useAuth();

  if (isRestoring) return <FullPageLoader />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (role && userRole !== role) {
    return <Navigate to={`/${userRole}/dashboard`} replace />;
  }
  return children;
}

function HomeRedirect() {
  const { isAuthenticated, role, isRestoring } = useAuth();
  if (isRestoring) return <FullPageLoader />;
  return (
    <Navigate
      to={isAuthenticated ? `/${role}/dashboard` : "/login"}
      replace
    />
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup/:role" element={<SignupPage />} />

      {/* <Route
        path="/candidate"
        element={
          <ProtectedRoute role="candidate">
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<CandidateDashboard />} />
        <Route path="jobs" element={<CandidateJobs />} />
        <Route path="applications" element={<CandidateApplications />} />
      </Route> */}

      <Route
        path="/hr"
        element={
          <ProtectedRoute role="hr">
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="dashboard" replace />} />
        <Route path="dashboard" element={<HrDashboard />} />
        <Route path="jobs" element={<HrJobs />} />
        <Route path="pipeline" element={<HrPipeline />} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
