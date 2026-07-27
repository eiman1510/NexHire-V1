export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  icon: Icon,
  className = "",
  disabled,
  ...props
}) {
  return (
    <button
      className={`btn btn-${variant} btn-${size} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <span className="spinner" /> : Icon ? <Icon size={17} /> : null}
      <span>{loading ? "Please wait…" : children}</span>
    </button>
  );
}
