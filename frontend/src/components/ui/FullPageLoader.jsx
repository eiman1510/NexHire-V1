import Logo from "../brand/Logo";

export default function FullPageLoader() {
  return (
    <div className="page-loader">
      <Logo />
      <span className="loading-dots" aria-label="Loading">
        <i />
        <i />
        <i />
      </span>
    </div>
  );
}
