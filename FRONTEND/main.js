// ─── Shared Utilities ─────────────────────────────────────────────────────────

function showError(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.classList.remove("hidden");
}

function hideError(el) {
  if (!el) return;
  el.textContent = "";
  el.classList.add("hidden");
}

function showSuccess(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.classList.remove("hidden");
}

function setLoading(btn, loading, text) {
  if (!btn) return;
  btn.disabled = loading;
  btn.textContent = loading ? "Please wait..." : text;
}

function formatCurrency(n) {
  return "$" + Number(n).toLocaleString();
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function statusBadge(status) {
  const cls =
    status === "ACCEPTED"
      ? "badge-accepted"
      : status === "REJECTED"
        ? "badge-rejected"
        : "badge-pending";
  return `<span class="badge ${cls}">${status}</span>`;
}

function campaignCard(c) {
  const url = c.id ? `campaign.html?id=${c.id}` : "#";
  return `
    <a href="${url}" class="card campaign-card">
      <div class="campaign-card-header">
        <div class="campaign-title">${escapeHtml(c.title)}</div>
        <span class="budget-badge">${formatCurrency(c.budget)}</span>
      </div>
      <div class="brand-name">${escapeHtml(c.brand_name || "")}</div>
      <div class="campaign-desc">${escapeHtml(c.description || "")}</div>
      <div class="campaign-footer">
        <span>${c.application_count || 0} applicant${c.application_count !== 1 ? "s" : ""}</span>
        <span>${formatDate(c.created_at)}</span>
      </div>
    </a>`;
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function buildNavbar(page) {
  const user = getUser();
  const links = {
    home: '<a href="/index.html">Home</a>',
    dashboard: user ? '<a href="/pages/dashboard.html">Dashboard</a>' : "",
    newCampaign:
      user && user.role === "BRAND"
        ? '<a href="/pages/campaign-new.html" class="btn btn-sm">+ New Campaign</a>'
        : "",
    auth: user
      ? `<span class="nav-user">${escapeHtml(user.name)} <span class="nav-role">${user.role}</span></span><button onclick="logout()" class="btn btn-outline btn-sm">Sign out</button>`
      : `<a href="/pages/login.html" class="btn btn-outline btn-sm">Sign in</a><a href="/pages/register.html" class="btn btn-sm">Join</a>`,
  };
  return `
    <nav class="navbar">
      <div class="nav-inner">
        <a href="/index.html" class="nav-brand"><span class="nav-logo">CC</span> Clout Consortium</a>
        <div class="nav-right">${links.dashboard}${links.newCampaign}${links.auth}</div>
      </div>
    </nav>`;
}
