import React from "react";

/**
 * Props:
 *  - rows: array of complaint objects
 * If rows not provided, component will attempt to fetch via API (fallback).
 */

export default function ComplaintTable({ rows = [] }) {
  return (
    <div className="table-wrapper">
      <table className="complaint-table">
        <thead>
          <tr>
            <th>Ref ID</th>
            <th>Phone</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan="6" style={{ textAlign: "center" }}>
                No complaints found
              </td>
            </tr>
          ) : (
            rows.map((r) => (
              <tr key={r.reference_id}>
                <td>{r.reference_id}</td>
                <td>{r.phone}</td>
                <td>{r.incident_type}</td>
                <td>{r.amount ?? "-"}</td>
                <td>{r.status}</td>
                <td>{new Date(r.created_at).toLocaleString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
