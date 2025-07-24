if (!localStorage.getItem('isLoggedIn')) {
  alert("Please login to view history.");
  window.location.href = "login.html";
}

document.addEventListener('DOMContentLoaded', () => {
  const history = JSON.parse(localStorage.getItem('promptHistory')) || [];
  const container = document.getElementById('versionHistory');
  if (container) {
    container.innerHTML = history.map(entry => `
      <div class="history-entry">
        <h4>${entry.timestamp}</h4>
        <p>${entry.text}</p>
      </div>
    `).join('');
  }
});
