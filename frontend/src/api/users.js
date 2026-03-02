const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function parseError(res) {
  let detail = `HTTP ${res.status}`;
  try {
    const data = await res.json();
    if (data && data.detail) detail = data.detail;
  } catch (_) {}
  return detail;
}

export async function listUsers() {
  const res = await fetch(`${API_BASE}/users`);
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function createUser(payload) {
  const res = await fetch(`${API_BASE}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function updateUserPut(id, payload) {
  const res = await fetch(`${API_BASE}/users/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function deleteUser(id) {
  const res = await fetch(`${API_BASE}/users/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(await parseError(res));
}