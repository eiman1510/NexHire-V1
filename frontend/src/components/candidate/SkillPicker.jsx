import { Check, Plus } from "lucide-react";
import { SKILL_OPTIONS } from "../../utils";

export default function SkillPicker({ value, onChange }) {
  function toggle(skill) {
    onChange(
      value.includes(skill)
        ? value.filter((item) => item !== skill)
        : [...value, skill],
    );
  }

  return (
    <div className="skills">
      {SKILL_OPTIONS.map((skill) => {
        const selected = value.includes(skill);
        return (
          <button
            type="button"
            className={selected ? "skill-btn skill-active" : "skill-btn"}
            onClick={() => toggle(skill)}
            key={skill}
          >
            {selected ? <Check size={14} /> : <Plus size={14} />}
            {skill}
          </button>
        );
      })}
    </div>
  );
}
