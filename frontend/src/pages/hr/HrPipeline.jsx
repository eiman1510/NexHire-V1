import { createElement, useState } from "react";
import {
  CalendarCheck2,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Search,
  UserRound,
  UsersRound,
  XCircle,
} from "lucide-react";
import CandidateModal from "../../components/hr/CandidateModal";
import PipelineActionModal from "../../components/hr/PipelineActionModal";
import Button from "../../components/ui/Button";
import EmptyState from "../../components/ui/EmptyState";
import PageHeader from "../../components/ui/PageHeader";
import Skeleton from "../../components/ui/Skeleton";
import StatusBadge from "../../components/ui/StatusBadge";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import useHrWorkspace from "../../hooks/useHrWorkspace";
import { getCandidateName } from "../../utils";
import { rejectApplication } from "../../services/api";

const filters = [
  { value: "", label: "All active", icon: UsersRound },
  { value: "Applied", label: "Needs review", icon: UserRound },
  { value: "In Process", label: "Assessment done", icon: ClipboardCheck },
  { value: "Interview Scheduled", label: "Interview", icon: CalendarCheck2 },
  { value: "Hired", label: "Hired", icon: CheckCircle2 },
];

export default function HrPipeline() {
  const { token } = useAuth();
  const { showToast } = useToast();
  const { apps, loading, refresh } = useHrWorkspace();
  const [filter, setFilter] = useState("");
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const [action, setAction] = useState(null);
  const [rejecting, setRejecting] = useState(false);

  const activeApps = apps.filter((item) => item.status !== "Rejected");
  const shownApps = activeApps.filter((application) => {
    const matchesFilter = !filter || application.status === filter;
    const query = search.toLowerCase();
    const matchesSearch =
      getCandidateName(application).toLowerCase().includes(query) ||
      application.job?.title?.toLowerCase().includes(query);
    return matchesFilter && matchesSearch;
  });

  function nextAction(status) {
    if (status === "Applied") return "assessment";
    if (status === "In Process") return "interview";
    if (status === "Interview Scheduled") return "hire";
    return null;
  }

  function actionLabel(status) {
    if (status === "Applied") return "Set assessment";
    if (status === "In Process") return "Schedule interview";
    if (status === "Interview Scheduled") return "Hire candidate";
    return "Hired";
  }

  async function handleReject(application) {
    if (!window.confirm(`Reject ${getCandidateName(application)}?`)) return;
    setRejecting(true);
    try {
      const response = await rejectApplication(token, application._id);
      showToast(response.message, "success");
      setSelected(null);
      refresh();
    } catch (error) {
      showToast(error.message, "error", "Application not rejected");
    } finally {
      setRejecting(false);
    }
  }

  return (
    <>
      <PageHeader
        eyebrow="Hiring pipeline"
        title="Move the right people forward."
        description="A stage-based view that keeps assessment, interview, and hiring in order."
      />

      <section className="pipe-tools">
        <div className="pipe-tabs">
          {filters.map(({ value, label, icon: Icon }) => (
            <button
              type="button"
              key={label}
              className={filter === value ? "active" : ""}
              onClick={() => setFilter(value)}
            >
              {createElement(Icon, { size: 16 })}
              {label}
              <span>{value ? activeApps.filter((item) => item.status === value).length : activeApps.length}</span>
            </button>
          ))}
        </div>
        <div className="search">
          <Search size={18} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search candidate or role"
          />
        </div>
      </section>

      <section className="table-box">
        {loading ? (
          <Skeleton count={5} className="pipe-row" />
        ) : shownApps.length ? (
          <div className="pipe-table">
            <div className="table-head">
              <span>Candidate</span><span>Role</span><span>Stage</span><span>Next action</span><span />
            </div>
            {shownApps.map((application) => {
              const availableAction = nextAction(application.status);
              return (
                <article className="pipe-row" key={application._id}>
                  <div className="pipe-person">
                    <span><UserRound size={18} /></span>
                    <div><strong>{getCandidateName(application)}</strong><small>{application.candidate?.email}</small></div>
                  </div>
                  <div><strong>{application.job?.title || "Role"}</strong><small>{application.job?.job_type}</small></div>
                  <StatusBadge status={application.status} />
                  <div className="row-action">
                    <Button
                      size="sm"
                      variant={availableAction ? "secondary" : "ghost"}
                      disabled={!availableAction}
                      onClick={() => {
                        setSelected(application);
                        setAction(availableAction);
                      }}
                    >
                      {actionLabel(application.status)}
                    </Button>
                  </div>
                  <button className="icon-btn" onClick={() => setSelected(application)} aria-label="View candidate">
                    <ChevronRight size={19} />
                  </button>
                </article>
              );
            })}
          </div>
        ) : (
          <EmptyState
            icon={UsersRound}
            title="No candidates in this view"
            description="Choose another stage or adjust your search."
          />
        )}
      </section>

      <CandidateModal
        application={selected && !action ? selected : null}
        onClose={() => setSelected(null)}
        showActions={false}
      />
      {selected && !action && selected.status !== "Hired" && (
        <div className="bottom-actions">
          <Button variant="danger" icon={XCircle} loading={rejecting} onClick={() => handleReject(selected)}>
            Reject candidate
          </Button>
          {nextAction(selected.status) && (
            <Button
              onClick={() => setAction(nextAction(selected.status))}
            >
              {actionLabel(selected.status)}
            </Button>
          )}
        </div>
      )}
      <PipelineActionModal
        application={selected}
        action={action}
        onClose={() => {
          setAction(null);
          setSelected(null);
        }}
        onSaved={refresh}
      />
    </>
  );
}
