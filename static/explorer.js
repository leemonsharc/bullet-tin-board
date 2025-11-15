let fileSystem = null;
let expanded = {};
let selected = null;

async function loadFiles() {
    const response = await fetch('/api/files');
    fileSystem = await response.json();
    renderTree();
}

function toggleFolder(path) {
    expanded[path] = !expanded[path];
    renderTree();
}

function selectItem(path) {
    selected = path;
    document.getElementById('status').textContent = `Selected: ${path}`;
    renderTree();
}

function renderItem(item, path = '', indent = 0) {
    const currentPath = path ? `${path}/${item.name}` : item.name;
    const isExpanded = expanded[currentPath];
    const isSelected = selected === currentPath;

    let html = '';

    if (item.type === 'folder') {
        const chevron = isExpanded ? '▼' : '►';
        html += `<div class="item ${isSelected ? 'selected' : ''}" 
                      onclick="toggleFolder('${currentPath}'); selectItem('${currentPath}')"
                      style="margin-left: ${indent * 20}px">
                    <span class="chevron">${chevron}</span>
                    <span class="folder">📁 ${item.name}</span>
                 </div>`;

    } else {
        html += `<div class="item ${isSelected ? 'selected' : ''}"
                  onclick="selectItem('${currentPath}')"
                  ondblclick="executeFile('${currentPath}')"
                  style="margin-left: ${(indent + 1) * 20}px">
                <span class="file">📄 ${item.name}</span>
             </div>`;
    }

    if (isExpanded && item.children) {
        item.children.forEach(child => {
            html += renderItem(child, currentPath, indent + 1);
        });
    }

    return html;
}
function executeFile(path) {
    if (path.includes('TICTACTOE.EXE')) {
        document.getElementById('ticTacToe').classList.add('active');
    }
}
function executeFile(path) {
    if (path.includes('TICTACTOE.EXE')) {
        OpenWindow('ticTacToe');
    }
}
function renderTree() {
    const tree = document.getElementById('file-tree');
    tree.innerHTML = renderItem(fileSystem);
}

// UHHHHH stuff so that tictactoe works and opens when you 2x click
function selectItem(path) {
    selected = path;
    document.getElementById('status').textContent = `Selected: ${path}`;
    renderTree();
}

function executeFile(path) {
    if (path.includes('TICTACTOE.EXE')) {
        document.getElementById('ticTacToe').classList.add('active');
    }
}

loadFiles();
