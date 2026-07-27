import { createElement, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
  BriefcaseBusiness,
  ChevronDown,
  ClipboardList,
  LayoutDashboard,
  LogOut,
  Menu,
  Search,
  UsersRound,
  X,
} from "lucide-react";
import Logo from "../components/brand/Logo";
import { useAuth } from "../context/AuthContext";
import { getInitials } from "../utils";

const candidateNav = [
  { to: "/candidate/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/candidate/jobs", label: "Find jobs", icon: Search },
  {
    to: "/candidate/applications",
    label: "My applications",
    icon: ClipboardList,
  },
];

const hrNav = [
  { to: "/hr/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/hr/jobs", label: "Manage jobs", icon: BriefcaseBusiness },
  { to: "/hr/pipeline", label: "Hiring pipeline", icon: UsersRound },
];

export default function AppShell() {
  const { role, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const nav = role === "hr" ? hrNav : candidateNav;
  const currentPage = nav.find((item) => location.pathname.startsWith(item.to));
  const roleName = role === "hr" ? "People team" : "Candidate";

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${menuOpen ? "side-open" : ""}`}>
        <div className="side-top">
          <Logo />
          <button
            className="icon-btn side-close"
            type="button"
            onClick={() => setMenuOpen(false)}
            aria-label="Close navigation"
          >
            <X size={20} />
          </button>
        </div>

        <div className="workspace">
          <span>{getInitials(roleName)}</span>
          <div>
            <strong>NexHire workspace</strong>
            <small>{roleName}</small>
          </div>
          <ChevronDown size={15} />
        </div>

        <nav className="side-nav" aria-label="Primary navigation">
          <span className="nav-label">Workspace</span>
          {nav.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setMenuOpen(false)}
              className={({ isActive }) =>
                `nav-link ${isActive ? "nav-active" : ""}`
              }
            >
              {createElement(Icon, { size: 19 })}
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="side-tip">
          <span>Good to know</span>
          <strong>
            {role === "hr"
              ? "Thoughtful hiring starts with clear next steps."
              : "Complete profiles make stronger first impressions."}
          </strong>
          <div className="mini-avatars">
            <i>NS</i>
            <i>JR</i>
            <i>+8</i>
          </div>
        </div>

        <button className="logout-btn" type="button" onClick={handleLogout}>
          <LogOut size={18} />
          Log out
        </button>
      </aside>

      {menuOpen && (
        <button
          className="side-bg"
          aria-label="Close navigation"
          onClick={() => setMenuOpen(false)}
        />
      )}

      <div className="main">
        <header className="topbar">
          <button
            className="icon-btn menu-btn"
            type="button"
            onClick={() => setMenuOpen(true)}
            aria-label="Open navigation"
          >
            <Menu size={21} />
          </button>
          <div>
            <small>{roleName} workspace</small>
            <strong>{currentPage?.label || "NexHire"}</strong>
          </div>
          <span className="top-avatar">{getInitials(roleName)}</span>
        </header>
        <main className="page">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
