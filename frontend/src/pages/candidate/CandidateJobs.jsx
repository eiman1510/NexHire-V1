import { useCallback, useEffect, useState } from "react";
import {
  ArrowRight,
  Briefcase,
  Filter,
  RotateCcw,
  Search,
  SlidersHorizontal,
  WalletCards,
} from "lucide-react";
import Button from "../../components/ui/Button";
import EmptyState from "../../components/ui/EmptyState";
import FormField from "../../components/ui/FormField";
import PageHeader from "../../components/ui/PageHeader";
import Skeleton from "../../components/ui/Skeleton";
import JobDetailsDrawer from "../../components/candidate/JobDetailsDrawer";
import { useAuth } from "../../context/AuthContext";
import { useToast } from "../../context/ToastContext";
import { JOB_TYPES, formatCurrency } from "../../utils";
import { applyToJob, getJobs } from "../../services/api";

const emptyFilters = { min_sal: "", experience: "", job_type: "" };

export default function CandidateJobs() {
  const { token } = useAuth();
  const { showToast } = useToast();
  const [jobs, setJobs] = useState([]);
  const [filters, setFilters] = useState(emptyFilters);
  const [search, setSearch] = useState("");
  const [selectedJob, setSelectedJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);

  const loadJobs = useCallback(async (newFilters = {}) => {
    setLoading(true);
    try {
      setJobs(await getJobs(newFilters));
    } catch (error) {
      showToast(error.message, "error", "Jobs not loaded");
    } finally {
      setLoading(false);
    }
  }, [showToast]);

  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  async function handleApply(jobId) {
    setApplying(true);
    try {
      const response = await applyToJob(token, jobId);
      showToast(response.message || "Application submitted.", "success");
      setSelectedJob(null);
    } catch (error) {
      const type = error.status === 201 || error.status === 202 ? "warning" : "error";
      showToast(error.message, type, "Application update");
    } finally {
      setApplying(false);
    }
  }

  function resetFilters() {
    setFilters(emptyFilters);
    loadJobs();
  }

  const shownJobs = jobs.filter((job) =>
    job.title?.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <>
      <PageHeader
        eyebrow="Opportunity board"
        title="Find work worth doing."
        description="Explore open roles, understand the fit, and apply with confidence."
      />

      <section className="job-filters">
        <div className="search">
          <Search size={18} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search by job title"
            aria-label="Search jobs"
          />
        </div>
        <form
          className="filters"
          onSubmit={(event) => {
            event.preventDefault();
            loadJobs(filters);
          }}
        >
          <FormField label="Minimum salary">
            <input
              type="number"
              min="0"
              placeholder="Any"
              value={filters.min_sal}
              onChange={(event) =>
                setFilters({ ...filters, min_sal: event.target.value })
              }
            />
          </FormField>
          <FormField label="Your experience">
            <input
              type="number"
              min="0"
              placeholder="Years"
              value={filters.experience}
              onChange={(event) =>
                setFilters({ ...filters, experience: event.target.value })
              }
            />
          </FormField>
          <FormField label="Job type">
            <select
              value={filters.job_type}
              onChange={(event) =>
                setFilters({ ...filters, job_type: event.target.value })
              }
            >
              <option value="">All types</option>
              {JOB_TYPES.map((type) => <option key={type}>{type}</option>)}
            </select>
          </FormField>
          <Button type="submit" size="sm" icon={Filter}>Filter</Button>
          <Button type="button" size="sm" variant="ghost" icon={RotateCcw} onClick={resetFilters}>
            Reset
          </Button>
        </form>
      </section>

      <div className="job-count">
        <span><SlidersHorizontal size={16} /> {shownJobs.length} opportunities</span>
        <small>Updated from the NexHire job board</small>
      </div>

      <section className="job-list">
        {loading ? (
          <Skeleton count={6} className="job-card" />
        ) : shownJobs.length ? (
          shownJobs.map((job, index) => (
            <article className="job-card" key={job._id || `${job.title}-${index}`}>
              <div className={`job-icon job-color-${(index % 4) + 1}`}>
                <Briefcase size={22} />
              </div>
              <span className={`status status-${job.status === "Open" ? "green" : "gray"}`}>
                <i /> {job.status || "Open"}
              </span>
              <div className="job-info">
                <small>{job.job_type || "Opportunity"}</small>
                <h3>{job.title}</h3>
              </div>
              <div className="job-pay">
                <WalletCards size={17} />
                <strong>{formatCurrency(job.pay)}</strong>
                <span>annual</span>
              </div>
              <button className="job-link" type="button" onClick={() => setSelectedJob(job)}>
                View details <ArrowRight size={17} />
              </button>
            </article>
          ))
        ) : (
          <EmptyState
            icon={Briefcase}
            title="No roles match just yet"
            description="Try widening your filters or check back as new opportunities arrive."
            action={<Button variant="secondary" onClick={resetFilters}>Clear filters</Button>}
          />
        )}
      </section>

      <JobDetailsDrawer
        job={selectedJob}
        onClose={() => setSelectedJob(null)}
        onApply={handleApply}
        applying={applying}
      />
    </>
  );
}
