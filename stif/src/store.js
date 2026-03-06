// Simple persistence helpers for stif
// Keep this module minimal and dependency-free.

const STORAGE_KEY = 'stif.items.v1';

export function loadItems() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed;
  } catch (e) {
    console.error('Failed to load items', e);
    return [];
  }
}

export function saveItems(items) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch (e) {
    console.error('Failed to save items', e);
  }
}

export function uid() {
  // Simple unique id. Not cryptographically strong.
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 9);
}
