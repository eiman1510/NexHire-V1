import { useEffect, useState } from "react";
import {
  ArrowRight,
  BriefcaseBusiness,
  CircleDot,
  Clock3,
  Plus,
  UsersRound,
} from "lucide-react";
import { Link } from "react-router-dom";
import Button from "../../components/ui/Button";
import PageHeader from "../../components/ui/PageHeader";
import Skeleton from "../../components/ui/Skeleton";
import JobFormModal from "../../components/hr/JobFormModal";
import { useAuth } from "../../context/AuthContext";
import { formatDate } from "../../utils";
import { getProfile } from "../../services/api";
import useHrWorkspace from "../../hooks/useHrWorkspace";

export default function HrDashboard() {
  const { token } = useAuth();
  const { jobs, apps, loading, refresh } = useHrWorkspace();
  const [profile, setProfile] = useState(null);
  const [createOpen, setCreateOpen] = useState(false);

  useEffect(() => {
    getProfile(token).then(setProfile).catch(() => {});
  }, [token]);

  const firstName = profile?.fullname?.split(" ")[0] || profile?.username || "there";
  const activeJobs = jobs.filter((job) => job.status === "Open").length;
  const progressing = apps.filter(
    (application) => !["Applied", "Rejected"].includes(application.status),
  ).length;

  return (
    <>
      <PageHeader
        eyebrow="People team Dashboard"
        title={`Welcome back, ${firstName}.`}
        description="Your hiring work, distilled into the decisions that matter."
        actions={<Button icon={Plus} onClick={() => setCreateOpen(true)}>Create job</Button>}
      />

      <section className="stats">
        {loading ? (
          <Skeleton count={3} className="stat-card" />
        ) : (
          <>
            <article className="stat-card stat-purple">
              <span className="stat-icon"><BriefcaseBusiness size={20} /></span>
              <div><strong>{jobs.length}</strong><span>Total jobs created</span></div>
              <small>{activeJobs} currently open</small>
            </article>
            <article className="stat-card stat-orange">
              <span className="stat-icon"><UsersRound size={20} /></span>
              <div><strong>{apps.length}</strong><span>Applications received</span></div>
              <small>Across all your roles</small>
            </article>
            <article className="stat-card stat-green">
              <span className="stat-icon"><CircleDot size={20} /></span>
              <div><strong>{progressing}</strong><span>In process</span></div>
              <small>Moving through your pipeline</small>
            </article>
          </>
        )}
      </section>

      <section className="dashboard-grid hr-grid">
        <article className="panel recent-jobs">
          <header className="panel-head">
            <div><span className="eyebrow">Recent activity</span><h3>Your latest roles</h3></div>
            <Link to="/hr/jobs">View all <ArrowRight size={16} /></Link>
          </header>
          {loading ? <Skeleton count={3} /> : jobs.length ? (
            <div className="compact-list">
              {jobs.slice(0, 4).map((job) => (
                <div key={job._id}>
                  <span className="list-icon"><BriefcaseBusiness size={18} /></span>
                  <div><strong>{job.title}</strong><small>Created {formatDate(job.created_at)}</small></div>
                  <span className={`status status-${job.status === "Open" ? "green" : "gray"}`}><i />{job.status}</span>
                </div>
              ))}
            </div>
          ) : <p className="panel-empty">Create your first role to begin building a pipeline.</p>}
        </article>
        <article className="panel pipe-box">
          <span className="eyebrow">Pipeline health</span>
          <h3>Make every next step visible.</h3>
          <p>Review candidates by stage and keep promising people moving.</p>
          <div className="pipe-counts">
            <div><span><Clock3 size={16} /> Awaiting review</span><strong>{apps.filter((a) => a.status === "Applied").length}</strong></div>
            <div><span><CircleDot size={16} /> Assessment</span><strong>{apps.filter((a) => a.status === "In Process").length}</strong></div>
            <div><span><UsersRound size={16} /> Interview</span><strong>{apps.filter((a) => a.status === "Interview Scheduled").length}</strong></div>
          </div>
          <Link to="/hr/pipeline">Open hiring pipeline <ArrowRight size={16} /></Link>
        </article>
      </section>

      <JobFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSaved={refresh}
      />
    </>
  );
}
