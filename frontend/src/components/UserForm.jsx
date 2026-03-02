import { useEffect, useState } from "react";

const empty = {
  first_name: "",
  last_name: "",
  email: "",
  age: 18,
  is_active: true,
};

export default function UserForm({ mode, initialUser, onSubmit, onCancel, busy }) {
  const [form, setForm] = useState(empty);

  useEffect(() => {
    if (initialUser) {
      setForm({
        first_name: initialUser.first_name || "",
        last_name: initialUser.last_name || "",
        email: initialUser.email || "",
        age: initialUser.age ?? 18,
        is_active: !!initialUser.is_active,
      });
    } else {
      setForm(empty);
    }
  }, [initialUser]);

  function setField(name, value) {
    setForm((f) => ({ ...f, [name]: value }));
  }

  function submit(e) {
    e.preventDefault();
    onSubmit({
      ...form,
      age: Number(form.age),
      email: String(form.email).trim(),
      first_name: String(form.first_name).trim(),
      last_name: String(form.last_name).trim(),
    });
  }

  return (
    <form onSubmit={submit} style={{ border: "1px solid #eee", borderRadius: 8, padding: 12, marginBottom: 12 }}>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <label>
          First name<br />
          <input
            value={form.first_name}
            onChange={(e) => setField("first_name", e.target.value)}
            required
          />
        </label>

        <label>
          Last name<br />
          <input
            value={form.last_name}
            onChange={(e) => setField("last_name", e.target.value)}
            required
          />
        </label>

        <label>
          Email<br />
          <input
            value={form.email}
            onChange={(e) => setField("email", e.target.value)}
            required
          />
        </label>

        <label>
          Age<br />
          <input
            type="number"
            value={form.age}
            onChange={(e) => setField("age", e.target.value)}
            required
            min="0"
            max="150"
            style={{ width: 90 }}
          />
        </label>

        <label style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 22 }}>
          <input
            type="checkbox"
            checked={form.is_active}
            onChange={(e) => setField("is_active", e.target.checked)}
          />
          Active
        </label>
      </div>

      <div className="toolbar" style={{ marginTop: 10 }}>
        <button type="submit" disabled={busy}>
          {mode === "edit" ? "Save" : "Add"}
        </button>
        {mode === "edit" ? (
          <button type="button" onClick={onCancel} disabled={busy}>
            Cancel
          </button>
        ) : null}
      </div>
    </form>
  );
}