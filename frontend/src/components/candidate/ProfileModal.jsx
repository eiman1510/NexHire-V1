import { createElement, useEffect, useState } from "react";
import { Briefcase, FileText, Save, Sparkles } from "lucide-react";
import Button from "../ui/Button";
import FormField from "../ui/FormField";
import Modal from "../ui/Modal";
import SkillPicker from "./SkillPicker";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import { saveProfile } from "../../services/api";

const updateOptions = [
  { key: "resume", label: "Resume", icon: FileText },
  { key: "experience", label: "Experience", icon: Briefcase },
  { key: "skills", label: "Skills", icon: Sparkles },
];

export default function ProfileModal({
  open,
  onClose,
  mode = "submit",
  profile,
  onSaved,
}) {
  const { token } = useAuth();
  const { showToast } = useToast();
  const [selectedFields, setSelectedFields] = useState([]);
  const [resume, setResume] = useState(null);
  const [experience, setExperience] = useState(profile?.experience ?? 0);
  const [skills, setSkills] = useState(profile?.skills || []);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) {
      setResume(null);
      setExperience(profile?.experience ?? 0);
      setSkills(profile?.skills || []);
      setSelectedFields([]);
    }
  }, [open, profile]);

  const isUpdate = mode === "update";
  const shouldShow = (field) => !isUpdate || selectedFields.includes(field);

  function toggleField(field) {
    setSelectedFields((current) =>
      current.includes(field)
        ? current.filter((item) => item !== field)
        : [...current, field],
    );
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (isUpdate && selectedFields.length === 0) {
      showToast("Choose at least one profile detail to update.", "warning");
      return;
    }
    if (!isUpdate && !resume) {
      showToast("Please attach your resume to complete your profile.", "warning");
      return;
    }

    setLoading(true);
    try {
      const values = {};
      if (shouldShow("resume") && resume) values.resume = resume;
      if (shouldShow("experience")) values.experience = Number(experience);
      if (shouldShow("skills")) values.skills = skills;
      const response = await saveProfile(token, values, isUpdate);
      showToast(response.message || "Your profile has been saved.", "success");
      await onSaved?.();
      onClose();
    } catch (error) {
      showToast(error.message, "error", "Profile not saved");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={isUpdate ? "Update your profile" : "Complete your profile"}
      eyebrow={isUpdate ? "Keep things current" : "Stand out to teams"}
      size="lg"
    >
      <form className="profile-form" onSubmit={handleSubmit}>
        {isUpdate && (
          <div className="update-options">
            <p>What would you like to update?</p>
            <div>
              {updateOptions.map(({ key, label, icon: Icon }) => (
                <button
                  type="button"
                  key={key}
                  onClick={() => toggleField(key)}
                  className={selectedFields.includes(key) ? "selected" : ""}
                >
                  {createElement(Icon, { size: 18 })}
                  <span>{label}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {shouldShow("resume") && (
          <FormField label="Resume" hint="PDF or DOCX, up to 10 MB">
            <label className="file-drop">
              <FileText size={24} />
              <div>
                <strong>{resume ? resume.name : "Choose your latest resume"}</strong>
                <span>
                  {resume
                    ? `${(resume.size / 1024 / 1024).toFixed(2)} MB selected`
                    : "Click to browse from your device"}
                </span>
              </div>
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={(event) => setResume(event.target.files?.[0] || null)}
                required={!isUpdate}
              />
            </label>
          </FormField>
        )}

        {shouldShow("experience") && (
          <FormField label="Years of experience">
            <div className="experience-box">
              <input
                type="range"
                min="0"
                max="30"
                value={experience}
                onChange={(event) => setExperience(event.target.value)}
              />
              <strong>{experience} {Number(experience) === 1 ? "year" : "years"}</strong>
            </div>
          </FormField>
        )}

        {shouldShow("skills") && (
          <FormField label="Core skills" hint={`${skills.length} selected`}>
            <SkillPicker value={skills} onChange={setSkills} />
          </FormField>
        )}

        <footer className="modal-actions">
          <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
          <Button type="submit" icon={Save} loading={loading}>
            {isUpdate ? "Save updates" : "Complete profile"}
          </Button>
        </footer>
      </form>
    </Modal>
  );
}
