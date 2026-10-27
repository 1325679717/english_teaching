/**
 * English Teaching - Mobile Reading Station & Live Sync Client
 */

// Application State
const state = {
  currentPath: '',
  currentMtime: 0,
  fontSize: 17,
  theme: 'light',
  categories: [],
  isLocalServer: true,
  serverInfo: {
    ip: '127.0.0.1',
    port: 8000,
    url: window.location.origin
  },
  pollingTimer: null
};

// DOM Elements
const elements = {
  progressBar: document.getElementById('progress-bar'),
  currentTitle: document.getElementById('current-title'),
  articleContent: document.getElementById('article-content'),
  docNavList: document.getElementById('doc-nav-list'),
  sidebarDrawer: document.getElementById('sidebar-drawer'),
  drawerOverlay: document.getElementById('drawer-overlay'),
  btnMenu: document.getElementById('btn-menu'),
  btnCloseDrawer: document.getElementById('btn-close-drawer'),
  btnFont: document.getElementById('btn-font'),
  fontSheet: document.getElementById('font-sheet'),
  fontDecrease: document.getElementById('font-decrease'),
  fontIncrease: document.getElementById('font-increase'),
  fontReset: document.getElementById('font-reset'),
  fontSizeVal: document.getElementById('font-size-val'),
  btnTheme: document.getElementById('btn-theme'),
  btnRefresh: document.getElementById('btn-refresh'),
  btnQr: document.getElementById('btn-qr'),
  btnShowQrMobile: document.getElementById('btn-show-qr-mobile'),
  qrModal: document.getElementById('qr-modal'),
  btnCloseModal: document.getElementById('btn-close-modal'),
  qrcodeBox: document.getElementById('qrcode-box'),
  qrUrlInput: document.getElementById('qr-url-input'),
  btnCopyUrl: document.getElementById('btn-copy-url'),
  lanIpDisplay: document.getElementById('lan-ip-display'),
  syncToast: document.getElementById('sync-toast'),
  btnPageToc: document.getElementById('btn-page-toc'),
  btnBackTop: document.getElementById('btn-back-top'),
  tocSheet: document.getElementById('toc-sheet'),
  tocOverlay: document.getElementById('toc-overlay'),
  tocSheetContent: document.getElementById('toc-sheet-content'),
  btnCloseToc: document.getElementById('btn-close-toc')
};

// Init application
document.addEventListener('DOMContentLoaded', () => {
  initPreferences();
  initEventListeners();
  fetchServerInfo();
  loadDocuments();
  startPolling();
});

/**
 * Initialize saved preferences (Theme & Font Size)
 */
function initPreferences() {
  // Theme
  const savedTheme = localStorage.getItem('reading_theme') || 'light';
  setTheme(savedTheme);

  // Font Size
  const savedSize = parseInt(localStorage.getItem('reading_font_size'), 10) || 17;
  setFontSize(savedSize);
}

/**
 * Set and apply theme
 */
function setTheme(theme) {
  state.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('reading_theme', theme);

  const icons = {
    light: '☀️',
    sepia: '📜',
    dark: '🌙'
  };
  const iconSpan = elements.btnTheme.querySelector('.theme-icon');
  if (iconSpan) {
    iconSpan.textContent = icons[theme] || '🌓';
  }
}

/**
 * Toggle themes: light -> sepia -> dark -> light
 */
function cycleTheme() {
  const sequence = ['light', 'sepia', 'dark'];
  const nextIdx = (sequence.indexOf(state.theme) + 1) % sequence.length;
  setTheme(sequence[nextIdx]);
}

/**
 * Set and apply font size
 */
function setFontSize(size) {
  const clamped = Math.max(14, Math.min(26, size));
  state.fontSize = clamped;
  document.documentElement.style.setProperty('--font-base', `${clamped}px`);
  elements.fontSizeVal.textContent = `${clamped}px`;
  localStorage.setItem('reading_font_size', clamped);
}

/**
 * Fetch Server LAN Info & Generate QR Code (Dual-mode: dynamic server vs cloud static)
 */
async function fetchServerInfo() {
  try {
    const res = await fetch('/api/info').catch(() => null);
    if (res && res.ok) {
      const data = await res.json();
      state.serverInfo = data;
      state.isLocalServer = true;
      elements.lanIpDisplay.textContent = data.url;
      elements.qrUrlInput.value = data.url;
      renderQrCode(data.url);
      const statusEl = document.getElementById('sync-status');
      if (statusEl) statusEl.textContent = '🟢 局域网实时同步';
      return;
    }
  } catch (err) {
    // Ignore and proceed to static mode
  }

  // Cloud static mode fallback (GitHub Pages / Vercel / Netlify)
  state.isLocalServer = false;
  const currentUrl = window.location.href.split('#')[0];
  state.serverInfo = { url: currentUrl };
  elements.lanIpDisplay.textContent = currentUrl;
  elements.qrUrlInput.value = currentUrl;
  renderQrCode(currentUrl);
  const statusEl = document.getElementById('sync-status');
  if (statusEl) statusEl.textContent = '☁️ 云端永久在线';
}

/**
 * Render QR Code inside modal
 */
let qrCodeInstance = null;
function renderQrCode(url) {
  if (!elements.qrcodeBox) return;
  elements.qrcodeBox.innerHTML = '';
  try {
    qrCodeInstance = new QRCode(elements.qrcodeBox, {
      text: url,
      width: 180,
      height: 180,
      colorDark: '#0f172a',
      colorLight: '#ffffff',
      correctLevel: QRCode.CorrectLevel.M
    });
  } catch (e) {
    console.error('QR code generation error:', e);
  }
}

/**
 * Fetch and render document list (Dual-mode: API vs static JSON)
 */
async function loadDocuments() {
  try {
    let categories = null;

    // 1. Try dynamic API
    const res = await fetch('/api/documents').catch(() => null);
    if (res && res.ok) {
      categories = await res.json();
    } else {
      // 2. Fallback to static documents.json
      const staticRes = await fetch('data/documents.json').catch(() => null);
      if (staticRes && staticRes.ok) {
        categories = await staticRes.json();
      }
    }

    if (!categories) throw new Error('No categories available');

    state.categories = categories;
    renderDocumentNav(categories);

    // Determine which document to open initially
    let initialDoc = '';
    const hashMatch = window.location.hash.match(/#doc=([^&]+)/);
    if (hashMatch && hashMatch[1]) {
      initialDoc = decodeURIComponent(hashMatch[1]);
    } else {
      initialDoc = localStorage.getItem('last_reading_path') || 'guides/english_sentence_learning_guide.md';
    }

    // Verify document exists in list, else pick first
    const allItems = categories.flatMap(c => c.items);
    const exists = allItems.some(i => i.path === initialDoc);
    if (!exists && allItems.length > 0) {
      initialDoc = allItems[0].path;
    }

    if (initialDoc) {
      loadDocument(initialDoc, false);
    }
  } catch (err) {
    console.error('Failed to load documents list:', err);
    elements.docNavList.innerHTML = '<div class="nav-loading" style="color:#ef4444;">无法读取目录，请稍候重试</div>';
  }
}

/**
 * Render document list into drawer sidebar
 */
function renderDocumentNav(categories) {
  elements.docNavList.innerHTML = '';

  categories.forEach(cat => {
    const group = document.createElement('div');
    group.className = 'nav-category';

    const title = document.createElement('div');
    title.className = 'nav-category-title';
    title.textContent = cat.category;
    group.appendChild(title);

    cat.items.forEach(item => {
      const btn = document.createElement('button');
      btn.className = 'nav-item';
      btn.dataset.path = item.path;
      btn.textContent = item.title;
      btn.title = item.title;
      btn.addEventListener('click', () => {
        loadDocument(item.path);
        closeDrawer();
      });
      group.appendChild(btn);
    });

    elements.docNavList.appendChild(group);
  });
}

/**
 * Load and render a specific Markdown document (Dual-mode: dynamic API vs static raw markdown)
 */
async function loadDocument(docPath, updateHash = true) {
  if (!docPath) return;

  state.currentPath = docPath;
  localStorage.setItem('last_reading_path', docPath);
  if (updateHash) {
    window.location.hash = `doc=${encodeURIComponent(docPath)}`;
  }

  // Update active state in nav
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.path === docPath);
  });

  // Find doc title
  const allItems = state.categories.flatMap(c => c.items);
  const matched = allItems.find(i => i.path === docPath);
  if (matched) {
    elements.currentTitle.textContent = matched.title;
    document.title = `${matched.title} · 英语精萃微课`;
  }

  // Show loading spinner
  elements.articleContent.innerHTML = `
    <div class="loading-placeholder">
      <div class="spinner"></div>
      <p>正在加载讲义内容...</p>
    </div>
  `;

  try {
    let rawContent = '';
    let mtime = 0;

    // 1. Try dynamic server API first
    const res = await fetch(`/api/content?path=${encodeURIComponent(docPath)}`).catch(() => null);
    if (res && res.ok) {
      const data = await res.json();
      rawContent = data.content;
      mtime = data.mtime;
    } else {
      // 2. Cloud static mode: fetch raw Markdown file directly!
      const staticRes = await fetch(docPath);
      if (!staticRes.ok) throw new Error(`HTTP ${staticRes.status}: 无法获取讲义文件`);
      rawContent = await staticRes.text();
      mtime = 0;
    }

    state.currentMtime = mtime;
    renderMarkdown(rawContent);
    window.scrollTo({ top: 0, behavior: 'instant' });
  } catch (err) {
    elements.articleContent.innerHTML = `
      <div style="padding: 40px 20px; text-align: center; color: var(--text-muted);">
        <h3>⚠️ 加载失败</h3>
        <p style="margin-top: 8px;">无法获取文档：${docPath}</p>
        <button onclick="location.reload()" class="footer-btn" style="max-width: 140px; margin: 16px auto 0;">重新加载</button>
      </div>
    `;
  }
}

/**
 * Render Markdown content, post-process tables and generate TOC
 */
function renderMarkdown(rawMd) {
  // Parse with marked
  const html = marked.parse(rawMd, {
    gfm: true,
    breaks: false
  });

  elements.articleContent.innerHTML = html;

  // Post-process: wrap tables for horizontal swipe
  elements.articleContent.querySelectorAll('table').forEach(table => {
    if (!table.parentElement.classList.contains('table-wrapper')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'table-wrapper';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  // Post-process: fix headings and extract in-page TOC
  buildPageToc();
}

/**
 * Build in-page TOC from H2 and H3 elements
 */
function buildPageToc() {
  const headings = elements.articleContent.querySelectorAll('h1, h2, h3');
  elements.tocSheetContent.innerHTML = '';

  if (headings.length === 0) {
    elements.tocSheetContent.innerHTML = '<div style="color:var(--text-muted); padding:10px;">本页暂无子标题</div>';
    return;
  }

  const tocList = document.createElement('div');

  headings.forEach((heading, idx) => {
    // If heading doesn't have an ID, assign one or check children spans
    let targetId = heading.id;
    const innerSpan = heading.querySelector('span[id]');
    if (innerSpan) {
      targetId = innerSpan.id;
    } else if (!targetId) {
      targetId = `heading-${idx}`;
      heading.id = targetId;
    }

    const tagName = heading.tagName.toLowerCase();
    if (tagName === 'h1') return; // Skip main doc title

    const item = document.createElement('a');
    item.className = `toc-item-link ${tagName === 'h2' ? 'toc-level-2' : 'toc-level-3'}`;
    item.textContent = heading.textContent.replace(/^[#\s]+/, '').trim();
    item.href = `#${targetId}`;

    item.addEventListener('click', (e) => {
      e.preventDefault();
      closeTocSheet();
      const targetEl = document.getElementById(targetId) || heading;
      if (targetEl) {
        const top = targetEl.getBoundingClientRect().top + window.pageYOffset - 70;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });

    tocList.appendChild(item);
  });

  elements.tocSheetContent.appendChild(tocList);
}

/**
 * Auto-polling: Check if Mac has updated current file
 */
function startPolling() {
  if (state.pollingTimer) clearInterval(state.pollingTimer);

  state.pollingTimer = setInterval(async () => {
    if (!state.isLocalServer || !state.currentPath || document.hidden) return;

    try {
      const res = await fetch(`/api/content?path=${encodeURIComponent(state.currentPath)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.mtime && state.currentMtime && data.mtime > state.currentMtime) {
          state.currentMtime = data.mtime;
          
          // Remember current scroll position
          const currentScroll = window.scrollY;

          // Re-render
          renderMarkdown(data.content);
          window.scrollTo({ top: currentScroll, behavior: 'instant' });

          // Show Toast
          showSyncToast();
        }
      }
    } catch (e) {
      // Ignore background network hiccups
    }
  }, 2500);
}

/**
 * Show Sync Toast Notification
 */
let toastTimeout = null;
function showSyncToast() {
  elements.syncToast.classList.add('visible');
  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    elements.syncToast.classList.remove('visible');
  }, 2800);
}

/**
 * Event Listeners Registration
 */
function initEventListeners() {
  // Drawer open / close
  elements.btnMenu.addEventListener('click', openDrawer);
  elements.btnCloseDrawer.addEventListener('click', closeDrawer);
  elements.drawerOverlay.addEventListener('click', closeDrawer);

  // Font Sheet toggle
  elements.btnFont.addEventListener('click', (e) => {
    e.stopPropagation();
    elements.fontSheet.classList.toggle('visible');
  });
  document.addEventListener('click', (e) => {
    if (!elements.fontSheet.contains(e.target) && e.target !== elements.btnFont) {
      elements.fontSheet.classList.remove('visible');
    }
  });

  // Font size buttons
  elements.fontDecrease.addEventListener('click', () => setFontSize(state.fontSize - 1));
  elements.fontIncrease.addEventListener('click', () => setFontSize(state.fontSize + 1));
  elements.fontReset.addEventListener('click', () => setFontSize(17));

  // Theme switch
  elements.btnTheme.addEventListener('click', cycleTheme);

  // Manual refresh
  elements.btnRefresh.addEventListener('click', () => {
    if (state.currentPath) {
      loadDocument(state.currentPath, false);
      showSyncToast();
    }
  });

  // QR Modal
  elements.btnQr.addEventListener('click', openQrModal);
  elements.btnShowQrMobile.addEventListener('click', () => {
    closeDrawer();
    openQrModal();
  });
  elements.btnCloseModal.addEventListener('click', closeQrModal);
  elements.qrModal.addEventListener('click', (e) => {
    if (e.target === elements.qrModal) closeQrModal();
  });

  // Copy URL button
  elements.btnCopyUrl.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(elements.qrUrlInput.value);
      const originalText = elements.btnCopyUrl.textContent;
      elements.btnCopyUrl.textContent = '已复制!';
      elements.btnCopyUrl.style.background = '#10b981';
      elements.btnCopyUrl.style.color = '#ffffff';
      setTimeout(() => {
        elements.btnCopyUrl.textContent = originalText;
        elements.btnCopyUrl.style.background = '';
        elements.btnCopyUrl.style.color = '';
      }, 2000);
    } catch (e) {
      elements.qrUrlInput.select();
      document.execCommand('copy');
      alert('已复制地址！');
    }
  });

  // TOC Bottom Sheet
  elements.btnPageToc.addEventListener('click', openTocSheet);
  elements.btnCloseToc.addEventListener('click', closeTocSheet);
  elements.tocOverlay.addEventListener('click', closeTocSheet);

  // Back to Top button
  elements.btnBackTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Scroll tracking (Progress bar + Back-to-top button visibility)
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    elements.progressBar.style.width = `${progress}%`;

    // Back to top button toggle
    if (scrollTop > 350) {
      elements.btnBackTop.classList.add('visible');
    } else {
      elements.btnBackTop.classList.remove('visible');
    }
  }, { passive: true });

  // Handle browser back/forward buttons
  window.addEventListener('hashchange', () => {
    const hashMatch = window.location.hash.match(/#doc=([^&]+)/);
    if (hashMatch && hashMatch[1]) {
      const docPath = decodeURIComponent(hashMatch[1]);
      if (docPath !== state.currentPath) {
        loadDocument(docPath, false);
      }
    }
  });
}

// Drawer Controls
function openDrawer() {
  elements.sidebarDrawer.classList.add('open');
  elements.drawerOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeDrawer() {
  elements.sidebarDrawer.classList.remove('open');
  elements.drawerOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

// TOC Sheet Controls
function openTocSheet() {
  elements.tocSheet.classList.add('open');
  elements.tocOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeTocSheet() {
  elements.tocSheet.classList.remove('open');
  elements.tocOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

// QR Modal Controls
function openQrModal() {
  elements.qrModal.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeQrModal() {
  elements.qrModal.classList.remove('open');
  document.body.style.overflow = '';
}
