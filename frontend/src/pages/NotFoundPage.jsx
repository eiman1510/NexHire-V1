import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import Logo from "../components/brand/Logo";

export default function NotFoundPage() {
  return (
    <main className="not-found">
      <Logo />
      <span>404</span>
      <h1>This page took another career path.</h1>
      <p>The page you’re looking for doesn’t exist or has been moved.</p>
      <Link className="btn btn-primary btn-md" to="/login">
        <ArrowLeft size={17} /> Back to NexHire
      </Link>
    </main>
  );
}
