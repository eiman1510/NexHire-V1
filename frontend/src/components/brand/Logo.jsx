import { Sparkles } from "lucide-react";

export default function Logo({ compact = false }) {
  return (
    <div className="logo" aria-label="NexHire">
      <span className="logo-icon">
        <Sparkles size={19} strokeWidth={2.4} />
      </span>
      {!compact && (
        <span className="logo-text">
          Nex<span>Hire</span>
        </span>
      )}
    </div>
  );
}
