const API_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export class ApiError extends Error {
  constructor(message, status = 500, data = null) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

function makeUrl(path, query = {}) {
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value !== "" && value !== undefined && value !== null) {
      params.set(key, value);
    }
  });

  const queryString = params.toString();
  const base = API_URL.endsWith("/") ? API_URL.slice(0, -1) : API_URL;
  return `${base}${path}${queryString ? `?${queryString}` : ""}`;
}

async function request(path, options = {}) {
  const { token, query, body, ...fetchOptions } = options;
  const headers = {};

  if (token) headers.Authorization = `Bearer ${token}`;
  if (body && !(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  let response;
  try {
    response = await fetch(makeUrl(path, query), {
      ...fetchOptions,
      headers,
      body: body instanceof FormData ? body : body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError("Cannot reach the server. Make sure FastAPI is running.", 0);
  }

  const result = await response.json();
  const status = Number(result.status_code || response.status);

  // The backend returns its real status inside the JSON response.
  if (!response.ok || status >= 400 || Number(result.error_code) === 1) {
    throw new ApiError(result.detail || result.message || "Request failed.", status, result.data);
  }

  return result;
}

// Authentication
export async function login(credentials) {
  const result = await request("/auth/login", { method: "POST", body: credentials });
  return {
    token: result.data.access_key,
    role: result.data.role.toLowerCase(),
  };
}

export async function signup(role, details) {
  const result = await request(`/auth/signup/${role}`, { method: "POST", body: details });
  return {
    token: result.data.access_token || result.data.access_key,
    role: (result.data.role || role).toLowerCase(),
  };
}

// Candidate profile and jobs
export async function getProfile(token) {
  const result = await request("/get_Profile_data", { token });
  return result.data;
}

export function saveProfile(token, values, isUpdate = false) {
  const form = new FormData();
  if (values.resume) form.append("resume", values.resume);
  if (values.experience !== undefined) form.append("experience", values.experience);
  if (values.skills) form.append("skills", values.skills.join(","));

  return request("/candidate/info", {
    method: isUpdate ? "PUT" : "POST",
    token,
    body: form,
  });
}

export async function getJobs(filters = {}) {
  const hasFilters = Object.values(filters).some((value) => value !== "");
  const result = await request(hasFilters ? "/get_filtered_job" : "/alljobs", {
    query: hasFilters ? filters : {},
  });
  return Array.isArray(result.data) ? result.data : [];
}

export function applyToJob(token, jobId) {
  return request(`/apply/${jobId}`, { method: "POST", token });
}

export async function getMyApplications(token, userId) {
  const result = await request(`/my_jobs/${userId || "me"}`, { token });
  return Array.isArray(result.data) ? result.data : [];
}

// HR jobs
export async function getCreatedJobs(token) {
  const result = await request("/my_created_jobs", { token });
  return Array.isArray(result.data) ? result.data : [];
}

export function createJob(token, job) {
  return request("/add_job", { method: "POST", token, body: job });
}

export function updateJob(token, jobId, updates) {
  return request("/update_job", {
    method: "PUT",
    token,
    query: { job_id: jobId, ...updates },
  });
}

export function deleteJob(token, jobId) {
  return request("/delete_job", {
    method: "DELETE",
    token,
    query: { jobId },
  });
}

export async function getJobApplications(jobId) {
  const result = await request(`/application/${jobId}`);
  return Array.isArray(result.data) ? result.data : [];
}

// HR application actions
export function rejectApplication(token, applicationId) {
  return request("/reject_application", {
    method: "POST",
    token,
    query: { job_id: applicationId },
  });
}

export function scheduleAssessment(token, applicationId, details) {
  return request("/initial_meeting", {
    method: "POST",
    token,
    query: {
      job_id: applicationId,
      interview_link: details.link,
      interview_date: details.date,
      interview_time: details.time,
    },
  });
}

export function scheduleInterview(token, applicationId, details) {
  return request("/schedule_interview", {
    method: "POST",
    token,
    query: {
      job_id: applicationId,
      interview_date: details.date,
      interview_time: details.time,
      stat: "Interview Scheduled",
    },
  });
}

export function hireCandidate(token, applicationId, details) {
  return request("/hiring_mail", {
    method: "POST",
    token,
    query: {
      job_id: applicationId,
      start: details.date,
      time: details.time,
      timings: details.timings,
      working_days: details.workingDays,
      pay: details.pay,
    },
  });
}

// Admin functions
export async function adminLogin(password) {
  const result = await request("/admin/admin_login", {
    method: "POST",
    body: { password },
  });
  return result.data;
}

export async function addHR(email) {
  const result = await request("/admin/add_hr", {
    method: "POST",
    body: { email },
  });
  return result.data;
}

export async function deleteHR(email) {
  const result = await request("/admin/delete_hr", {
    method: "DELETE",
    query: { email },
  });
  return result.data;
}

export async function getApprovedHRs() {
  const result = await request("/admin/app_hr");
  return Array.isArray(result.data) ? result.data : [];
}

export async function getRegisteredHRs() {
  const result = await request("/admin/get_registered_hrs");
  return Array.isArray(result.data) ? result.data : [];
}
