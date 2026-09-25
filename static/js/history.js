/**
 * VisionCaption AI - Recent Analysis History Manager
 * Persists recent image understanding sessions in localStorage.
 */

const HISTORY_KEY = 'visioncaption_history_v2';
const MAX_HISTORY = 20;

const HistoryManager = {
  getAll() {
    try {
      const data = localStorage.getItem(HISTORY_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Failed to parse history:', e);
      return [];
    }
  },

  add(item) {
    try {
      const current = this.getAll();
      const entry = {
        id: item.id || `hist_${Date.now()}`,
        timestamp: new Date().toISOString(),
        languageCode: item.language_code || 'en',
        languageName: item.language_name || 'English',
        languageFlag: item.languageFlag || '🌐',
        caption: item.short_caption || 'Image Analysis',
        imageUrl: item.image_url || '',
        analysis: item
      };

      // Prepend and trim
      const updated = [entry, ...current.filter(x => x.id !== entry.id)].slice(0, MAX_HISTORY);
      localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
      this.updateBadge();
    } catch (e) {
      console.warn('Could not save to localStorage:', e);
    }
  },

  remove(id) {
    const updated = this.getAll().filter(item => item.id !== id);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
    this.updateBadge();
    this.render();
  },

  clear() {
    localStorage.removeItem(HISTORY_KEY);
    this.updateBadge();
    this.render();
  },

  updateBadge() {
    const badge = document.getElementById('history-count-badge');
    if (badge) {
      const count = this.getAll().length;
      badge.textContent = count;
      badge.classList.toggle('hidden', count === 0);
    }
  },

  render() {
    const listEl = document.getElementById('history-list');
    const emptyEl = document.getElementById('history-empty');
    if (!listEl) return;

    const items = this.getAll();
    if (items.length === 0) {
      listEl.innerHTML = '';
      if (emptyEl) emptyEl.classList.remove('hidden');
      return;
    }

    if (emptyEl) emptyEl.classList.add('hidden');
    listEl.innerHTML = items.map(item => {
      const timeStr = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const dateStr = new Date(item.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric' });
      return `
        <div class="p-3 bg-gray-800/60 hover:bg-gray-700/60 rounded-xl border border-gray-700/50 transition cursor-pointer flex gap-3 items-center group" onclick="HistoryManager.reopen('${item.id}')">
          <img src="${item.imageUrl}" class="w-14 h-14 object-cover rounded-lg border border-gray-600 flex-shrink-0" alt="Thumbnail" onerror="this.src='/static/samples/street_market.jpg'">
          <div class="flex-grow min-w-0">
            <div class="flex items-center justify-between gap-1 mb-1">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30 truncate">
                ${item.languageFlag} ${item.languageName}
              </span>
              <span class="text-[11px] text-gray-400 flex-shrink-0">${dateStr}, ${timeStr}</span>
            </div>
            <p class="text-xs text-gray-200 line-clamp-2 leading-relaxed">${item.caption}</p>
          </div>
          <button onclick="event.stopPropagation(); HistoryManager.remove('${item.id}')" class="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 transition p-1">
            ✕
          </button>
        </div>
      `;
    }).join('');
  },

  reopen(id) {
    const item = this.getAll().find(x => x.id === id);
    if (item && window.restoreAnalysis) {
      window.restoreAnalysis(item.analysis, item.imageUrl);
      // Close history drawer
      const drawer = document.getElementById('history-drawer');
      if (drawer) drawer.classList.add('translate-x-full');
    }
  }
};

window.HistoryManager = HistoryManager;
