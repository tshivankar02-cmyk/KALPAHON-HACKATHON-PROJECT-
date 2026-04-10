// ─── API Client ───────────────────────────────────────────────────────────────

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) headers["Authorization"] = "Bearer " + token;

  const res = await fetch(BASE_URL + path, { ...options, headers });

  if (res.status === 401) {
    clearSession();
    window.location.href = "/pages/login.html";
    return;
  }

  let data;
  try {
    data = await res.json();
  } catch {
    data = {};
  }

  if (!res.ok) {
    const msg = data.message || "Something went wrong";
    throw new Error(msg);
  }
  return data;
}

// Auth
const api = {
  register: (body) =>
    apiFetch("/auth/register", { method: "POST", body: JSON.stringify(body) }),
  login: (body) =>
    apiFetch("/auth/login", { method: "POST", body: JSON.stringify(body) }),
  me: () => apiFetch("/users/me"),

  // Campaigns
  campaigns: () => apiFetch("/campaigns"),
  campaignStats: () => apiFetch("/campaigns/stats"),
  campaign: (id) => apiFetch("/campaigns/" + id),
  createCampaign: (body) =>
    apiFetch("/campaigns", { method: "POST", body: JSON.stringify(body) }),
  deleteCampaign: (id) => apiFetch("/campaigns/" + id, { method: "DELETE" }),

  // Applications
  apply: (body) =>
    apiFetch("/applications", { method: "POST", body: JSON.stringify(body) }),
  myApplications: () => apiFetch("/applications/my"),
  updateStatus: (id, status) =>
    apiFetch("/applications/" + id + "/status", {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),
};
