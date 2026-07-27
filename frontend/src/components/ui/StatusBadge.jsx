import { STATUS_META } from "../../utils";

export default function StatusBadge({ status }) {
  const meta = STATUS_META[status] || {
    label: status || "Unknown",
    tone: "gray",
  };
  return (
    <span className={`status status-${meta.tone}`}>
      <i />
      {meta.label}
    </span>
  );
}
