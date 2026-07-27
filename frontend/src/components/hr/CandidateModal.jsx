import {
  BriefcaseBusiness,
  FileText,
  Mail,
  Sparkles,
  UserRound,
} from "lucide-react";
import Button from "../ui/Button";
import Modal from "../ui/Modal";
import StatusBadge from "../ui/StatusBadge";
import { getCandidateName } from "../../utils";

export default function CandidateModal({
  application,
  onClose,
  onReject,
  onProceed,
  loading,
  showActions = true,
}) {
  if (!application) return null;
  const candidate = application.candidate || {};
  const parsed = application.parsed_resume || {};
  const skills = candidate.skills || parsed.skills || [];

  return (
    <Modal
      open={Boolean(application)}
      onClose={onClose}
      title={getCandidateName(application)}
      eyebrow={`Applicant for ${application.job?.title || "this role"}`}
      size="lg"
    >
      <div className="person-details">
        <header>
          <span><UserRound size={27} /></span>
          <div>
            <h3>{getCandidateName(application)}</h3>
            <p>{candidate.email || parsed.email || "Email not available"}</p>
          </div>
          <StatusBadge status={application.status} />
        </header>
        <div className="person-facts">
          <div><Mail size={18} /><span>Contact</span><strong>{candidate.email || "Not listed"}</strong></div>
          <div><BriefcaseBusiness size={18} /><span>Experience</span><strong>{candidate.experience ?? parsed.experience ?? 0} years</strong></div>
          <div><FileText size={18} /><span>Resume</span><strong>{candidate.resume_key ? "Available" : "Parsed on application"}</strong></div>
        </div>
        <section>
          <h4><Sparkles size={17} /> Candidate skills</h4>
          <div className="tag-list">
            {skills.length
              ? skills.map((skill) => <span key={skill}>{skill}</span>)
              : <small>No skills were found in this profile.</small>}
          </div>
        </section>
        {parsed.summary && (
          <section><h4>Resume summary</h4><p>{parsed.summary}</p></section>
        )}
      </div>
      {showActions && (
        <footer className="modal-actions split-actions">
          <Button variant="danger" onClick={onReject} disabled={loading}>Reject application</Button>
          <Button onClick={onProceed} loading={loading}>Proceed to assessment</Button>
        </footer>
      )}
    </Modal>
  );
}
