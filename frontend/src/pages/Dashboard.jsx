import React, { useEffect, useState } from "react";
import ComplaintTable from "../components/ComplaintTable";
import AnalyticsChart from "../components/AnalyticsChart";
import api from "../services/api";

export default function Dashboard() {
  const [stats, setStats] = useState({ total: 0, recent: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      setLoading(true);
      try {
        // backend currently doesn't have a /stats endpoint; using list for demo
        const res = await api.get("/api/v1/complaints/list");
        const list = res.data || [];
        setStats({ total: list.length, recent: list.slice(0, 10) });
      } catch (e) {
        console.warn("Failed to load stats", e);
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  return (
    <div className="container">
      <header className="header">
        <h1>CyberSathi Admin Dashboard</h1>
        <div className="header-meta">
          <span>Total complaints: {stats.total}</span>
        </div>
      </header>

      <main>
        <section className="card">
          <h2>Analytics</h2>
          <AnalyticsChart />
        </section>

        <section className="card">
          <h2>Recent Complaints</h2>
          {loading ? <p>Loading...</p> : <ComplaintTable rows={stats.recent} />}
        </section>
      </main>

      <footer className="footer">
        <small>CyberSathi — Cybercrime Helpline (1930) Support • Demo UI</small>
      </footer>
    </div>
  );
}
