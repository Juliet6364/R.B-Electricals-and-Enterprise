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
