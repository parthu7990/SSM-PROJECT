/* ============================================================
   PSK FUTURE INNOVATION – Main JavaScript
============================================================ */

/* ---- PRELOADER ---- */
window.addEventListener('load', () => {
  setTimeout(() => {
    const p = document.getElementById('preloader');
    if (p) { p.style.opacity = '0'; setTimeout(() => p.remove(), 600); }
  }, 700);
});

/* ---- NAVBAR ---- */
const navbar    = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
const scrollTop = document.getElementById('scrollTop');

/* Overlay backdrop */
const navOverlay = document.createElement('div');
navOverlay.className = 'nav-overlay';
document.body.appendChild(navOverlay);

function openNav() {
  hamburger.classList.add('open');
  navLinks.classList.add('open');
  navOverlay.classList.add('show');
  document.body.classList.add('nav-open');
}

function closeNav() {
  hamburger.classList.remove('open');
  navLinks.classList.remove('open');
  navOverlay.classList.remove('show');
  document.body.classList.remove('nav-open');
  document.body.style.overflow = '';
}

hamburger && hamburger.addEventListener('click', e => {
  e.stopPropagation();
  navLinks.classList.contains('open') ? closeNav() : openNav();
});

navOverlay.addEventListener('click', closeNav);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });

/* ============================================================
   SCROLL TO SECTION — works on mobile & desktop
============================================================ */
function scrollToSection(id) {
  // First make sure body scroll is enabled
  document.body.style.overflow = '';
  document.body.style.position = '';

  const el = document.getElementById(id);
  if (!el) return;

  const navH = navbar ? navbar.offsetHeight + 10 : 80;
  const top  = el.getBoundingClientRect().top + window.pageYOffset - navH;

  window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
}

/* Wire EVERY anchor link */
document.addEventListener('click', function(e) {
  const link = e.target.closest('a[href^="#"]');
  if (!link) return;

  const href = link.getAttribute('href');
  if (!href || href === '#') return;

  const id = href.slice(1); // remove the '#'
  const target = document.getElementById(id);
  if (!target) return;

  e.preventDefault();

  if (navLinks && navLinks.classList.contains('open')) {
    // Close nav menu first, restore scroll, THEN scroll to section
    closeNav();
    setTimeout(() => scrollToSection(id), 350);
  } else {
    scrollToSection(id);
  }
});

/* Scroll events */
window.addEventListener('scroll', () => {
  navbar && navbar.classList.toggle('scrolled', window.scrollY > 80);
  scrollTop && scrollTop.classList.toggle('show', window.scrollY > 400);
  updateActiveNav();
}, { passive: true });

/* Highlight active nav link */
function updateActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 200) current = s.id;
  });
  document.querySelectorAll('.nav-link').forEach(l => {
    const href = l.getAttribute('href') || '';
    l.classList.toggle('active', href === '#' + current);
  });
}

scrollTop && scrollTop.addEventListener('click', () =>
  window.scrollTo({ top: 0, behavior: 'smooth' })
);

/* ---- HERO SLIDER ---- */
const slides  = document.querySelectorAll('.hero-slide');
const dots    = document.querySelectorAll('.dot');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
let current = 0;

function goToSlide(n) {
  if (!slides.length) return;
  slides[current].classList.remove('active');
  if (dots[current]) dots[current].classList.remove('active');
  current = (n + slides.length) % slides.length;
  slides[current].classList.add('active');
  if (dots[current]) dots[current].classList.add('active');
}

if (slides.length > 1) {
  function restart() { clearInterval(timer); timer = setInterval(() => goToSlide(current + 1), 6000); }
  let timer = setInterval(() => goToSlide(current + 1), 6000);
  prevBtn && prevBtn.addEventListener('click', () => { goToSlide(current - 1); restart(); });
  nextBtn && nextBtn.addEventListener('click', () => { goToSlide(current + 1); restart(); });
  dots.forEach((d, i) => d.addEventListener('click', () => { goToSlide(i); restart(); }));
}

/* ---- COUNTER ANIMATION ---- */
const cObs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting || entry.target.dataset.done) return;
    entry.target.dataset.done = '1';
    const target = parseInt(entry.target.dataset.target) || 0;
    let n = 0;
    const step = Math.max(1, Math.ceil(target / 60));
    (function tick() {
      n = Math.min(n + step, target);
      entry.target.textContent = Math.floor(n) + (target === 100 ? '%' : '+');
      if (n < target) requestAnimationFrame(tick);
    })();
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-num[data-target]').forEach(el => cObs.observe(el));

/* ---- TOAST ---- */
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.querySelector('.toast-icon').className =
    'toast-icon fas fa-' + (type === 'success' ? 'check-circle' : 'exclamation-circle');
  toast.querySelector('.toast-msg').textContent = msg;
  toast.className = 'toast show ' + type;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.remove('show'), 4500);
}
window.showToast = showToast;

/* ---- SERVICE TOGGLE ---- */
window.toggleService = function(btn) {
  const extra = btn.previousElementSibling;
  const open  = extra.style.display === 'block';
  extra.style.display = open ? 'none' : 'block';
  const m = btn.querySelector('span').textContent.match(/\d+/);
  btn.querySelector('span').textContent = open ? `Show all ${m ? m[0] : ''} features` : 'Hide features';
  btn.querySelector('i').style.transform = open ? 'rotate(0deg)' : 'rotate(180deg)';
};

/* ---- PARTICLES ---- */
const particlesEl = document.getElementById('particles');
if (particlesEl) {
  for (let i = 0; i < 18; i++) {
    const p = document.createElement('div');
    const s = Math.random() * 3 + 1;
    Object.assign(p.style, {
      position:'absolute', width:s+'px', height:s+'px', borderRadius:'50%',
      background:`rgba(99,102,241,${Math.random()*.3+.05})`,
      left:Math.random()*100+'%', top:Math.random()*100+'%',
      animation:`pfloat ${Math.random()*20+10}s linear infinite`,
      animationDelay:`-${Math.random()*20}s`, pointerEvents:'none',
    });
    particlesEl.appendChild(p);
  }
  const sty = document.createElement('style');
  sty.textContent = `@keyframes pfloat{0%{transform:translateY(0) rotate(0deg);opacity:.5}50%{transform:translateY(-60px) rotate(180deg);opacity:.1}100%{transform:translateY(0) rotate(360deg);opacity:.5}}`;
  document.head.appendChild(sty);
}

console.log('%c PSK Future Innovation FZE ', 'background:linear-gradient(135deg,#6366f1,#ec4899);color:#fff;font-size:16px;padding:8px 18px;border-radius:8px;font-weight:700;');
