import { Check, X } from "lucide-react";
import { APPLICATION_STAGES, STATUS_META } from "../../utils";

export default function ApplicationTimeline({ status }) {
  const currentStep = STATUS_META[status]?.step ?? 0;
  const rejected = status === "Rejected";

  if (rejected) {
    return (
      <div className="timeline timeline-rejected">
        <span><X size={16} /></span>
        <div>
          <strong>Application closed</strong>
          <small>This role is no longer progressing.</small>
        </div>
      </div>
    );
  }

  return (
    <div className="timeline">
      {APPLICATION_STAGES.map((stage, index) => {
        const complete = index <= currentStep;
        return (
          <div className={`timeline-step ${complete ? "complete" : ""}`} key={stage}>
            <span>{index < currentStep ? <Check size={13} /> : index + 1}</span>
            <small>{STATUS_META[stage]?.label || stage}</small>
          </div>
        );
      })}
    </div>
  );
}
