let draggedElement = null;
let offsetX = 0;
let offsetY = 0;

document.querySelectorAll('.window').forEach(win => {
    const saved = localStorage.getItem("winstate_" + win.id);
    if (!saved) return;

    const state = JSON.parse(saved);

    if (state.left) win.style.left = state.left;
    if (state.top) win.style.top = state.top;
    if (state.width) win.style.width = state.width;
    if (state.height) win.style.height = state.height;

    if (state.active) {
        win.classList.add('active');
    } else {
        win.classList.remove('active');
    }
});

function OpenWindow(id, triggerEl) {
    const winEl = document.getElementById(id);
    if (!winEl) return;

    if (!triggerEl) {
        triggerEl = Array.from(document.querySelectorAll('.window-button')).find(b => {
            const on = b.getAttribute('onclick') || '';
            return on.indexOf("'" + id + "'") !== -1 || on.indexOf('"' + id + '"') !== -1 || on.indexOf(id) !== -1;
        });
    }

    winEl.classList.add('active');
    saveWindowState(winEl)
    bringToFront(winEl);

    if (triggerEl && typeof triggerEl.getBoundingClientRect === 'function') {
        const btnRect = triggerEl.getBoundingClientRect();
        const winRect = winEl.getBoundingClientRect();

        let left = btnRect.left + (btnRect.width / 2) - (winRect.width / 2);
        let top = btnRect.bottom + 8 - 50;

        left = Math.max(8, Math.min(left, window.innerWidth - winRect.width - 8));
        top = Math.max(8, Math.min(top, window.innerHeight - winRect.height - 8));

        winEl.style.left = left + 'px';
        winEl.style.top = top + 'px';
    }
}

function closeWindow(id) {
    const win = document.getElementById(id)
    win.classList.remove('active');
    saveWindowState(win)
}

function bringToFront(element) {
    const windows = document.querySelectorAll('.window');
    windows.forEach(w => w.style.zIndex = 1);
    element.style.zIndex = 1000;
}

function startDrag(e, id) {
    draggedElement = document.getElementById(id);
    const rect = draggedElement.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;
    bringToFront(draggedElement);
   
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDrag);
}

function drag(e) {
    if (draggedElement) {
        let newX = e.clientX - offsetX;
        let newY = e.clientY - offsetY;
       
        newX = Math.max(0, Math.min(newX, window.innerWidth - draggedElement.offsetWidth));
        newY = Math.max(0, Math.min(newY, window.innerHeight - draggedElement.offsetHeight));
       
        draggedElement.style.left = newX + 'px';
        draggedElement.style.top = newY + 'px';
    }
}

function saveWindowState(win) {
    const state = {
        left: win.style.left,
        top: win.style.top,
        width: win.style.width,
        height: win.style.height,
        active: win.classList.contains('active')
    };
    localStorage.setItem("winstate_" + win.id, JSON.stringify(state));
}

function stopDrag() {
    saveWindowState(draggedElement)
    draggedElement = null;
    document.removeEventListener('mousemove', drag);
    document.removeEventListener('mouseup', stopDrag);
}

document.querySelectorAll('.window').forEach(window => {
    window.addEventListener('mousedown', () => bringToFront(window));
});


let currentPlayer = 'X';
let tttBoard = ['', '', '', '', '', '', '', '', ''];
let gameActive = true;
let humanPlayer = 'X';
let botPlayer = 'O';
let lastWinner = null;

const winPatterns = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

function initTicTacToe() {
    const boardEl = document.getElementById('tttBoard');
    if (!boardEl) {
        console.error('Board element not found!');
        return;
    }
    
    boardEl.innerHTML = '';
    tttBoard = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    currentPlayer = humanPlayer;
    
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.index = i;
        cell.addEventListener('click', handleCellClick);
        boardEl.appendChild(cell);
    }

    const resetBtn = document.getElementById('tttResetBtn');
    if (resetBtn) {
        resetBtn.removeEventListener('click', resetGame);
        resetBtn.addEventListener('click', resetGame);
    }
    
    const statusEl = document.getElementById('tttStatus');
    if (statusEl) statusEl.textContent = 'Your Turn';
}

function handleCellClick(e) {
    const index = e.target.dataset.index;
    
    if (tttBoard[index] !== '' || !gameActive || currentPlayer !== humanPlayer) return;
    
    makeMove(index, humanPlayer);
    
    if (gameActive) {
        setTimeout(botMove, 500);
    }
}

function makeMove(index, player) {
    tttBoard[index] = player;
    const cells = document.querySelectorAll('#tttBoard .cell');
    cells[index].textContent = player;
    cells[index].classList.add('taken');
    
    const statusEl = document.getElementById('tttStatus');
    
    if (checkWin()) {
        lastWinner = player;
        const winner = player === humanPlayer ? 'You Win!' : 'Bot Wins!';
        if (statusEl) statusEl.textContent = winner;
        gameActive = false;
        return;
    }
    
    if (tttBoard.every(cell => cell !== '')) {
        if (statusEl) statusEl.textContent = 'Draw!';
        gameActive = false;
        lastWinner = null;
        return;
    }
    
    currentPlayer = player === humanPlayer ? botPlayer : humanPlayer;
    const turn = currentPlayer === humanPlayer ? 'Your Turn' : 'Bot Thinking...';
    if (statusEl) statusEl.textContent = turn;
}

function botMove() {
    if (!gameActive) return;
    
    const move = getBestMove();
    makeMove(move, botPlayer);
}

function getBestMove() {
    for (let i = 0; i < 9; i++) {
        if (tttBoard[i] === '') {
            tttBoard[i] = botPlayer;
            if (checkWin()) {
                tttBoard[i] = '';
                return i;
            }
            tttBoard[i] = '';
        }
    }
    
    for (let i = 0; i < 9; i++) {
        if (tttBoard[i] === '') {
            tttBoard[i] = humanPlayer;
            if (checkWin()) {
                tttBoard[i] = '';
                return i;
            }
            tttBoard[i] = '';
        }
    }
    
    if (tttBoard[4] === '') return 4;
    
    const corners = [0, 2, 6, 8];
    const availableCorners = corners.filter(i => tttBoard[i] === '');
    if (availableCorners.length > 0) {
        return availableCorners[Math.floor(Math.random() * availableCorners.length)];
    }
    
    const available = tttBoard.map((cell, i) => cell === '' ? i : null).filter(i => i !== null);
    return available[Math.floor(Math.random() * available.length)];
}

function checkWin() {
    return winPatterns.some(pattern => {
        const [a, b, c] = pattern;
        return tttBoard[a] && tttBoard[a] === tttBoard[b] && tttBoard[a] === tttBoard[c];
    });
}

function resetGame() {
    tttBoard = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    
    document.querySelectorAll('#tttBoard .cell').forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('taken');
    });
    
    const statusEl = document.getElementById('tttStatus');
    
    if (lastWinner === botPlayer) {
        currentPlayer = botPlayer;
        if (statusEl) statusEl.textContent = 'Bot Goes First...';
        setTimeout(botMove, 500);
    } else {
        currentPlayer = humanPlayer;
        if (statusEl) statusEl.textContent = 'Your Turn';
    }
}

let slotsWins = 0;

function spinSlots() {
    const symbols = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣'];
    const slot1 = document.getElementById('slot1');
    const slot2 = document.getElementById('slot2');
    const slot3 = document.getElementById('slot3');
    const result = document.getElementById('slotsResult');
    
    let spins = 0;
    const spinInterval = setInterval(() => {
        slot1.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        slot2.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        slot3.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        spins++;
        
        if (spins >= 20) {
            clearInterval(spinInterval);
            
            const final1 = symbols[Math.floor(Math.random() * symbols.length)];
            const final2 = symbols[Math.floor(Math.random() * symbols.length)];
            const final3 = symbols[Math.floor(Math.random() * symbols.length)];
            
            slot1.textContent = final1;
            slot2.textContent = final2;
            slot3.textContent = final3;
            
            if (final1 === final2 && final2 === final3) {
                slotsWins++;
                document.getElementById('slotsWins').textContent = slotsWins;
                result.textContent = '🎉 JACKPOT! YOU WIN! 🎉';
                result.style.color = '#ff0';
            } else if (final1 === final2 || final2 === final3 || final1 === final3) {
                result.textContent = 'Close! Two match!';
                result.style.color = '#0ff';
            } else {
                result.textContent = 'Try again!';
                result.style.color = '#f00';
            }
        }
    }, 100);
}