// ...existing code...

function handleResult(result) {
    const resultDiv = document.getElementById('result');
    // Instead of clearing, append new results
    resultDiv.innerHTML += `<div class="result-item">${result}</div>`;
}

// Add clear button functionality
function clearResults() {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
}

// ...existing code...