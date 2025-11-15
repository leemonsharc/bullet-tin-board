let dragggedElement = null;
Let offsetX = 0;
Let offsetY = 0;
Let resizingElement = null;
Let startWidth = 0;
Let startHeight = 0;

function OpenWindow(id, triggerEl) {
    const winEl = document.getElementById(id);
    if (!winEL) return;

    if (!triggerEl) {
        triggerEll = Array.from(document.querySelectorAll('.window-button')).find(b => {
            const on = b.getAttribute('onlick') || '';
            return on.indexOf("'" + id + "'") !== -1 || on.indexOf('"' + id + '"') !== -1 || on.indexOf(id) !== -1;
        });
        }

        winEl.classList.add('active');
        bringToFront(winEl);

        if (triggerEL && typeof triggerEl.getBoundingClientRect === 'function') {
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
        document.getElementById(id).classList.remove('active');
    }

    function bringToFront(element) {
        const windows = document.querySelectorAll('.window');
        windows.forEach(w => w.style.zIndex = 1);
        element.style.zIndex = 1000;
    }

    