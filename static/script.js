const input = document.getElementById("movieInput");
const btn = document.getElementById("searchBtn");
const grid = document.getElementById("grid");
const statusText = document.getElementById("statusText");
const chip = document.getElementById("chip");
document.getElementById("year").textContent = new Date().getFullYear();

function setStatus(text, pillText = null) {
  statusText.textContent = text;
  if (pillText) {
    chip.textContent = pillText;
    chip.classList.remove("hidden");
  } else {
    chip.classList.add("hidden");
  }
}

function showSkeletons(count = 8) {
  grid.innerHTML = "";
  for (let i = 0; i < count; i++) {
    const s = document.createElement("div");
    s.className = "skeleton";
    grid.appendChild(s);
  }
}

function renderCards(movie, recs) {
  grid.innerHTML = "";
  recs.forEach((rec, idx) => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <div class="poster">
        <img src="${escapeHtml(rec.poster)}" alt="${escapeHtml(rec.title)}" loading="lazy" />
        <div class="badge">✨ #${idx + 1}</div>
      </div>
      <div class="card-content">
        <div class="title">${escapeHtml(rec.title)}</div>
      </div>
    `;

    grid.appendChild(card);
  });
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function getRecommendations() {
  const movie = input.value.trim();
  if (!movie) {
    setStatus("Type a movie name first.");
    grid.innerHTML = "";
    return;
  }

  btn.disabled = true;
  setStatus("Searching your model…", "Working");
  showSkeletons();

  try {
    const res = await fetch(`/recommend?movie=${encodeURIComponent(movie)}`);
    const data = await res.json();

    if (!res.ok) {
      setStatus(data.error || "Something went wrong.");
      grid.innerHTML = "";
      return;
    }

    setStatus(`Showing recommendations for "${data.searched_movie}"`, `${data.recommendations.length} results`);
    renderCards(data.searched_movie, data.recommendations);
  } catch (e) {
    setStatus("Network error. Is Flask running?");
    grid.innerHTML = "";
  } finally {
    btn.disabled = false;
  }
}

btn.addEventListener("click", getRecommendations);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") getRecommendations();
});
