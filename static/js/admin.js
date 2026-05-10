/* ============================================================
   SSM Custom Admin Panel — JavaScript
============================================================ */

/* ---- Sidebar mobile toggle with overlay ---- */
(function () {
  const sidebar  = document.querySelector('.admin-sidebar');
  const main     = document.querySelector('.admin-main');
  if (!sidebar) return;

  // Create toggle button
  const toggleBtn = document.createElement('button');
  toggleBtn.className = 'sidebar-toggle';
  toggleBtn.setAttribute('aria-label', 'Toggle menu');
  toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
  document.body.appendChild(toggleBtn);

  // Create overlay backdrop
  const overlay = document.createElement('div');
  overlay.className = 'admin-sidebar-overlay';
  document.body.appendChild(overlay);

  function openSidebar() {
    sidebar.classList.add('active');
    overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
    toggleBtn.innerHTML = '<i class="fas fa-times"></i>';
  }

  function closeSidebar() {
    sidebar.classList.remove('active');
    overlay.classList.remove('show');
    document.body.style.overflow = '';
    toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
  }

  toggleBtn.addEventListener('click', () => {
    sidebar.classList.contains('active') ? closeSidebar() : openSidebar();
  });

  overlay.addEventListener('click', closeSidebar);

  // Close on escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSidebar();
  });

  // Close sidebar on nav link click (mobile)
  sidebar.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 1024) closeSidebar();
    });
  });
})();

/* ---- Auto-dismiss alerts after 4s ---- */
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.transition = 'opacity 0.5s ease, max-height 0.5s ease, padding 0.5s ease';
    alert.style.opacity    = '0';
    alert.style.maxHeight  = '0';
    alert.style.padding    = '0';
    alert.style.overflow   = 'hidden';
    setTimeout(() => alert.remove(), 550);
  }, 4000);
});

/* ---- Image preview on file input ---- */
document.querySelectorAll('input[type="file"]').forEach(input => {
  input.addEventListener('change', function () {
    const file = this.files[0];
    if (!file || !file.type.startsWith('image/')) return;
    let preview = this.parentElement.querySelector('.img-preview');
    if (!preview) {
      preview = document.createElement('img');
      preview.className = 'img-preview';
      this.parentElement.appendChild(preview);
    }
    preview.src = URL.createObjectURL(file);
  });
});

/* ---- Stats counter animation on dashboard ---- */
document.querySelectorAll('.stat-card h3').forEach(el => {
  const target = parseInt(el.textContent);
  if (isNaN(target) || target === 0) return;
  let current = 0;
  const step  = Math.max(1, Math.ceil(target / 60));
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current;
    if (current >= target) clearInterval(timer);
  }, 20);
});

/* ---- Highlight active sidebar link ---- */
const currentPath = window.location.pathname;
document.querySelectorAll('.sidebar-menu a').forEach(link => {
  const href = link.getAttribute('href');
  if (href && href !== '#' && currentPath.startsWith(href) && href.length > 1) {
    link.classList.add('active');
  }
});

/* ---- Table row click (navigate to detail) ---- */
document.querySelectorAll('.admin-table tbody tr').forEach(row => {
  const link = row.querySelector('a.btn');
  if (!link) return;
  row.style.cursor = 'pointer';
  row.addEventListener('click', e => {
    if (!e.target.closest('a, button, select, input')) {
      link.click();
    }
  });
});

/* ---- Confirm delete ---- */
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', e => {
    if (!confirm(el.dataset.confirm || 'Are you sure?')) e.preventDefault();
  });
});

console.log('%c SSM Admin ', 'background:#6366f1;color:#fff;padding:5px 12px;border-radius:6px;font-weight:700;');
