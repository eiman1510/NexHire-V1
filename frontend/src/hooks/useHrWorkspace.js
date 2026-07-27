import { useCallback, useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getCreatedJobs, getJobApplications } from "../services/api";

export default function useHrWorkspace() {
  const { token } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const createdJobs = await getCreatedJobs(token);
      setJobs(createdJobs);
      const appGroups = await Promise.all(
        createdJobs.map(async (job) => {
          const items = await getJobApplications(job._id);
          return items.map((application) => ({ ...application, job }));
        }),
      );
      setApps(appGroups.flat());
    } catch (requestError) {
      setError(requestError);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { jobs, apps, loading, error, refresh };
}
