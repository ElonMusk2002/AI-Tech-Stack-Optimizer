// main.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const resultSection = document.createElement("div");
  resultSection.id = "results";
  document.querySelector("main").appendChild(resultSection);

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const checkedCheckboxes = document.querySelectorAll(
      'input[name="tech_stack"]:checked'
    );
    const techStack = Array.from(checkedCheckboxes).map((cb) => cb.value);

    if (techStack.length === 0) {
      console.error("No technologies selected");
      resultSection.innerHTML =
        '<p class="error">Please select at least one technology.</p>';
      return;
    }

    resultSection.innerHTML = '<p class="loading">Loading...</p>';

    fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tech_stack: techStack }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          throw new Error(data.error);
        }
        displayResults(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        resultSection.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
      });
  });

  function displayResults(data) {
    let html = "<h2>Analysis Results</h2>";

    html += "<h3>Tech Stack Analysis</h3>";
    for (const [tech, details] of Object.entries(data.analysis)) {
      html += `
                <div class="tech-item">
                    <h4>${escapeHTML(tech)}</h4>
                    <p>Category: ${escapeHTML(details.category)}</p>
                    <p>Popularity: ${escapeHTML(details.popularity)}</p>
                    <p>Description: ${escapeHTML(details.description)}</p>
                </div>
            `;
    }

    html += "<h3>Recommendations</h3>";
    for (const [tech, alternatives] of Object.entries(data.recommendations)) {
      html += `
                <div class="recommendation-item">
                    <h4>Alternatives for ${escapeHTML(tech)}</h4>
                    <ul>
                        ${alternatives
                          .map(
                            (alt) => `
                            <li>
                                <strong>${escapeHTML(alt.name)}</strong>
                                <p>Reason: ${escapeHTML(alt.reason)}</p>
                                <p>Score: ${escapeHTML(alt.score)}</p>
                            </li>
                        `
                          )
                          .join("")}
                    </ul>
                </div>
            `;
    }
    html += "<h2>Overall Opinion</h2>";
    html += `
            <p><strong>Opinion:</strong> ${escapeHTML(
              data.overall_opinion.opinion
            )}</p>
            <h3>Strengths</h3>
            <ul>
                ${data.overall_opinion.strengths
                  .map((strength) => `<li>${escapeHTML(strength)}</li>`)
                  .join("")}
            </ul>
            <h3>Weaknesses</h3>
            <ul>
                ${data.overall_opinion.weaknesses
                  .map((weakness) => `<li>${escapeHTML(weakness)}</li>`)
                  .join("")}
            </ul>
        `;

    resultSection.innerHTML = html;
  }

  function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
