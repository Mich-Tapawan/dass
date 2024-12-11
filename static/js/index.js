document.addEventListener("DOMContentLoaded", () => {
  const questionList = document.getElementById("question-list");
  const returnBtn = document.getElementById("return");
  const nextBtn = document.getElementById("next");
  let dAnswers = [];
  let aAnswers = [];
  let sAnswers = [];

  const questions = [
    "I felt that I had nothing to look forward to",
    "I was unable to become enthusiastic about anything",
    "I feel like I am not worth anything as a person",
    "I believe that life is meaningless",
    "I couldn’t seem to experience any positive feelings at all",
    "I found it difficult to work up the initiative to do things",
    "I was downhearted and blue",
    "I was aware of dryness of my mouth",
    "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion) ",
    "I experienced trembling (e.g. in the hands)",
    "I was worried about situations in which I might panic and make a fool of myself",
    "I felt I was close to panic",
    "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)",
    "I felt scared without any good reason",
    "I found it hard to wind down",
    "I tended to over-react to situations",
    "I felt that I was using a lot of nervous energy",
    "I found myself getting agitated",
    "I found it difficult to relax",
    "I was intolerant of anything that kept me from getting on with what I was doing ",
    "I felt that I was rather touchy ",
  ];
  const choices = ["Never", "Sometimes", "Often", "Very Often"];
  let count = 0;

  questions.forEach((question) => {
    const li = document.createElement("li");
    const p = document.createElement("p");
    const select = document.createElement("select");

    count += 1;
    p.innerHTML = `${count}. ${question}`;

    choices.forEach((choice) => {
      const option = document.createElement("option");
      option.innerHTML = choice;
      option.setAttribute("value", choice);
      select.appendChild(option);
    });

    if (count <= 7) {
      select.setAttribute("class", "D-question");
    } else if (count <= 14) {
      select.setAttribute("class", "A-question");
    } else {
      select.setAttribute("class", "S-question");
    }

    li.append(p, select);
    questionList.appendChild(li);
  });

  const groups = [
    document.querySelectorAll(".D-question"),
    document.querySelectorAll(".A-question"),
    document.querySelectorAll(".S-question"),
  ];
  let currentGroupIndex = 0;

  function showGroup(index) {
    groups.forEach((group, i) => {
      group.forEach((element) => {
        element.parentElement.style.display = i === index ? "block" : "none";
      });
    });
  }

  showGroup(currentGroupIndex);

  nextBtn.addEventListener("click", () => {
    if (currentGroupIndex < groups.length - 1) {
      currentGroupIndex++;
      showGroup(currentGroupIndex);
    } else {
      currentGroupIndex = 0;
      showGroup(currentGroupIndex);
      computeDASS(dAnswers, aAnswers, sAnswers);
    }

    returnBtn.style.background = currentGroupIndex == 0 ? "#e57373" : "#f34646";
    nextBtn.innerHTML =
      currentGroupIndex === groups.length - 1 ? "SUBMIT" : "NEXT";
  });

  returnBtn.addEventListener("click", () => {
    if (currentGroupIndex > 0) {
      currentGroupIndex--;
      showGroup(currentGroupIndex);
    }

    returnBtn.style.background = currentGroupIndex == 0 ? "#e57373" : "#f34646";
    nextBtn.innerHTML =
      currentGroupIndex === groups.length - 1 ? "SUBMIT" : "NEXT";
  });

  async function computeDASS(dAnswers, aAnswers, sAnswers) {
    console.log(dAnswers, aAnswers, sAnswers);
    try {
      const res = await fetch("http://localhost:5000/computeDass", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dAnswers, aAnswers, sAnswers }),
      });
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error("Error computing DASS: ", error);
    }
  }
});
