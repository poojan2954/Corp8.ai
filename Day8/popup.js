document.getElementById("submit").addEventListener("click", async () => {
  const question = document.getElementById("question").value;

  // Get current tab URL
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = new URL(tab.url);

  // Extract YouTube video ID
  const videoId = url.searchParams.get("v");

  if (!videoId) {
    document.getElementById("answer").innerText = "❌ Not a valid YouTube video.";
    return;
  }

  // Send question + video ID to your Python backend
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ video_id: videoId, question })
  });

  const data = await response.json();
  document.getElementById("answer").innerText = data.answer || "No answer returned.";
});
