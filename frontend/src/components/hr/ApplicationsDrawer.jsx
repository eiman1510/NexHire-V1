import { ArrowRight, Inbox, UserRound } from "lucide-react";
import Drawer from "../ui/Drawer";
import EmptyState from "../ui/EmptyState";
import StatusBadge from "../ui/StatusBadge";
import { getCandidateName } from "../../utils";

export default function ApplicationsDrawer({
  job,
  applications,
  onClose,
  onSelect,
}) {
  return (
    <Drawer
      open={Boolean(job)}
      onClose={onClose}
      title={`${job?.title || "Job"} applications`}
      subtitle={`${applications.length} candidate${applications.length === 1 ? "" : "s"} received`}
    >
      <div className="people-list">
        {applications.length ? (
          applications.map((application) => (
            <button
              type="button"
              key={application._id}
              className="candidate-row"
              onClick={() => onSelect(application)}
            >
              <span className="person-icon"><UserRound size={20} /></span>
              <div>
                <strong>{getCandidateName(application)}</strong>
                <small>{application.candidate?.email || "Candidate profile"}</small>
              </div>
              <StatusBadge status={application.status} />
              <ArrowRight size={17} />
            </button>
          ))
        ) : (
          <EmptyState
            icon={Inbox}
            title="No applications yet"
            description="New candidates will appear here as they apply."
          />
        )}
      </div>
    </Drawer>
  );
}
