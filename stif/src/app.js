import { loadItems, saveItems, uid } from './store.js';

// Main app logic for stif — tiny client-side list manager

const elements = {
  input: null,
  addBtn: null,
  list: null,
  empty: null
};

let items = [];

function createItemElement(item) {
  const li = document.createElement('li');
  li.className = 'item';
  li.dataset.id = item.id;

  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.checked = !!item.completed;
  checkbox.setAttribute('aria-label', 'Mark item completed');

  const text = document.createElement('div');
  text.className = 'text' + (item.completed ? ' completed' : '');
  text.textContent = item.text;

  const del = document.createElement('button');
  del.className = 'delete';
  del.title = 'Delete';
  del.textContent = '✕';

  li.appendChild(checkbox);
  li.appendChild(text);
  li.appendChild(del);

  return li;
}

function render() {
  elements.list.innerHTML = '';
  if (items.length === 0) {
    elements.empty.style.display = 'block';
    return;
  }
  elements.empty.style.display = 'none';
  const fragment = document.createDocumentFragment();
  for (const item of items) {
    fragment.appendChild(createItemElement(item));
  }
  elements.list.appendChild(fragment);
}

function addItem(text) {
  const trimmed = text.trim();
  if (!trimmed) return;
  const newItem = { id: uid(), text: trimmed, completed: false };
  items.unshift(newItem);
  saveItems(items);
  render();
}

function toggleItem(id, completed) {
  const idx = items.findIndex(i => i.id === id);
  if (idx === -1) return;
  items[idx].completed = completed;
  saveItems(items);
  render();
}

function deleteItem(id) {
  items = items.filter(i => i.id !== id);
  saveItems(items);
  render();
}

function wireUI() {
  elements.input = document.getElementById('new-item');
  elements.addBtn = document.getElementById('add-btn');
  elements.list = document.getElementById('items');
  elements.empty = document.getElementById('empty');

  elements.addBtn.addEventListener('click', () => {
    addItem(elements.input.value);
    elements.input.value = '';
    elements.input.focus();
  });

  elements.input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      addItem(elements.input.value);
      elements.input.value = '';
    }
  });

  // Event delegation for list interactions
  elements.list.addEventListener('click', (e) => {
    const li = e.target.closest('li.item');
    if (!li) return;
    const id = li.dataset.id;
    if (e.target.matches('button.delete')) {
      deleteItem(id);
    }
  });

  elements.list.addEventListener('change', (e) => {
    if (e.target.matches('input[type="checkbox"]')) {
      const li = e.target.closest('li.item');
      if (!li) return;
      const id = li.dataset.id;
      toggleItem(id, e.target.checked);
    }
  });
}

function init() {
  items = loadItems();
  wireUI();
  render();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Known issues (documented here):
// - Rapid repeated adds (very fast typing + multiple Enter presses) may create duplicates
//   because there's no debouncing or optimistic locking.
// - No edit-in-place feature yet. Deleting is permanent (no undo).
// - LocalStorage is the only persistence; clearing storage loses data.
// - Accessibility improvements needed (focus management, screen reader announcements).
