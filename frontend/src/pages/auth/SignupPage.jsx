import { useEffect, useState } from "react";
import { ArrowLeft, ArrowRight, AtSign, Eye, EyeOff, UserRound } from "lucide-react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import Button from "../../components/ui/Button";
import FormField from "../../components/ui/FormField";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import AuthLayout from "../../layouts/AuthLayout";

export default function SignupPage() {
  const { role } = useParams();
  const isHr = role === "hr";
  const { signup, isAuthenticated } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [values, setValues] = useState({
    fullname: "",
    username: "",
    email: "",
    password: "",
  });

  useEffect(() => {
    document.title = `${isHr ? "HR" : "Candidate"} sign up · NexHire`;
  }, [isHr]);

  if (!["candidate", "hr"].includes(role)) return <Navigate to="/login" replace />;
  if (isAuthenticated) return <Navigate to={`/${role}/dashboard`} replace />;

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const session = await signup(role, values);
      showToast("Your NexHire account is ready.", "success");
      navigate(`/${session.role}/dashboard`, { replace: true });
    } catch (error) {
      showToast(error.message, "error", "Account not created");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout role={role}>
      <div className="auth-card signup-form">
        <Link className="back-link" to="/login">
          <ArrowLeft size={16} /> Back to sign in
        </Link>
        <div className="auth-header">
          <span className="eyebrow">{isHr ? "People team account" : "Candidate account"}</span>
          <h2>{isHr ? "Create your hiring workspace" : "Create your profile"}</h2>
          <p>
            {isHr
              ? "HR access is available to pre-approved company emails."
              : "A few details and you’ll be ready to explore opportunities."}
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-cols two-cols">
            <FormField label="Full name">
              <div className="input-box">
                <UserRound size={18} />
                <input
                  placeholder="Your full name"
                  value={values.fullname}
                  onChange={(event) =>
                    setValues({ ...values, fullname: event.target.value })
                  }
                  required
                />
              </div>
            </FormField>
            <FormField label="Username">
              <div className="input-box">
                <AtSign size={18} />
                <input
                  placeholder="Choose a username"
                  value={values.username}
                  onChange={(event) =>
                    setValues({ ...values, username: event.target.value })
                  }
                  required
                />
              </div>
            </FormField>
          </div>
          <FormField label={isHr ? "Approved work email" : "Email address"}>
            <div className="input-box">
              <AtSign size={18} />
              <input
                type="email"
                autoComplete="email"
                placeholder={isHr ? "you@company.com" : "you@example.com"}
                value={values.email}
                onChange={(event) =>
                  setValues({ ...values, email: event.target.value })
                }
                required
              />
            </div>
          </FormField>
          <FormField label="Password" hint="At least 6 characters">
            <div className="input-box">
              <input
                type={showPassword ? "text" : "password"}
                autoComplete="new-password"
                placeholder="Create a secure password"
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

          <label className="terms-check">
            <input type="checkbox" required />
            <span>I agree to the Terms of Service and Privacy Policy.</span>
          </label>
          <Button type="submit" loading={loading} icon={ArrowRight}>
            Create {isHr ? "HR" : "candidate"} account
          </Button>
        </form>
      </div>
    </AuthLayout>
  );
}
