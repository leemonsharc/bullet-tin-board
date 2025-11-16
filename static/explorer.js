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
    const statusEl = document.getElementById('explorerStatus');
    if (statusEl) statusEl.textContent = `Selected: ${path}`;
    renderTree();
}

function renderItem(item, path = '', indent = 0) {
    let currentPath;
    if (path === 'C:\\') {
        currentPath = `C:\\${item.name}`;
    } else {
        currentPath = path ? `${path}/${item.name}` : item.name;
    }
    
    const isExpanded = expanded[currentPath];
    const isSelected = selected === currentPath;
    const escapedPath = currentPath.replace(/\\/g, '\\\\');

    let html = '';

    if (item.type === 'folder') {
        const chevron = isExpanded ? '▼' : '►';
        html += `<div class="item ${isSelected ? 'selected' : ''}" 
                      onclick="toggleFolder('${escapedPath}'); selectItem('${escapedPath}')"
                      style="margin-left: ${indent * 20}px">
                    <span class="chevron">${chevron}</span>
                    <span class="folder">📁 ${item.name}</span>
                 </div>`;

        if (isExpanded && item.children) {
            item.children.forEach(child => {
                html += renderItem(child, currentPath, indent + 1);
            });
        }

    } else {
        html += `<div class="item ${isSelected ? 'selected' : ''}"
                  onclick="selectItem('${escapedPath}')"
                  ondblclick="executeFile('${escapedPath}')"
                  style="margin-left: ${(indent + 1) * 20}px">
                <span class="file">📄 ${item.name}</span>
             </div>`;
    }

    return html;
}

function executeFile(path) {
    if (path.includes('TICTACTOE')) {
        OpenWindow('ticTacToe');
        setTimeout(initTicTacToe, 100);
    }
}

function executeFile(path) {
    console.log('executeFile called with:', path);
    if (path.includes('TICTACTOE')) {
        console.log('Opening tic tac toe...');
        OpenWindow('ticTacToe');
        setTimeout(initTicTacToe, 100);
    }
}

function renderTree() {
    const tree = document.getElementById('fileTree');
    let html = '';
    
    if (fileSystem) {
        const isExpanded = expanded[fileSystem.name];
        const chevron = isExpanded ? '▼' : '►';
        const escapedName = fileSystem.name.replace(/\\/g, '\\\\');
        html += `<div class="item" 
                      onclick="toggleFolder('${escapedName}'); selectItem('${escapedName}')"
                      style="margin-left: 0px">
                    <span class="chevron">${chevron}</span>
                    <span class="folder">📁 ${fileSystem.name}</span>
                 </div>`;
        
        if (isExpanded && fileSystem.children) {
            fileSystem.children.forEach(child => {
                html += renderItem(child, fileSystem.name, 1);
            });
        }
    }
    
    tree.innerHTML = html;
}

loadFiles();