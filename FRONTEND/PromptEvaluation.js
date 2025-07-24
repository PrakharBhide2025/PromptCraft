if (!localStorage.getItem('isLoggedIn')) {
  alert("Please login to use Prompt Evaluation.");
  window.location.href = "login.html";
}

function evaluatePrompt(promptText) {
  const feedback = [];

  if (promptText.length >= 100) {
    feedback.push("Prompt is detailed.");
  } else {
    feedback.push(" Try making the prompt more descriptive.");
  }

  if (!promptText.toLowerCase().includes("you")) {
    feedback.push(" Use direct instructions (e.g., 'You should...').");
  }

  if (promptText.endsWith("?")) {
    feedback.push(" Prompt ends with a question – great for open-ended answers.");
  } else {
    feedback.push("Consider ending the prompt with a question to guide the model.");
  }

  if (promptText.match(/\bAI\b|\bChatGPT\b|\bmodel\b/i)) {
    feedback.push("🔍 Prompt mentions AI context – clear intention!");
  }

  const resultBox = document.getElementById("evaluationResult");
  if (resultBox) {
    resultBox.innerHTML = feedback.join("<br>");
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('evaluateBtn');
  const promptInput = document.getElementById('userInput');

  if (btn && promptInput) {
    btn.addEventListener('click', () => {
      const prompt = promptInput.value;
      if (prompt.trim()) {
        evaluatePrompt(prompt);
      } else {
        alert(" Please enter a prompt first.");
      }
    });
  }
});
