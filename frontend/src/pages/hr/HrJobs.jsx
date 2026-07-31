import { useState } from "react";
import {
  BriefcaseBusiness,
  CalendarDays,
  Edit3,
  Eye,
  MoreHorizontal,
  Plus,
  Search,
  Trash2,
  UsersRound,
  WalletCards,
} from "lucide-react";
import ApplicationsDrawer from "../../components/hr/ApplicationsDrawer";
import CandidateModal from "../../components/hr/CandidateModal";
import JobFormModal from "../../components/hr/JobFormModal";
import PipelineActionModal from "../../components/hr/PipelineActionModal";
import Button from "../../components/ui/Button";
import EmptyState from "../../components/ui/EmptyState";
import PageHeader from "../../components/ui/PageHeader";
import Skeleton from "../../components/ui/Skeleton";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import useHrWorkspace from "../../hooks/useHrWorkspace";
import { formatCurrency, formatDate } from "../../utils";
import { deleteJob, rejectApplication } from "../../services/api";

export default function HrJobs() {
  const { token } = useAuth();
  const { showToast } = useToast();
  const { jobs, apps, loading, refresh } = useHrWorkspace();
  const [search, setSearch] = useState("");
  const [editJob, setEditJob] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [selectedApp, setSelectedApp] = useState(null);
  const [nextApp, setNextApp] = useState(null);
  const [saving, setSaving] = useState(false);

  const shownJobs = jobs.filter((job) =>
    job.title?.toLowerCase().includes(search.toLowerCase()),
  );
  const jobApps = apps.filter((item) => item.job_id === selectedJob?._id);

  function openCreate() {
    setEditJob(null);
    setShowForm(true);
  }

  function openEdit(job) {
    setEditJob(job);
    setShowForm(true);
  }

  async function handleDelete(job) {
    const confirmed = window.confirm(
      `Delete “${job.title}”? Jobs with applications will be closed instead.`,
    );
    if (!confirmed) return;
    try {
      const response = await deleteJob(token, job._id);
      showToast(response.message, "success");
      refresh();
    } catch (error) {
      showToast(error.message, "error", "Job not removed");
    }
  }

  async function handleReject() {
    if (!selectedApp) return;
    setSaving(true);
    try {
      const response = await rejectApplication(token, selectedApp._id);
      showToast(response.message, "success");
      setSelectedApp(null);
      await refresh();
    } catch (error) {
      showToast(error.message, "error", "Application not rejected");
    } finally {
      setSaving(false);
    }
  }

  return (
    <>
      <PageHeader
        eyebrow="Job management"
        title="Roles, candidates, momentum."
        description="Create clear opportunities and manage every role from one place."
        actions={<Button icon={Plus} onClick={openCreate}>Add job</Button>}
      />
      <div className="job-tools">
        <div className="search">
          <Search size={18} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search your jobs"
          />
        </div>
        <span>{jobs.length} total roles</span>
      </div>

      <section className="hr-jobs">
        {loading ? (
          <Skeleton count={4} className="hr-job" />
        ) : shownJobs.length ? (
          shownJobs.map((job) => {
            const count = apps.filter((item) => item.job_id === job._id).length;
            return (
              <article className="hr-job" key={job._id}>
                <header>
                  <span className="hr-job-icon"><BriefcaseBusiness size={21} /></span>
                  <div><small>{job.job_type}</small><h3>{job.title}</h3></div>
                  <span className={`status status-${job.status === "Open" ? "green" : "gray"}`}>
                    <i />{job.status}
                  </span>
                  {/* <button className="icon-btn" aria-label="More job options"><MoreHorizontal size={19} /></button> */}
                </header>
                <div className="hr-job-info">
                  <span>
                    <WalletCards size={16} style={{ color: "#22c55e" }} />{" "}
                    {formatCurrency(job.pay)}
                  </span>

                  <span>
                    <UsersRound size={16} style={{ color: "#ec4899" }} />{" "}
                    {count} applications
                  </span>

                  <span>
                    <CalendarDays size={16} style={{ color: "#f59e0b" }} />{" "}
                    Closes {formatDate(job.last_date_to_apply)}
                  </span>
                </div>
                <p style={{fontSize:12}}>{job.description}</p>
                <footer>
                  <Button size="sm" icon={Eye} onClick={() => setSelectedJob(job)}>
                    View applications
                  </Button>
                  <div>
                    <Button size="sm" variant="ghost" icon={Edit3} onClick={() => openEdit(job)}>Edit</Button>
                    <Button size="sm" variant="ghost-danger" icon={Trash2} onClick={() => handleDelete(job)}>Delete</Button>
                  </div>
                </footer>
              </article>
            );
          })
        ) : (
          <EmptyState
            icon={BriefcaseBusiness}
            title="No roles to show"
            description={search ? "Try another search." : "Create your first job and start meeting candidates."}
            action={!search && <Button icon={Plus} onClick={openCreate}>Create job</Button>}
          />
        )}
      </section>

      <JobFormModal
        open={showForm}
        job={editJob}
        onClose={() => setShowForm(false)}
        onSaved={refresh}
      />
      <ApplicationsDrawer
        job={selectedJob}
        applications={jobApps}
        onClose={() => setSelectedJob(null)}
        onSelect={(item) => setSelectedApp(item)}
      />
      <CandidateModal
        application={selectedApp}
        onClose={() => setSelectedApp(null)}
        onReject={handleReject}
        onProceed={() => {
          setNextApp(selectedApp);
          setSelectedApp(null);
        }}
        loading={saving}
        showActions={selectedApp?.status === "Applied"}
      />
      <PipelineActionModal
        application={nextApp}
        action="assessment"
        onClose={() => setNextApp(null)}
        onSaved={refresh}
      />
    </>
  );
}
