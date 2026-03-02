export default function UsersTable({ users, onEdit, onDelete, busyId }) {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Age</th>
          <th>Active</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {users.map((u) => (
          <tr key={u.id}>
            <td>{u.id}</td>
            <td>
              {u.first_name} {u.last_name}
            </td>
            <td>{u.email}</td>
            <td>{u.age}</td>
            <td>
              <span className="badge">{u.is_active ? "Yes" : "No"}</span>
            </td>
            <td style={{ whiteSpace: "nowrap" }}>
              <button onClick={() => onEdit(u)} disabled={busyId === u.id}>
                Edit
              </button>{" "}
              <button onClick={() => onDelete(u)} disabled={busyId === u.id}>
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}