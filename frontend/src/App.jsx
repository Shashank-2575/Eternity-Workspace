import { useState } from "react";

function App() {
  const [loading, setLoading] = useState(false);

  const startWorkspace = async () => {
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/workspace/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: "my-workspace",
        }),
      });

      const data = await res.json();

      console.log(data);

      // 🔥 Open workspace in new tab
      window.open(data.url, "_blank");

    } catch (err) {
      console.error(err);
      alert("Failed to start workspace");
    }

    setLoading(false);
  };

  return (
    <div>
      <h1>Eternity Workspace</h1>

      <button onClick={startWorkspace} disabled={loading}>
        {loading ? "Starting..." : "Start Workspace"}
      </button>
    </div>
  );
}

export default App;