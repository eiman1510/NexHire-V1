import { ArrowUpRight, CheckCircle2, Sparkles } from "lucide-react";
import Logo from "../components/brand/Logo";

export default function AuthLayout({ children, role = "candidate" }) {
  const isHr = role === "hr";
  return (
    <main className="auth-page">
      <section className="auth-panel">
        <div className="auth-orb auth-orb-one" />
        <div className="auth-orb auth-orb-two" />
        <Logo />
        <div className="auth-hero">
          <span className="auth-kicker">
            <Sparkles size={15} /> Hiring, made more human
          </span>
          <h1>
            {isHr ? "Build teams with clarity." : "Your next chapter starts here."}
          </h1>
          <p>
            {isHr
              ? "Create roles, review talent, and keep every candidate moving with a calmer hiring workspace."
              : "Discover thoughtful opportunities and follow every application from first click to final decision."}
          </p>
          <div className="auth-benefits">
            <span><CheckCircle2 size={17} /> One clear workspace</span>
            <span><CheckCircle2 size={17} /> Meaningful progress updates</span>
            <span><CheckCircle2 size={17} /> Secure, focused experience</span>
          </div>
        </div>
        <div className="auth-quote">
          <div className="mini-avatars"><i>AL</i><i>MS</i><i>RK</i></div>
          <p>“A hiring flow that finally feels as thoughtful as the people in it.”</p>
          <ArrowUpRight size={19} />
        </div>
      </section>
      <section className="auth-content">{children}</section>
    </main>
  );
}
