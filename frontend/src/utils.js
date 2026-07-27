export const SKILL_OPTIONS = [
  "JavaScript", "TypeScript", "React", "Node.js", "Python", "FastAPI",
  "Django", "Java", "C#", "AWS", "Docker", "MongoDB", "PostgreSQL",
  "Figma", "Product Management", "Data Analysis",
];

export const JOB_TYPES = ["Full Time", "Part Time", "Internship", "Contract"];

export const APPLICATION_STAGES = [
  "Applied", "In Process", "Interview Scheduled", "Hired",
];

export const STATUS_META = {
  Applied: { label: "Applied", tone: "blue", step: 0 },
  "In Process": { label: "Assessment", tone: "yellow", step: 1 },
  "Interview Scheduled": { label: "Interview", tone: "purple", step: 2 },
  Hired: { label: "Hired", tone: "green", step: 3 },
  Rejected: { label: "Not selected", tone: "red", step: -1 },
};

export function formatCurrency(value) {
  if (value === null || value === undefined || value === "") return "Not listed";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

export function formatDate(value, options = {}) {
  if (!value) return "Not set";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Not set";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    ...options,
  }).format(date);
}

export function getInitials(name = "") {
  return (
    name.trim().split(/\s+/).slice(0, 2).map((part) => part[0]).join("").toUpperCase()
    || "NH"
  );
}

export function decodeToken(token) {
  try {
    const payload = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(decodeURIComponent(escape(atob(payload))));
  } catch {
    return {};
  }
}

export function getId(item) {
  return item?._id || item?.id || item?.job_id || "";
}

export function getCandidateName(application) {
  return (
    application?.candidate?.fullname ||
    application?.candidate?.username ||
    application?.parsed_resume?.name ||
    "Candidate"
  );
}
