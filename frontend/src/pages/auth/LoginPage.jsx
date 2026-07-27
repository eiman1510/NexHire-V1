import { useEffect, useState } from "react";
import { ArrowRight, Eye, EyeOff, LockKeyhole, Mail } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import Button from "../../components/ui/Button";
import FormField from "../../components/ui/FormField";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import AuthLayout from "../../layouts/AuthLayout";

export default function LoginPage() {
  const { login, isAuthenticated, role } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [values, setValues] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated && role) {
      navigate(`/${role}/dashboard`, { replace: true });
    }
  }, [isAuthenticated, role, navigate]);

  // Centralized login executor used by both standard form and guest buttons
  async function executeLogin(credentials, isGuest = false) {
    setLoading(true);
    try {
      const session = await login(credentials);
      const message = isGuest
        ? `Signed in as guest ${session.role}.`
        : "Welcome back. Your workspace is ready.";
      
      showToast(message, "success");
      navigate(`/${session.role}/dashboard`, { replace: true });
    } catch (error) {
      showToast(error.message || "Couldn’t sign you in", "error");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    executeLogin(values);
  }

  function handleGuestLogin(email, password) {
    executeLogin({ email, password }, true);
  }

  return (
    <AuthLayout>
      <div className="auth-card">
        <div className="auth-header">
          <span className="eyebrow">Welcome back</span>
          <h2>Sign in to NexHire</h2>
          <p>Continue to your candidate or people team workspace.</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <FormField label="Work email">
            <div className="input-box">
              <Mail size={18} />
              <input
                type="email"
                autoComplete="email"
                placeholder="you@company.com"
                value={values.email}
                onChange={(event) =>
                  setValues({ ...values, email: event.target.value })
                }
                required
              />
            </div>
          </FormField>

          <FormField label="Password">
            <div className="input-box">
              <LockKeyhole size={18} />
              <input
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                placeholder="Enter your password"
                minLength={6}
                value={values.password}
                onChange={(event) =>
                  setValues({ ...values, password: event.target.value })
                }
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword((current) => !current)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </FormField>

          <div className="form-options">
            <label>
              <input type="checkbox" /> Keep me signed in
            </label>
            <span>Secure login</span>
          </div>

          <Button type="submit" loading={loading} icon={ArrowRight}>
            Sign in
          </Button>
        </form>

        <div className="auth-divider">
          <span>New to NexHire?</span>
        </div>
        
        <div className="signup-options">
          <Link to="/signup/candidate">
            I’m a candidate <ArrowRight size={16} />
          </Link>
          <Link to="/signup/hr">
            I’m hiring <ArrowRight size={16} />
          </Link>
        </div>

        <div className="guest-login">
          <div className="auth-divider guest-divider">
            <span>Enter as guest</span>
          </div>

          <div className="guest-actions">
            <button
              type="button"
              className="guest-action"
              onClick={() => handleGuestLogin("hr@example.com", "hr12345")}
              disabled={loading}
            >
              <span>HR</span>
              <strong>→</strong>
            </button>

            <button
              type="button"
              className="guest-action"
              onClick={() => handleGuestLogin("candidate@example.com", "cand12345")}
              disabled={loading}
            >
              <span>Candidate</span>
              <strong>→</strong>
            </button>
          </div>
        </div>
      </div>
    </AuthLayout>
  );
}