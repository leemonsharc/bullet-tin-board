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

        if (isExpanded && item.children) {
            item.children.forEach(child => {
                html += renderItem(child, currentPath, indent + 1);
            });
        }
    } else {
        html += `<div class="item ${isSelected ? 'selected' : ''}"
                      onclick="selectItem('${currentPath}')"
                      style="margin-left: ${(indent + 1) * 20}px">
                    <span class="file">📄 ${item.name}</span>
                 </div>`;
    }

    return html;
}

function renderTree() {
    const tree = document.getElementById('file-tree');
    tree.innerHTML = renderItem(fileSystem);
}

loadFiles();