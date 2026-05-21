import React from 'react';

function App() {
  return (
    <div style={{
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      maxWidth: "600px",
      margin: "50px auto",
      padding: "30px",
      borderRadius: "10px",
      boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
      backgroundColor: "#f0fdf4",
      border: "1px solid #bbf7d0"
    }}>
      <h1 style={{ color: "#16a34a", marginTop: 0, display: "flex", alignItems: "center", gap: "10px" }}>
        ⚡ Multi-Stage Build Success!
      </h1>
      <p style={{ fontSize: "16px", color: "#1f2937" }}>
        This React application was compiled inside a heavy Node.js environment, but is now served by a lightweight Nginx web server.
      </p>
      
      <div style={{ backgroundColor: "#ffffff", border: "1px solid #bbf7d0", borderRadius: "8px", padding: "15px", margin: "20px 0" }}>
        <h3 style={{ color: "#15803d", marginTop: 0, marginBottom: "10px" }}>📦 Image Size Analysis</h3>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #e5e7eb", textAlign: "left" }}>
              <th style={{ padding: "8px 0" }}>Build Strategy</th>
              <th style={{ padding: "8px 0" }}>Estimated Size</th>
              <th style={{ padding: "8px 0" }}>Inclusions</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: "1px solid #f3f4f6" }}>
              <td style={{ padding: "8px 0" }}><b>Single-stage (Node runtime)</b></td>
              <td style={{ padding: "8px 0", color: "#dc2626", fontWeight: "bold" }}>~1.2 GB</td>
              <td style={{ padding: "8px 0", color: "#6b7280" }}>Node Engine, Compiler, Dev dependencies, npm cache</td>
            </tr>
            <tr>
              <td style={{ padding: "8px 0" }}><b>Multi-stage (Nginx runner)</b></td>
              <td style={{ padding: "8px 0", color: "#16a34a", fontWeight: "bold" }}>~25 MB</td>
              <td style={{ padding: "8px 0", color: "#6b7280" }}>Only static build assets + alpine Nginx web server</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <hr style={{ border: 0, borderTop: "1px solid #bbf7d0", margin: "20px 0" }} />
      <p style={{ color: "#166534", fontStyle: "italic", fontSize: "14px", textAlign: "center" }}>
        Secure, lightweight, and optimized for production deployments.
      </p>
    </div>
  );
}

export default App;
