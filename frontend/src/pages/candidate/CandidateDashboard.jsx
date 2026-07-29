import { useCallback, useEffect, useState } from "react";
import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  FilePenLine,
  FilePlus2,
  Mail,
  Sparkles,
  UserRound,
} from "lucide-react";
import { Link } from "react-router-dom";
import Button from "../../components/ui/Button";
import PageHeader from "../../components/ui/PageHeader";
import ProfileModal from "../../components/candidate/ProfileModal";
import Skeleton from "../../components/ui/Skeleton";
import { useAuth } from "../../context/AuthContext";
import { getInitials } from "../../utils";
import { getMyApplications, getProfile } from "../../services/api";

export default function CandidateDashboard() {
  const { token, userId } = useAuth();
  const [profile, setProfile] = useState(null);
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [profileModal, setProfileModal] = useState(null);

  const loadData = useCallback(async () => {
    const [profileData, appData] = await Promise.allSettled([
      getProfile(token),
      getMyApplications(token, userId),
    ]);
    if (profileData.status === "fulfilled") setProfile(profileData.value);
    if (appData.status === "fulfilled") {
      setApps(appData.value);
    }
    setLoading(false);
  }, [token, userId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const hasProfile = Boolean(profile?.resume_key);
  const firstName =
    profile?.fullname?.split(" ")[0] || profile?.username || "there";

  return (
    <>
      <PageHeader
        eyebrow="Candidate overview"
        title={`Good to see you, ${firstName}.`}
        description="Here’s a calm, clear view of your job search today."
      />

      <section className="welcome-box">
        <div className="welcome-info">
          <span className="welcome-icon"><Sparkles size={21} /></span>
          <div>
            <span className="eyebrow">Your next move</span>
            <h2>
              {hasProfile
                ? "Your profile is ready to make an impression."
                : "A complete profile opens the right doors."}
            </h2>
            <p>
              {hasProfile
                ? "Keep your experience and skills current, then explore roles selected for ambitious people."
                : "Add your resume, experience, and core skills before applying to opportunities."}
            </p>
          </div>
        </div>
        <div className="welcome-btns">
          {!hasProfile && (
            <Button icon={FilePlus2} onClick={() => setProfileModal("submit")}>
              Submit profile
            </Button>
          )}
          <Button
            variant={hasProfile ? "primary" : "secondary"}
            icon={FilePenLine}
            onClick={() => setProfileModal("update")}
            disabled={!profile}
          >
            Update profile
          </Button>
        </div>
      </section>

      <section className="stats candidate-stats">
        {loading ? (
          <Skeleton count={3} className="stat-card" />
        ) : (
          <>
            <article className="stat-card stat-purple">
              <span className="stat-icon"><BriefcaseBusiness size={20} /></span>
              <div><strong>{apps.length}</strong><span>Jobs applied</span></div>
              <small>Across your active search</small>
            </article>
            <article className="stat-card stat-green">
              <span className="stat-icon"><CheckCircle2 size={20} /></span>
              <div><strong>{profile?.skills?.length || 0}</strong><span>Skills added</span></div>
              <small>Helping teams understand you</small>
            </article>
            <article className="stat-card stat-orange">
              <span className="stat-icon"><UserRound size={20} /></span>
              <div><strong>{hasProfile ? "Ready" : "Pending"}</strong><span>Profile status</span></div>
              <small>{hasProfile ? "You can apply to roles" : "Resume still needed"}</small>
            </article>
          </>
        )}
      </section>

      <section className="dashboard-grid">
        <article className="panel profile-card">
          <header className="panel-head">
            <div><span className="eyebrow">About you</span><h3>Profile details</h3></div>
            <span className={`profile-state ${hasProfile ? "complete" : ""}`}>
              {hasProfile ? "Complete" : "Needs attention"}
            </span>
          </header>
          {loading ? (
            <Skeleton count={1} />
          ) : (
            <>
              <div className="profile-person">
                <span>{getInitials(profile?.fullname || profile?.username)}</span>
                <div>
                  <strong>{profile?.fullname || "Your name"}</strong>
                  <small>@{profile?.username || "username"}</small>
                </div>
              </div>
              <div className="details">
                <div><Mail size={17} /><span>Email</span><strong>{profile?.email || "—"}</strong></div>
                <div><BriefcaseBusiness size={17} /><span>Experience</span><strong>{profile?.experience ?? 0} years</strong></div>
                <div><FilePlus2 size={17} /><span>Resume</span><strong>{hasProfile ? "Uploaded" : "Not uploaded"}</strong></div>
              </div>
              <div className="profile-tags">
                <span>Top skills</span>
                <div>
                  {profile?.skills?.length
                    ? profile.skills.map((skill) => <i key={skill}>{skill}</i>)
                    : <small>Add skills to help match your profile.</small>}
                </div>
              </div>
            </>
          )}
        </article>

        <article className="panel next-card">
          <span className="eyebrow">Keep moving</span>
          <h3>Find a role that feels like progress.</h3>
          <p>Browse open opportunities, compare details, and apply when the fit feels right.</p>
          <Link to="/candidate/jobs">
            Explore open roles <ArrowRight size={17} />
          </Link>
          <div className="next-art">
            <i /><i /><i /><span><BriefcaseBusiness size={27} /></span>
          </div>
        </article>
      </section>

      <ProfileModal
        open={Boolean(profileModal)}
        mode={profileModal}
        profile={profile}
        onClose={() => setProfileModal(null)}
        onSaved={loadData}
      />
    </>
  );
}
