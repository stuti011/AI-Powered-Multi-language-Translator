// Load language list on page load
document.addEventListener("DOMContentLoaded", () => {
  fetch("/get-languages")
    .then(res => res.json())
    .then(data => {
      const sourceLang = document.getElementById("source-lang");
      const targetLang = document.getElementById("target-lang");

      for (const [code, name] of Object.entries(data.languages)) {
        const option1 = new Option(name, code);
        const option2 = new Option(name, code);
        sourceLang.add(option1);
        targetLang.add(option2);
      }
    });
});

document.getElementById("translate-btn").addEventListener("click", () => {
  const text = document.getElementById("text-input").value;
  const sourceLang = document.getElementById("source-lang").value;
  const targetLangs = Array.from(document.getElementById("target-lang").selectedOptions).map(opt => opt.value);

  if (!text || targetLangs.length === 0) {
    alert("Please enter text and select at least one target language.");
    return;
  }

  fetch("/translate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: text,
      source_language: sourceLang || null,
      target_languages: targetLangs
    })
  })
  .then(res => res.json())
  .then(data => {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";
    for (const [lang, translation] of Object.entries(data.translations)) {
      const div = document.createElement("div");
      div.className = "result-item";
      div.innerHTML = `<strong>${lang}</strong>: ${translation}`;
      resultsDiv.appendChild(div);
    }
  })
  .catch(err => {
    alert("Error during translation. Check backend console.");
    console.error(err);
  });
});
