import { useEffect, useState } from "react";
import { CalendarCheck2, Send } from "lucide-react";
import Button from "../ui/Button";
import FormField from "../ui/FormField";
import Modal from "../ui/Modal";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import {
  hireCandidate,
  scheduleAssessment,
  scheduleInterview,
} from "../../services/api";
import { getCandidateName } from "../../utils";

function tomorrow() {
  const date = new Date();
  date.setDate(date.getDate() + 1);
  return date.toISOString().slice(0, 10);
}

export default function PipelineActionModal({
  application,
  action,
  onClose,
  onSaved,
}) {
  const { token } = useAuth();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [values, setValues] = useState({
    date: tomorrow(),
    time: "10:00",
    link: "",
    timings: "9:00 AM – 5:00 PM",
    workingDays: "Monday – Friday",
    pay: application?.job?.pay || "",
  });

  useEffect(() => {
    if (application) {
      setValues((current) => ({
        ...current,
        date: tomorrow(),
        pay: application.job?.pay || "",
      }));
    }
  }, [application]);

  if (!application || !action) return null;

  const copy = {
    assessment: {
      eyebrow: "First stage",
      title: "Schedule initial assessment",
      submit: "Send assessment",
    },
    interview: {
      eyebrow: "Next stage",
      title: "Schedule candidate interview",
      submit: "Send interview invite",
    },
    hire: {
      eyebrow: "Final stage",
      title: "Prepare hiring details",
      submit: "Hire candidate",
    },
  }[action];

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const applicationId = application._id;
      let response;
      if (action === "assessment") {
        response = await scheduleAssessment(token, applicationId, values);
      } else if (action === "interview") {
        response = await scheduleInterview(token, applicationId, values);
      } else {
        response = await hireCandidate(token, applicationId, values);
      }
      showToast(response.message, "success");
      await onSaved?.();
      onClose();
    } catch (error) {
      showToast(error.message, "error", "Stage not updated");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Modal
      open
      onClose={onClose}
      eyebrow={copy.eyebrow}
      title={copy.title}
    >
      <form className="stage-form" onSubmit={handleSubmit}>
        <div className="stage-person">
          <span><CalendarCheck2 size={21} /></span>
          <div><small>Candidate</small><strong>{getCandidateName(application)}</strong></div>
        </div>
        {action === "assessment" && (
          <FormField label="Assessment link">
            <input
              type="url"
              placeholder="https://assessment.example.com/…"
              value={values.link}
              onChange={(event) => setValues({ ...values, link: event.target.value })}
              required
            />
          </FormField>
        )}
        <div className="form-cols two-cols">
          <FormField label={action === "hire" ? "Joining date" : "Date"}>
            <input
              type="date"
              min={tomorrow()}
              value={values.date}
              onChange={(event) => setValues({ ...values, date: event.target.value })}
              required
            />
          </FormField>
          <FormField label="Time">
            <input
              type="time"
              value={values.time}
              onChange={(event) => setValues({ ...values, time: event.target.value })}
              required
            />
          </FormField>
        </div>
        {action === "hire" && (
          <>
            <div className="form-cols two-cols">
              <FormField label="Working hours">
                <input
                  value={values.timings}
                  onChange={(event) => setValues({ ...values, timings: event.target.value })}
                  required
                />
              </FormField>
              <FormField label="Working days">
                <input
                  value={values.workingDays}
                  onChange={(event) => setValues({ ...values, workingDays: event.target.value })}
                  required
                />
              </FormField>
            </div>
            <FormField label="Confirmed annual pay">
              <input
                type="number"
                min="1"
                value={values.pay}
                onChange={(event) => setValues({ ...values, pay: event.target.value })}
                required
              />
            </FormField>
          </>
        )}
        <div className="info-box">
          <Send size={18} />
          <p>NexHire will update the stage and send the relevant email notification.</p>
        </div>
        <footer className="modal-actions">
          <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
          <Button type="submit" loading={loading}>{copy.submit}</Button>
        </footer>
      </form>
    </Modal>
  );
}
