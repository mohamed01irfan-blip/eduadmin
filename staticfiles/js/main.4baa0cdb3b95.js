/* EduAdmin - Main JavaScript */
document.addEventListener("DOMContentLoaded", function () {
// ===== SIDEBAR TOGGLE (MOBILE) =====
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    sidebarOverlay.classList.toggle('active');
  });
}

if (sidebarOverlay) {
  sidebarOverlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('active');
  });
}

// ===== AUTO-DISMISS ALERTS =====
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-8px)';
    setTimeout(() => alert.remove(), 500);
  }, 4000);
});

// ===== CONFIRM DELETE =====
function confirmDelete(formId) {
  const form = document.getElementById(formId);
  if (form) form.submit();
}

// ===== COUNTER ANIMATION =====
function animateCounter(el, end, duration = 1200) {
  let start = 0;
  const step = end / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= end) {
      el.textContent = end;
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(start);
    }
  }, 16);
}

// Animate all stat values
document.querySelectorAll('.stat-value-counter').forEach(el => {
  const val = parseInt(el.dataset.value || el.textContent, 10);
  if (!isNaN(val)) {
    el.textContent = '0';
    animateCounter(el, val); // direct run
  }
});

// ===== RIPPLE EFFECT ON BUTTONS =====
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const ripple = document.createElement('span');
    ripple.style.cssText = `
      position:absolute; border-radius:50%;
      background:rgba(255,255,255,0.2);
      width:10px; height:10px;
      transform:translate(-50%,-50%) scale(0);
      animation: ripple 0.5s ease;
      left:${x}px; top:${y}px; pointer-events:none;
        `;
    this.style.position = 'relative';
    this.style.overflow = 'hidden';
    this.style.willChange = 'transform';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});

// Add ripple keyframes dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes ripple {
    to { transform: translate(-50%,-50%) scale(20); opacity: 0; }
  }
`;
document.head.appendChild(style);

// ===== TABLE ROW HIGHLIGHT =====
document.querySelectorAll('.data-table tbody tr').forEach((row, i) => {
  row.style.opacity = '0';
  
  setTimeout(() => {
    row.style.transition = 'all 0.3s ease';
    row.style.opacity = '1';
    row.style.transform = 'translateY(0)';
  }, i * 40);
});
// ===== TOOLTIP (SIMPLE) =====
document.querySelectorAll('[data-tooltip]').forEach(el => {
  const tip = document.createElement('div');
  tip.className = 'tooltip-popup';
  tip.textContent = el.dataset.tooltip;
  tip.style.cssText = `
    position:absolute; background:rgba(20,21,35,0.95);
    border:1px solid rgba(255,255,255,0.1); border-radius:6px;
    padding:0.3rem 0.65rem; font-size:0.75rem; color:#fff;
    white-space:nowrap; z-index:200; pointer-events:none;
    opacity:0; transition:opacity 0.2s ease; bottom:calc(100%+6px); left:50%;
    transform:translateX(-50%);
  `;
  el.style.position = 'relative';
  el.appendChild(tip);
  el.addEventListener('mouseenter', () => tip.style.opacity = '1');
  el.addEventListener('mouseleave', () => tip.style.opacity = '0');
});
});
