import { useEffect, useState } from "react";
import { CalendarDays, Plus, Save } from "lucide-react";
import Button from "../ui/Button";
import FormField from "../ui/FormField";
import Modal from "../ui/Modal";
import { JOB_TYPES, SKILL_OPTIONS } from "../../utils";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import { createJob, updateJob } from "../../services/api";

function futureDate(days = 14) {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return date.toISOString().slice(0, 16);
}

const defaults = {
  title: "",
  description: "",
  last_date_to_apply: futureDate(),
  skills_required: [],
  required_experience: 0,
  minimum_education: "Bachelor's degree",
  threshold: 70,
  job_type: "Full Time",
  status: "Open",
  pay: "",
};

export default function JobFormModal({ open, onClose, job, onSaved }) {
  const { token, userId } = useAuth();
  const { showToast } = useToast();
  const [values, setValues] = useState(defaults);
  const [loading, setLoading] = useState(false);
  const isEdit = Boolean(job);

  useEffect(() => {
    if (!open) return;
    setValues(
      job
        ? {
            ...defaults,
            ...job,
            last_date_to_apply: job.last_date_to_apply
              ? new Date(job.last_date_to_apply).toISOString().slice(0, 16)
              : futureDate(),
          }
        : { ...defaults, last_date_to_apply: futureDate() },
    );
  }, [open, job]);

  function toggleSkill(skill) {
    setValues((current) => ({
      ...current,
      skills_required: current.skills_required.includes(skill)
        ? current.skills_required.filter((item) => item !== skill)
        : [...current.skills_required, skill],
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      let response;
      if (isEdit) {
        const updates = {};
        if (values.last_date_to_apply !== job.last_date_to_apply) {
          updates.last_date_to_apply = new Date(values.last_date_to_apply).toISOString();
        }
        if (values.status !== job.status) updates.status = values.status;
        if (Number(values.threshold) !== Number(job.threshold)) {
          updates.threshold = Number(values.threshold);
        }
        response = await updateJob(token, job._id, updates);
      } else {
        response = await createJob(token, {
          ...values,
          pay: Number(values.pay),
          threshold: Number(values.threshold),
          required_experience: Number(values.required_experience),
          last_date_to_apply: new Date(values.last_date_to_apply).toISOString(),
          created_at: new Date().toISOString(),
          created_by: userId || "",
        });
      }
      showToast(response.message, "success");
      await onSaved?.();
      onClose();
    } catch (error) {
      showToast(error.message, "error", "Job not saved");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={isEdit ? "Edit job availability" : "Create a new role"}
      eyebrow={isEdit ? "Keep the listing current" : "Add to your job board"}
      size="lg"
    >
      <form className="job-form" onSubmit={handleSubmit}>
        {isEdit ? (
          <>
            <div className="info-box">
              <CalendarDays size={19} />
              <p>Update the role status, application deadline, and ATS threshold whenever the hiring plan changes.</p>
            </div>
            <div className="form-cols three-cols">
              <FormField label="Job status">
                <select
                  value={values.status}
                  onChange={(event) => setValues({ ...values, status: event.target.value })}
                >
                  <option>Open</option><option>Paused</option><option>Closed</option>
                </select>
              </FormField>
              <FormField label="ATS threshold" hint="0–100">
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={values.threshold}
                  onChange={(event) => setValues({ ...values, threshold: event.target.value })}
                  required
                />
              </FormField>
              <FormField label="Application deadline">
                <input
                  type="datetime-local"
                  value={values.last_date_to_apply}
                  onChange={(event) =>
                    setValues({ ...values, last_date_to_apply: event.target.value })
                  }
                  required
                />
              </FormField>
            </div>
          </>
        ) : (
          <>
            <FormField label="Job title">
              <input
                value={values.title}
                onChange={(event) => setValues({ ...values, title: event.target.value })}
                placeholder="e.g. Senior Product Designer"
                required
              />
            </FormField>
            <FormField label="Role description">
              <textarea
                value={values.description}
                onChange={(event) => setValues({ ...values, description: event.target.value })}
                placeholder="Describe the role, impact, and the person who will thrive here…"
                rows="5"
                required
              />
            </FormField>
            <div className="form-cols three-cols">
              <FormField label="Job type">
                <select
                  value={values.job_type}
                  onChange={(event) => setValues({ ...values, job_type: event.target.value })}
                >
                  {JOB_TYPES.map((type) => <option key={type}>{type}</option>)}
                </select>
              </FormField>
              <FormField label="Annual pay">
                <input
                  type="number"
                  min="1"
                  value={values.pay}
                  onChange={(event) => setValues({ ...values, pay: event.target.value })}
                  placeholder="85000"
                  required
                />
              </FormField>
              <FormField label="Experience required">
                <input
                  type="number"
                  min="0"
                  value={values.required_experience}
                  onChange={(event) =>
                    setValues({ ...values, required_experience: event.target.value })
                  }
                  required
                />
              </FormField>
            </div>
            <div className="form-cols three-cols">
              <FormField label="Minimum education">
                <input
                  value={values.minimum_education}
                  onChange={(event) =>
                    setValues({ ...values, minimum_education: event.target.value })
                  }
                  required
                />
              </FormField>
              <FormField label="ATS threshold" hint="0–100">
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={values.threshold}
                  onChange={(event) => setValues({ ...values, threshold: event.target.value })}
                  required
                />
              </FormField>
              <FormField label="Apply by">
                <input
                  type="datetime-local"
                  value={values.last_date_to_apply}
                  onChange={(event) =>
                    setValues({ ...values, last_date_to_apply: event.target.value })
                  }
                  required
                />
              </FormField>
            </div>
            <FormField label="Required skills" hint={`${values.skills_required.length} selected`}>
              <div className="skills small-skills">
                {SKILL_OPTIONS.map((skill) => (
                  <button
                    type="button"
                    key={skill}
                    className={values.skills_required.includes(skill) ? "skill-btn skill-active" : "skill-btn"}
                    onClick={() => toggleSkill(skill)}
                  >
                    {values.skills_required.includes(skill) ? "✓" : <Plus size={13} />} {skill}
                  </button>
                ))}
              </div>
            </FormField>
          </>
        )}
        <footer className="modal-actions">
          <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
          <Button type="submit" icon={Save} loading={loading}>
            {isEdit ? "Save changes" : "Publish role"}
          </Button>
        </footer>
      </form>
    </Modal>
  );
}
