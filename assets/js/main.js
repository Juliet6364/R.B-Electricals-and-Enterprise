// R.B Electricals & Enterprises — site behaviour
(function () {
  var header = document.querySelector('.header');
  var nav = document.getElementById('nav');
  var btn = document.querySelector('.menu-btn');

  // Sticky header shadow
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 10); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.querySelector('.i-open').style.display = open ? 'none' : '';
      btn.querySelector('.i-close').style.display = open ? '' : 'none';
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); });
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // Scroll progress bar
  var bar = document.querySelector('.progress');
  if (bar) {
    var upd = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? window.scrollY / h : 0) + ')';
    };
    window.addEventListener('scroll', upd, { passive: true }); upd();
  }

  // Count-up numbers
  var nums = document.querySelectorAll('[data-count]');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function countUp(el) {
    var end = +el.getAttribute('data-count'), t0 = null, dur = 1400;
    if (reduce || end < 2) { el.textContent = end; return; }
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = '0'; requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (n) { co.observe(n); });
  }

  // Gallery filters + lightbox
  var gItems = Array.prototype.slice.call(document.querySelectorAll('.g-item'));
  document.querySelectorAll('.gf').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.gf').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      var f = b.getAttribute('data-filter');
      gItems.forEach(function (g) { g.classList.toggle('hide', f !== 'all' && g.getAttribute('data-cat') !== f); });
    });
  });
  var lb = document.getElementById('lightbox');
  if (lb && gItems.length) {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption'), idx = 0;
    function visible() { return gItems.filter(function (g) { return !g.classList.contains('hide'); }); }
    function show(i) {
      var v = visible(); if (!v.length) return;
      idx = (i + v.length) % v.length;
      lbImg.src = v[idx].getAttribute('href'); lbCap.textContent = v[idx].getAttribute('data-caption') || '';
    }
    gItems.forEach(function (g) {
      g.addEventListener('click', function (e) { e.preventDefault(); lb.hidden = false; show(visible().indexOf(g)); document.body.style.overflow = 'hidden'; });
    });
    function close() { lb.hidden = true; document.body.style.overflow = ''; }
    lb.querySelector('.lb-close').onclick = close;
    lb.querySelector('.lb-prev').onclick = function () { show(idx - 1); };
    lb.querySelector('.lb-next').onclick = function () { show(idx + 1); };
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(idx - 1); else if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  // Year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Quote form -> WhatsApp or Email (no server needed)
  var form = document.getElementById('quote-form');
  if (form) {
    function compose() {
      var f = form.elements;
      var lines = [
        'Hello R.B Electricals & Enterprises, I would like a quote.',
        '',
        'Name: ' + f.name.value.trim(),
        'Phone: ' + f.phone.value.trim(),
        f.email.value.trim() ? 'Email: ' + f.email.value.trim() : '',
        'Service: ' + f.service.value,
        f.location.value.trim() ? 'Site location: ' + f.location.value.trim() : '',
        '',
        f.message.value.trim()
      ];
      return lines.filter(function (l, i) { return l !== '' || i === 1 || i === 7; }).join('\n');
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      window.open('https://wa.me/918970772028?text=' + encodeURIComponent(compose()), '_blank', 'noopener');
    });
    var mailBtn = document.getElementById('quote-email');
    if (mailBtn) mailBtn.addEventListener('click', function () {
      if (!form.reportValidity()) return;
      window.location.href = 'mailto:rb.electricalsandenterprises@gmail.com?subject=' +
        encodeURIComponent('Quote request - ' + form.elements.service.value) +
        '&body=' + encodeURIComponent(compose());
    });
  }
})();
