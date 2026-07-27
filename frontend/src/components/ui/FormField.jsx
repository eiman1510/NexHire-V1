export default function FormField({
  label,
  hint,
  error,
  children,
  className = "",
}) {
  return (
    <label className={`field ${className}`}>
      <span className="field-label">
        {label}
        {hint && <small>{hint}</small>}
      </span>
      {children}
      {error && <span className="field-error">{error}</span>}
    </label>
  );
}
