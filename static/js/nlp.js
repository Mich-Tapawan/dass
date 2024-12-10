document.addEventListener("DOMContentLoaded", () => {
  const textArea = document.getElementById("user-input");
  const analyzeBtn = document.getElementById("analyze-btn");
  const symptomsList = document.getElementById("symptoms-list");
  const depressionCount = document.getElementById("depression-count");
  const anxietyCount = document.getElementById("anxiety-count");
  const stressCount = document.getElementById("stress-count");

  analyzeBtn.addEventListener("click", () => {
    const userText = textArea.value;
    if (userText === "") {
      alert("Please enter text before submitting");
      return;
    }
    processText(userText);
  });

  async function processText(text) {
    console.log(text);
    const response = await fetch("http://localhost:5000/processText", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    console.log(data);
    const keywords = String(data.matched_symptoms.Depression);
    symptomsList.innerHTML = keywords;

    depressionCount.innerHTML = data.symptom_counts.Depression;
    anxietyCount.innerHTML = data.symptom_counts.Anxiety;
    stressCount.innerHTML = data.symptom_counts.Stress;
  }
});
