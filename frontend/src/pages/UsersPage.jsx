import { useEffect, useState } from "react";
import { createUser, deleteUser, listUsers, updateUserPut } from "../api/users";
import ErrorBanner from "../components/ErrorBanner";
import UserForm from "../components/UserForm";
import UsersTable from "../components/UsersTable";

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [editing, setEditing] = useState(null);
  const [busyId, setBusyId] = useState(null);

  async function refresh() {
    setError("");
    setLoading(true);
    try {
      setUsers(await listUsers());
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleCreate(payload) {
    setError("");
    try {
      await createUser(payload);
      await refresh();
    } catch (e) {
      setError(String(e.message || e));
    }
  }

  async function handleEditSave(payload) {
    setError("");
    if (!editing) return;

    setBusyId(editing.id);
    try {
      await updateUserPut(editing.id, payload);
      setEditing(null);
      await refresh();
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setBusyId(null);
    }
  }

  async function handleDelete(u) {
    const ok = confirm(`Delete ${u.first_name} ${u.last_name}?`);
    if (!ok) return;

    setError("");
    setBusyId(u.id);
    try {
      await deleteUser(u.id);
      if (editing && editing.id === u.id) setEditing(null);
      await refresh();
    } catch (e) {
      setError(String(e.message || e));
    } finally {
      setBusyId(null);
    }
  }

  return (
    <div className="container">
      <h1>Conference Attendees</h1>

      <div className="toolbar">
        <button onClick={refresh} disabled={loading}>
          {loading ? "Loading..." : "Refresh"}
        </button>
      </div>

      <ErrorBanner message={error} />

      {editing ? (
      <UserForm
        mode="edit"
        initialUser={editing}
        busy={busyId === editing.id}
        onSubmit={handleEditSave}
        onCancel={() => setEditing(null)}
      />
        ) : (
          <UserForm
            mode="create"
            initialUser={null}
            busy={false}
            onSubmit={handleCreate}
          />
        )}

      <UsersTable users={users} onEdit={setEditing} onDelete={handleDelete} busyId={busyId} />
    </div>
  );
}