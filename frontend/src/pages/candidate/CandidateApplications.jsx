import { useCallback, useEffect, useState } from "react";
import { BriefcaseBusiness, CalendarDays, Search } from "lucide-react";
import ApplicationTimeline from "../../components/candidate/ApplicationTimeline";
import EmptyState from "../../components/ui/EmptyState";
import PageHeader from "../../components/ui/PageHeader";
import Skeleton from "../../components/ui/Skeleton";
import StatusBadge from "../../components/ui/StatusBadge";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import { formatCurrency, formatDate } from "../../utils";
import { getMyApplications } from "../../services/api";

export default function CandidateApplications() {
  const { token, userId } = useAuth();
  const { showToast } = useToast();
  const [apps, setApps] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);

  const loadApplications = useCallback(async () => {
    setLoading(true);
    try {
      setApps(await getMyApplications(token, userId));
    } catch (error) {
      showToast(error.message, "error", "Applications not loaded");
    } finally {
      setLoading(false);
    }
  }, [token, userId, showToast]);

  useEffect(() => {
    loadApplications();
  }, [loadApplications]);

  const shownApps = apps.filter((application) => {
    const matchesSearch = application.job?.title
      ?.toLowerCase()
      .includes(search.toLowerCase());
    return matchesSearch && (!status || application.status === status);
  });

  return (
    <>
      <PageHeader
        eyebrow="Application tracker"
        title="Every application, one clear view."
        description="Follow each opportunity from application to final decision."
      />

      <section className="app-tools">
        <div className="search">
          <Search size={18} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search your applications"
          />
        </div>
        <select value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">All stages</option>
          <option>Applied</option>
          <option>In Process</option>
          <option>Interview Scheduled</option>
          <option>Hired</option>
          <option>Rejected</option>
        </select>
      </section>

      <section className="app-list">
        {loading ? (
          <Skeleton count={4} className="app-card" />
        ) : shownApps.length ? (
          shownApps.map((application) => (
            <article className="app-card" key={application._id}>
              <header>
                <span className="app-icon"><BriefcaseBusiness size={21} /></span>
                <div>
                  <h3>{application.job?.title || "Job opportunity"}</h3>
                  <p>{application.job?.job_type || "Role"} · {formatCurrency(application.job?.pay)}</p>
                </div>
                <StatusBadge status={application.status} />
              </header>
              <div className="app-meta">
                <span><CalendarDays size={16} /> Applied {formatDate(application.applied_at)}</span>
                <span>Application #{application._id?.slice(-6).toUpperCase()}</span>
              </div>
              <ApplicationTimeline status={application.status} />
              {application.status === "Interview Scheduled" && application.interview?.date && (
                <div className="app-note">
                  <strong>Interview scheduled</strong>
                  <span>{formatDate(application.interview.date)} at {application.interview.time}</span>
                </div>
              )}
            </article>
          ))
        ) : (
          <EmptyState
            icon={BriefcaseBusiness}
            title="No applications here yet"
            description="When you apply to a role, its progress will appear here."
          />
        )}
      </section>
    </>
  );
}
