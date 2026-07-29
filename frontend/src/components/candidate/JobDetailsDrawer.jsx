import {
  Briefcase,
  CalendarDays,
  CheckCircle2,
  GraduationCap,
  Sparkles,
  WalletCards,
} from "lucide-react";
import Button from "../ui/Button";
import Drawer from "../ui/Drawer";
import { formatCurrency, formatDate, getId } from "../../utils";

export default function JobDetailsDrawer({
  job,
  onClose,
  onApply,
  applying,
}) {
  if (!job) return null;
  const isOpen = (job.status || "Open") === "Open";

  return (
    <Drawer
      open={Boolean(job)}
      onClose={onClose}
      title={job.title}
      subtitle={`${job.job_type || "Role"} · ${formatCurrency(job.pay)}`}
    >
      <div className="job-top">
        <span><Briefcase size={24} /></span>
        <div><small>Opportunity</small><strong>{job.title}</strong></div>
      </div>

      <div className="job-details">
        <div><WalletCards size={19} /><span>Compensation</span><strong>{formatCurrency(job.pay)}</strong></div>
        <div><Briefcase size={19} /><span>Experience</span><strong>{job.required_experience || 0}+ years</strong></div>
        <div><GraduationCap size={19} /><span>Education</span><strong>{job.minimum_education || "Not specified"}</strong></div>
        <div><CalendarDays size={19} /><span>Apply by</span><strong>{formatDate(job.last_date_to_apply)}</strong></div>
      </div>

      <section className="job-section">
        <h3>About the role</h3>
        <p>{job.description || "More information will be shared by the hiring team."}</p>
      </section>
      <section className="job-section">
        <h3><Sparkles size={18} /> Skills that matter</h3>
        <div className="tag-list">
          {job.skills_required?.length
            ? job.skills_required.map((skill) => <span key={skill}>{skill}</span>)
            : <small>No specific skills listed.</small>}
        </div>
      </section>
      <section className="ats-note">
        <CheckCircle2 size={20} />
        <div>
          <strong>Thoughtful matching</strong>
          <p>Your resume is securely evaluated by the backend before an application is created.</p>
        </div>
      </section>
      <footer className="drawer-foot">
        <Button
          onClick={() => onApply(getId(job))}
          loading={applying}
          disabled={!isOpen}
        >
          {isOpen ? "Apply for this role" : "Applications closed"}
        </Button>
      </footer>
    </Drawer>
  );
}
