// RB Assistant: instant answers to common customer questions, with WhatsApp / call handoff.
(function () {
  var PHONE = '+91 89707 72028', TEL = 'tel:+918970772028', WA = 'https://wa.me/918970772028';
  var EMAIL = 'rb.electricalsandenterprises@gmail.com';
  var MAP = 'https://www.google.com/maps/dir/?api=1&destination=Ropena+Agrahara,+Bengaluru,+Karnataka+560068';

  var KB = [
    { k: ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good evening'],
      a: 'Hello! 👋 How can I help you today? You can ask about our services, licence, location or getting a quote.' },
    { k: ['service', 'services', 'what do you do', 'offer', 'work do you'],
      a: 'We offer 9 services under one roof:<br>• Interior Fit-Out & Furnishing<br>• Civil & Partition Works<br>• False Ceiling & POP<br>• Electrical Works – HT & LT<br>• Lighting & Power Systems<br>• LAN / CCTV / Wi-Fi<br>• UPS & Power Distribution<br>• Painting & Finishing<br>• Turnkey Project Execution<br><a href="/services">See all services →</a>' },
    { k: ['licen', 'certif', 'class 1', 'class-1', 'class i', 'govt', 'government', 'approved', 'registered'],
      a: 'Yes, we are a <b>Government Certified Class-1 Licensed Electrical Contractor</b> (Licence No. 57/8, K No. 492492). We are a registered business with GSTIN 29ASLPV0247P1ZU.' },
    { k: ['price', 'cost', 'quote', 'quotation', 'estimate', 'rate', 'charges', 'budget', 'how much', 'boq'],
      a: 'Every project is different, so we share a <b>detailed BOQ</b> with transparent pricing after understanding your requirement. <a href="/contact#quote">Request a free quote →</a> or WhatsApp us your details.' },
    { k: ['where', 'location', 'address', 'located', 'office', 'map', 'direction'],
      a: 'We are at <b>No 57/8, K No 492492, Ropena Agrahara, Bengaluru – 560068</b>. <a href="' + MAP + '" target="_blank" rel="noopener">Get directions →</a>' },
    { k: ['area', 'serve', 'bangalore', 'bengaluru', 'city', 'come to', 'outside'],
      a: 'We take up commercial, corporate and residential projects across <b>Bengaluru</b>. For sites outside Bengaluru, please call or WhatsApp us to discuss.' },
    { k: ['contact', 'phone', 'call', 'number', 'mobile', 'reach', 'talk'],
      a: 'You can call us on <a href="tel:+918970772028">89707 72028</a>, <a href="tel:+919494514228">94945 14228</a> or <a href="tel:+919535688541">95356 88541</a>, or email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>.' },
    { k: ['email', 'mail'], a: 'Our email is <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>.' },
    { k: ['client', 'worked', 'customers', 'companies', 'portfolio', 'previous', 'project'],
      a: 'We have delivered interior & electrical works for companies like Acko Technology, Great Learning, Enyzme Office Spaces, Ellisys India, UV (Inchnmile), GoPro Ventures, Work Square, iEnergizer, Chin Design and Vishwaa Apparels. <a href="/projects">View projects →</a>' },
    { k: ['turnkey', 'complete', 'end to end', 'full project', 'everything'],
      a: 'Yes! With <b>turnkey execution</b>, one team handles planning, civil, interiors, electrical, networking and finishing, and hands over a ready-to-use space. You deal with a single point of contact.' },
    { k: ['ht', 'lt', 'panel', 'wiring', 'electric', 'cabling', 'earthing', 'transformer', 'db'],
      a: 'We handle <b>HT & LT electrical works</b>: panels and distribution boards, cabling, internal wiring, earthing and protection, all as a licensed Class-1 contractor.' },
    { k: ['interior', 'furniture', 'workstation', 'cabin', 'fit out', 'fit-out', 'office setup', 'design'],
      a: 'We do complete <b>interior fit-outs</b>: workstations, cabins, reception, pantry, modular furniture and soft furnishing for offices, commercial spaces and homes.' },
    { k: ['ceiling', 'pop', 'gypsum', 'grid'], a: 'We build <b>false ceilings</b> in gypsum, grid/mineral fibre and decorative POP, with integrated cove and feature lighting.' },
    { k: ['partition', 'civil', 'flooring', 'tile', 'masonry', 'glass'], a: 'Our <b>civil & partition</b> team handles gypsum, board and glass partitions, block work, plastering, flooring and tiling.' },
    { k: ['cctv', 'camera', 'lan', 'network', 'wifi', 'wi-fi', 'internet', 'access control'], a: 'We install <b>LAN cabling, network racks, CCTV surveillance, Wi-Fi access points</b> and access control.' },
    { k: ['ups', 'power backup', 'inverter', 'backup'], a: 'We install <b>UPS systems</b> with dedicated distribution so critical equipment keeps running during power cuts.' },
    { k: ['paint', 'texture', 'polish', 'finishing'], a: 'Our <b>painting & finishing</b> team does interior and exterior painting, textures, feature walls and wood polish.' },
    { k: ['light', 'led', 'lamp'], a: 'We design and install efficient <b>LED, panel, cove and feature lighting</b> along with power points and floor boxes.' },
    { k: ['home', 'house', 'residential', 'apartment', 'villa', 'flat'], a: 'Yes, we do <b>residential</b> work too: safe wiring, lighting, false ceilings, painting and complete interiors for homes and apartments.' },
    { k: ['time', 'how long', 'duration', 'deadline', 'days', 'weeks'], a: 'Timelines depend on the size of the project. We plan a clear schedule upfront and are committed to <b>on-time handover</b>. Share your requirement and we will give you an estimate.' },
    { k: ['gst', 'pan', 'invoice'], a: 'GSTIN: <b>29ASLPV0247P1ZU</b><br>PAN: <b>ASLPV0247P</b>' },
    { k: ['repair', 'small work', 'maintenance', 'fault', 'short circuit'], a: 'For repairs or small jobs, please call or WhatsApp us with details and photos so we can check and get back to you.' },
    { k: ['thank', 'thanks', 'ok', 'okay', 'great'], a: 'You are welcome! 😊 Anything else I can help with?' }
  ];
  var CHIPS = ['Our services', 'Are you licensed?', 'Get a quote', 'Where are you located?', 'Contact numbers'];

  function norm(s) { return (' ' + s.toLowerCase().replace(/[^a-z0-9\- ]/g, ' ').replace(/\s+/g, ' ') + ' '); }
  function answer(q) {
    var t = norm(q), best = null, score = 0;
    KB.forEach(function (e) {
      var s = 0;
      e.k.forEach(function (k) {
        var kk = k.length <= 3 ? ' ' + k + ' ' : k;
        if (t.indexOf(kk) > -1) s += k.length > 3 ? 2 : 1;
      });
      if (s > score) { score = s; best = e; }
    });
    if (best) return best.a;
    return 'I am not sure about that one. Our team can help you directly:';
  }

  // ---- UI
  var root = document.createElement('div');
  root.className = 'rbchat';
  root.innerHTML =
    '<button class="rbc-launch" aria-label="Chat with RB Assistant" aria-expanded="false">' +
      '<span class="rbc-dot"></span><svg viewBox="0 0 24 24" class="icon"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 10h.01M12 10h.01M16 10h.01"/></svg><span class="rbc-label">Ask us</span></button>' +
    '<div class="rbc-panel" role="dialog" aria-label="RB Assistant" hidden>' +
      '<div class="rbc-head"><img src="/assets/img/logo-mark.png" alt=""><div><b>RB Assistant</b><span><i></i>Typically replies instantly</span></div><button class="rbc-x" aria-label="Close chat">×</button></div>' +
      '<div class="rbc-body" aria-live="polite"></div>' +
      '<div class="rbc-chips"></div>' +
      '<form class="rbc-form"><input type="text" placeholder="Type your question…" aria-label="Your question" autocomplete="off"><button aria-label="Send"><svg viewBox="0 0 24 24" class="icon"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4z"/></svg></button></form>' +
    '</div>';
  document.body.appendChild(root);

  var launch = root.querySelector('.rbc-launch'), panel = root.querySelector('.rbc-panel'),
      body = root.querySelector('.rbc-body'), chips = root.querySelector('.rbc-chips'),
      form = root.querySelector('.rbc-form'), input = form.querySelector('input'), started = false;

  function add(html, who) {
    var m = document.createElement('div');
    m.className = 'rbc-msg ' + who;
    m.innerHTML = html;
    body.appendChild(m);
    body.scrollTop = body.scrollHeight;
    return m;
  }
  function handoff() {
    return '<div class="rbc-actions"><a class="rbc-btn wa" href="' + WA + '" target="_blank" rel="noopener">WhatsApp us</a><a class="rbc-btn call" href="' + TEL + '">Call ' + PHONE + '</a></div>';
  }
  function reply(q) {
    add(q.replace(/</g, '&lt;'), 'me');
    var typing = add('<span class="rbc-typing"><i></i><i></i><i></i></span>', 'bot');
    setTimeout(function () {
      var a = answer(q);
      var fallback = a.indexOf('not sure') > -1;
      typing.innerHTML = a + (fallback || /quote|price|cost|contact|call/i.test(q) ? handoff() : '');
      body.scrollTop = body.scrollHeight;
    }, 650);
  }
  function renderChips() {
    chips.innerHTML = '';
    CHIPS.forEach(function (c) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = c;
      b.onclick = function () { reply(c); };
      chips.appendChild(b);
    });
  }
  function open() {
    panel.hidden = false; launch.setAttribute('aria-expanded', 'true'); root.classList.add('open');
    if (!started) {
      started = true;
      add('Hi! 👋 I am the <b>RB Assistant</b>. Ask me about our services, licence, location or getting a quote.', 'bot');
      renderChips();
    }
    setTimeout(function () { input.focus(); }, 50);
  }
  function close() { panel.hidden = true; launch.setAttribute('aria-expanded', 'false'); root.classList.remove('open'); }
  launch.onclick = function () { panel.hidden ? open() : close(); };
  root.querySelector('.rbc-x').onclick = close;
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = input.value.trim(); if (!q) return;
    input.value = ''; reply(q);
  });
})();
