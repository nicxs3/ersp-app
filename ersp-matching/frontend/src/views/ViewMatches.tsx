import React, { useState } from 'react';

const ViewMatches: React.FC = () => {
  const [matches, setMatches] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchMatches = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:8000/api/v1/match');
    const data = await res.json();
    setMatches(data.matches || []);
    setLoading(false);
  };

  return (
    <div className="form-container" style={{ color: "#222" }}>
      <div className="form-title">View Matches</div>
      <div className="form-subtitle">See the current TA-to-course assignments</div>
      <button className="form-submit" onClick={fetchMatches} disabled={loading}>
        {loading ? "Loading..." : "View Matches"}
      </button>
      {matches && (
        <div style={{ marginTop: 24 }}>
          {matches.length === 0 ? (
            <div>No matches found.</div>
          ) : (
            <table style={{ width: "100%", marginTop: 16, borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left", padding: 8, borderBottom: "1px solid #ccc" }}>Course Slot</th>
                  <th style={{ textAlign: "left", padding: 8, borderBottom: "1px solid #ccc" }}>TA</th>
                </tr>
              </thead>
              <tbody>
                {matches.map((m, i) => (
                  <tr key={i}>
                    <td style={{ padding: 8, borderBottom: "1px solid #eee" }}>{m.course}</td>
                    <td style={{ padding: 8, borderBottom: "1px solid #eee" }}>{m.ta}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default ViewMatches;