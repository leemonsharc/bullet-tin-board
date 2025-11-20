const STORAGE_KEY = 'bullet_tin_history';

function loadHistory() {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
}

function saveHistory(arr) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
}

function renderHistory() {
    const container = document.getElementById('terminalHistory');
    container.innerHTML = '';
    const hist = loadHistory();
    hist.forEach(entry => {
        const p = document.createElement('p');
        p.innerHTML = entry;
        container.appendChild(p);
    });
    container.parentElement.scrollTop = container.parentElement.scrollHeight;
}

function addHistoryEntry(text) {
    const hist = loadHistory();
    hist.push(text);
    saveHistory(hist);
    renderHistory();
}

async function submitCommand(evt) {
    evt.preventDefault();
    const input = document.getElementById('cmdInput');
    const command = input.value.trim();
    if (!command) return;

    const cmdLower = command.toLowerCase();
    if (cmdLower === 'clear' || cmdLower === 'cls') {
        localStorage.removeItem(STORAGE_KEY);
        renderHistory();
        input.value = '';
        return;
    }

    addHistoryEntry('&gt; ' + escapeHtml(command));
    input.value = '';

    try {
        const res = await fetch('/api/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command})
        });
        if (res.ok) {
            const data = await res.json();
            const resp = (data.response || '').replace(/\r?\n+$/,'');
            addHistoryEntry(resp || '');
        } else {
            addHistoryEntry('Error: could not reach server.');
        }
    } catch (e) {
        addHistoryEntry('Error: ' + e.message);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.getElementById('cmdForm').addEventListener('submit', submitCommand);

// initialize
renderHistory();