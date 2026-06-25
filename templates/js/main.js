/* =========================================================
   main.js — IPTV PRO v3.0
   Vanilla JS | No dependencies
   Features: dark mode, popup notifications, FAQ, scroll, stats
   ========================================================= */

(function () {
  'use strict';

  /* ─── Dark / Light Mode ─── */
  const THEME_KEY = 'iptv_theme';
  const html = document.documentElement;

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    const btn = document.getElementById('darkToggle');
    if (btn) {
      btn.innerHTML = theme === 'dark' ? '<i data-lucide="sun" style="width:20px;height:20px;"></i>' : '<i data-lucide="moon" style="width:20px;height:20px;"></i>';
      if (typeof lucide !== 'undefined') {
        lucide.createIcons();
      }
    }
  }

  // Initialize: read saved theme or default to dark
  const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
  applyTheme(savedTheme);

  document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('darkToggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        const current = html.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        localStorage.setItem(THEME_KEY, next);
      });
    }

    /* ─── Navbar Scroll Effect ─── */
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      window.addEventListener('scroll', function () {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
      }, { passive: true });
    }

    /* ─── Hamburger / Mobile Menu ─── */
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    if (hamburger && mobileMenu) {
      hamburger.addEventListener('click', function () {
        hamburger.classList.toggle('open');
        mobileMenu.classList.toggle('open');
      });
      document.addEventListener('click', function (e) {
        if (!hamburger.contains(e.target) && !mobileMenu.contains(e.target)) {
          hamburger.classList.remove('open');
          mobileMenu.classList.remove('open');
        }
      });
    }

    /* ─── Smooth Scroll for Anchor Links ─── */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          if (hamburger) hamburger.classList.remove('open');
          if (mobileMenu) mobileMenu.classList.remove('open');
        }
      });
    });

    /* ─── FAQ Accordion ─── */
    document.querySelectorAll('.faq-question').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const item = btn.closest('.faq-item');
        const isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item.open').forEach(function (i) { i.classList.remove('open'); });
        if (!isOpen) item.classList.add('open');
      });
    });

    /* ─── Countdown Timer ─── */
    const countdownEl = document.getElementById('countdown');
    if (countdownEl) {
      let endTime = sessionStorage.getItem('ctEnd');
      if (!endTime) {
        endTime = Date.now() + 3 * 24 * 60 * 60 * 1000;
        sessionStorage.setItem('ctEnd', endTime);
      }
      endTime = parseInt(endTime);
      const dEl = document.getElementById('ct-days');
      const hEl = document.getElementById('ct-hours');
      const mEl = document.getElementById('ct-mins');
      const sEl = document.getElementById('ct-secs');
      function updateCountdown() {
        const rem = Math.max(0, endTime - Date.now());
        if (dEl) dEl.textContent = String(Math.floor(rem / 86400000)).padStart(2, '0');
        if (hEl) hEl.textContent = String(Math.floor((rem % 86400000) / 3600000)).padStart(2, '0');
        if (mEl) mEl.textContent = String(Math.floor((rem % 3600000) / 60000)).padStart(2, '0');
        if (sEl) sEl.textContent = String(Math.floor((rem % 60000) / 1000)).padStart(2, '0');
        if (rem > 0) setTimeout(updateCountdown, 1000);
      }
      updateCountdown();
    }

    /* ─── Stats Counter Animation ─── */
    function animateCounter(el) {
      const target = parseFloat(el.dataset.target);
      const isDecimal = el.dataset.decimal === 'true';
      const suffix = el.dataset.suffix || '';
      const duration = 2000;
      const start = performance.now();
      function update(now) {
        const ease = 1 - Math.pow(1 - Math.min((now - start) / duration, 1), 3);
        el.textContent = (isDecimal ? (ease * target).toFixed(1) : Math.floor(ease * target).toLocaleString()) + suffix;
        if (ease < 1) requestAnimationFrame(update);
      }
      requestAnimationFrame(update);
    }
    const statsObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { animateCounter(entry.target); statsObs.unobserve(entry.target); }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-target]').forEach(function (el) { statsObs.observe(el); });

    /* ─── Scroll Reveal ─── */
    const revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); revealObs.unobserve(entry.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { revealObs.observe(el); });

    /* ─── TOC Active Highlight ─── */
    const tocLinks = document.querySelectorAll('.toc-list a');
    if (tocLinks.length) {
      const headings = Array.from(document.querySelectorAll('.article-body h2[id]'));
      const tocObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            tocLinks.forEach(function (l) { l.classList.remove('active'); });
            const link = document.querySelector('.toc-list a[href="#' + entry.target.id + '"]');
            if (link) link.classList.add('active');
          }
        });
      }, { rootMargin: '-20% 0px -70% 0px' });
      headings.forEach(function (h) { tocObs.observe(h); });
    }

    /* ─── Progress Bar on Scroll ─── */
    const progressBar = document.getElementById('readProgress');
    if (progressBar) {
      window.addEventListener('scroll', function () {
        const docH = document.documentElement.scrollHeight - window.innerHeight;
        progressBar.style.width = (window.scrollY / docH * 100) + '%';
      }, { passive: true });
    }

    /* ─── Lazy Loading Images ─── */
    if ('IntersectionObserver' in window) {
      const imgObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const img = entry.target;
            if (img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
            imgObs.unobserve(img);
          }
        });
      }, { rootMargin: '200px 0px' });
      document.querySelectorAll('img[data-src]').forEach(function (img) { imgObs.observe(img); });
    }

    /* ─── Purchase Popup Notifications ─── */
    (function initPopup() {
      const names = [
        { initials: 'JD', name: 'John D.', flag: '🇺🇸' },
        { initials: 'SM', name: 'Sarah M.', flag: '🇨🇦' },
        { initials: 'MR', name: 'Mike R.', flag: '🇬🇧' },
        { initials: 'AL', name: 'Anna L.', flag: '🇺🇸' },
        { initials: 'KT', name: 'Kevin T.', flag: '🇨🇦' },
        { initials: 'PR', name: 'Paul R.', flag: '🇬🇧' },
        { initials: 'JW', name: 'James W.', flag: '🇺🇸' },
        { initials: 'LC', name: 'Laura C.', flag: '🇨🇦' },
        { initials: 'TN', name: 'Tom N.', flag: '🇬🇧' },
        { initials: 'DB', name: 'David B.', flag: '🇺🇸' },
        { initials: 'EM', name: 'Emily M.', flag: '🇨🇦' },
        { initials: 'RK', name: 'Ryan K.', flag: '🇬🇧' },
        { initials: 'AH', name: 'Alex H.', flag: '🇺🇸' },
        { initials: 'SP', name: 'Sophie P.', flag: '🇨🇦' },
        { initials: 'OB', name: 'Oliver B.', flag: '🇬🇧' },
        { initials: 'NC', name: 'Natalie C.', flag: '🇺🇸' },
        { initials: 'MS', name: 'Marcus S.', flag: '🇨🇦' },
        { initials: 'IT', name: 'Isabella T.', flag: '🇬🇧' },
        { initials: 'BF', name: 'Brandon F.', flag: '🇺🇸' },
        { initials: 'ZM', name: 'Zoe M.', flag: '🇨🇦' },
        { initials: 'CW', name: 'Charlie W.', flag: '🇬🇧' },
        { initials: 'HA', name: 'Hannah A.', flag: '🇺🇸' }
      ];
      const plans = ['1 Month Plan', '3 Months Plan', '6 Months Plan', '1 Year Plan'];
      const timeAgo = ['just now', '1 minute ago', '2 minutes ago', '3 minutes ago', '5 minutes ago', '8 minutes ago'];

      function randomItem(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

      var popup = document.getElementById('purchasePopup');
      if (!popup) {
        popup = document.createElement('div');
        popup.id = 'purchasePopup';
        popup.className = 'purchase-popup';
        popup.innerHTML =
          '<div class="pp-avatar" id="ppAvatar"></div>' +
          '<div class="pp-body">' +
            '<div class="pp-name" id="ppName"></div>' +
            '<div class="pp-action" id="ppAction"></div>' +
            '<div class="pp-time" id="ppTime"></div>' +
          '</div>' +
          '<div class="pp-green-dot"></div>' +
          '<button class="pp-close" id="ppClose" aria-label="Close">✕</button>';
        document.body.appendChild(popup);
      }

      var ppClose = document.getElementById('ppClose');
      if (ppClose) {
        ppClose.addEventListener('click', function () {
          popup.classList.remove('show');
        });
      }

      function showPopup() {
        var person = randomItem(names);
        var plan = randomItem(plans);
        var ago = randomItem(timeAgo);
        var avatarEl = document.getElementById('ppAvatar');
        var nameEl = document.getElementById('ppName');
        var actionEl = document.getElementById('ppAction');
        var timeEl = document.getElementById('ppTime');
        if (avatarEl) avatarEl.textContent = person.initials;
        if (nameEl) nameEl.textContent = person.flag + ' ' + person.name;
        if (actionEl) actionEl.textContent = 'just purchased the ' + plan + ' 🎉';
        if (timeEl) timeEl.textContent = ago;
        popup.classList.add('show');
        setTimeout(function () { popup.classList.remove('show'); }, 4000);
      }

      // First popup after 5 seconds, then every 15-20 seconds
      setTimeout(function loop() {
        showPopup();
        var next = 15000 + Math.random() * 5000; // 15-20 seconds
        setTimeout(loop, next);
      }, 5000);
    })();

  }); // end DOMContentLoaded

})();
