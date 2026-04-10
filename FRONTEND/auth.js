// ─── Auth helpers ────────────────────────────────────────────────────────────

function getToken() {
  return localStorage.getItem("token");
}

function getUser() {
  const raw = localStorage.getItem("user");
  try {
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function setSession(token, user) {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}

function requireAuth(redirectTo) {
  if (!getToken()) {
    window.location.href = redirectTo || "/pages/login.html";
    return false;
  }
  return true;
}

function requireRole(role, redirectTo) {
  const user = getUser();
  if (!user || user.role !== role) {
    window.location.href = redirectTo || "/index.html";
    return false;
  }
  return true;
}

function logout() {
  clearSession();
  window.location.href = "/index.html";
}
