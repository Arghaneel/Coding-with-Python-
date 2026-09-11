// Mobile nav toggle
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
  });

  navLinks.addEventListener('click', (e) => {
    if (e.target instanceof Element && e.target.matches('a.nav-link')) {
      navLinks.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// Smooth scroll offset fix for sticky header (native smooth via CSS)
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    if (!href) return;
    const target = document.querySelector(href);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.pushState(null, '', href);
  });
});

// Scroll spy to highlight active nav link
const sections = document.querySelectorAll('main section[id]');
const navAnchors = document.querySelectorAll('.nav-link');

const sectionById = {};
sections.forEach((s) => sectionById[s.id] = s);

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navAnchors.forEach((a) => {
        const href = a.getAttribute('href');
        a.classList.toggle('active', href === `#${id}`);
      });
    }
  });
}, { rootMargin: '-40% 0px -55% 0px', threshold: [0, 0.25, 0.6, 1] });

sections.forEach((sec) => observer.observe(sec));

// Accordion behavior
const accordions = document.querySelectorAll('.accordion-item');
accordions.forEach((item) => {
  const header = item.querySelector('.accordion-header');
  const panel = item.querySelector('.accordion-panel');
  if (!header || !panel) return;

  header.addEventListener('click', () => {
    const expanded = header.getAttribute('aria-expanded') === 'true';
    // Close others
    accordions.forEach((other) => {
      if (other !== item) {
        const h = other.querySelector('.accordion-header');
        const p = other.querySelector('.accordion-panel');
        if (h && p) {
          h.setAttribute('aria-expanded', 'false');
          p.hidden = true;
        }
      }
    });
    // Toggle this
    header.setAttribute('aria-expanded', String(!expanded));
    panel.hidden = expanded;
  });
});

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear().toString();