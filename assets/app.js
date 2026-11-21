/* Pauwi Na — small helpers. Nothing typed here leaves the visitor's browser. */
(function () {
  'use strict';

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ---------- Checklist ---------- */
  var qBox = document.getElementById('questions');
  if (qBox) {
    var QS = [
      { id: 'filipino', text: 'Are you (or your spouse) a Filipino citizen coming home to live?', help: 'Dual citizens who re-acquired citizenship count. A dependent spouse and children are covered too.' },
      { id: 'six', text: 'Did you live abroad for at least 6 months straight?', help: 'Your passport stamps are the proof: your last departure from the Philippines and your latest arrival.' },
      { id: 'window', text: 'Will your shipment arrive within 60 days of the day you landed?', help: 'Count from YOUR arrival date, not the day the container shipped.' },
      { id: 'notice', text: 'Have you received an arrival notice from the shipping line?', help: 'Usually an email or PDF with the vessel name, ETA and bill of lading number.' },
      { id: 'bl', text: 'Do you have the original bill of lading, or a telex release?', help: 'An "Original" bill of lading must be signed on the back and handed over before the container is released.' },
      { id: 'list', text: 'Do you have an itemized list of your goods, with used values?', help: 'Customs wants every item and what it is worth today, not what you paid.' },
      { id: 'passport', text: 'Do you have copies of your passport photo page and stamps?', help: 'Photo page, plus the departure and arrival stamp pages.' },
      { id: 'tin', text: 'Do you have a TIN (Philippine tax ID)?', help: 'Needed for the customs declaration and for a duty-exemption request.' }
    ];
    var answers = {};
    var html = '';
    QS.forEach(function (q, i) {
      html += '<div class="q" role="group" aria-labelledby="ql-' + q.id + '"><div class="q-head"><span class="dotnum" aria-hidden="true">' + (i + 1) + '</span><span><strong id="ql-' + q.id + '">' + esc(q.text) + '</strong><span>' + esc(q.help) + '</span></span></div>' +
        '<div class="opts">' +
        ['yes', 'no', 'unsure'].map(function (v) {
          var label = v === 'yes' ? 'Yes' : v === 'no' ? 'No' : 'Not sure';
          return '<button type="button" class="opt" aria-pressed="false" data-q="' + q.id + '" data-v="' + v + '">' + label + '</button>';
        }).join('') + '</div></div>';
    });
    qBox.innerHTML = html;

    var out = document.getElementById('results');
    var bar = document.getElementById('bar');
    var count = document.getElementById('count');

    function add(list, tone, title, body) { list.push('<div class="result ' + tone + '"><strong>' + esc(title) + '</strong><span>' + body + '</span></div>'); }

    function render() {
      var a = answers, r = [];
      if (a.filipino === 'yes' && a.six === 'yes' && a.window === 'yes') add(r, 'good', 'You likely qualify for duty-free entry', 'Up to ₱150,000, ₱250,000 or ₱350,000 depending on how long you lived abroad. Apply to the DOF Revenue Office for a Tax Exemption Indorsement, and fill out the PHED form. <a href="chapter-3.html">Chapter 3</a>');
      else if (a.filipino === 'no') add(r, 'todo', 'Duties will probably apply', 'Plan for roughly 15% duty plus 12% VAT on the value customs assigns. Some visa holders (13A, SRRV, 9G and others) may qualify for an exemption, so check yours. <a href="costs.html">Estimate it</a>');
      if (a.six === 'no') add(r, 'warn', 'Under 6 months abroad', 'The returning-resident exemption needs at least 6 months abroad. Expect to pay duties.');
      if (a.window === 'no') add(r, 'warn', 'You may be past the 60-day window', 'There’s no written extension process, but you can still ask. Read <a href="chapter-3.html#missed">“What if I already missed it?”</a> before you pay anyone.');
      if (a.window === 'unsure') add(r, 'todo', 'Work out your 60-day date', 'Take your arrival stamp date and add 60 days. Compare it with the ETA on your arrival notice.');
      if (a.notice === 'no' || a.notice === 'unsure') add(r, 'todo', 'Get your arrival notice', 'Ask your forwarder (the company that picked up your goods) which shipping line has your container and the bill of lading number.');
      if (a.notice === 'yes') add(r, 'good', 'Arrival notice: done', 'Check the vessel ETA and the pick-up terminal. You have 15 days from unloading to file with customs. <a href="chapter-4.html">Chapter 4</a>');
      if (a.bl === 'no' || a.bl === 'unsure') add(r, 'warn', 'Chase your bill of lading now', 'This is what usually holds up release. Ask your forwarder to courier the original, or switch to a telex release.');
      if (a.list === 'no' || a.list === 'unsure') add(r, 'todo', 'Make your valued inventory', 'Type every item with a realistic used value, in plain words: “used 3-seat couch,” “framed prints (reproductions).” <a href="ai-helper.html">Our AI prompt can help</a>');
      if (a.passport === 'no' || a.passport === 'unsure') add(r, 'todo', 'Copy your passport pages', 'Photo page, plus the departure and arrival stamps.');
      if (a.tin === 'no' || a.tin === 'unsure') add(r, 'todo', 'Get a TIN', 'Register with the BIR. You’ll need it for the declaration and any exemption request.');
      var n = Object.keys(a).length;
      out.innerHTML = n ? r.join('') || '<p class="muted" style="margin:0">Looking good so far. Keep going.</p>' : '<p class="muted" style="margin:0">Start answering. Your personal to-do list builds here as you go.</p>';
      bar.style.width = Math.round(n / QS.length * 100) + '%';
      count.textContent = n + ' of ' + QS.length + ' answered';
    }

    qBox.addEventListener('click', function (e) {
      var b = e.target.closest('.opt'); if (!b) return;
      answers[b.dataset.q] = b.dataset.v;
      qBox.querySelectorAll('.opt[data-q="' + b.dataset.q + '"]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      render();
    });
    var reset = document.getElementById('reset');
    if (reset) reset.addEventListener('click', function () {
      answers = {};
      qBox.querySelectorAll('.opt').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      render(); window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    render();
  }

  /* ---------- Duty estimator ---------- */
  var range = document.getElementById('val');
  if (range) {
    var cap = 0;
    var peso = function (n) { return '₱' + Math.round(n).toLocaleString('en-US'); };
    var capBtns = document.querySelectorAll('[data-cap]');
    function calc() {
      var v = Number(range.value) || 0;
      var taxable = Math.max(0, v - cap), duty = taxable * 0.15, vat = (taxable + duty) * 0.12;
      document.getElementById('valText').textContent = peso(v);
      document.getElementById('taxable').textContent = peso(taxable);
      document.getElementById('duty').textContent = peso(duty);
      document.getElementById('vat').textContent = peso(vat);
      document.getElementById('total').textContent = peso(duty + vat);
    }
    range.addEventListener('input', calc);
    capBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        cap = Number(b.dataset.cap);
        capBtns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        calc();
      });
    });
    calc();
  }

  /* ---------- Copy prompt buttons ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var pre = document.getElementById(btn.dataset.copy);
      var text = pre ? pre.innerText : '';
      var done = function () { var t = btn.textContent; btn.textContent = 'Copied!'; setTimeout(function () { btn.textContent = t; }, 1600); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, function () { fallback(); });
      else fallback();
      function fallback() {
        var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* ---------- Glossary search ---------- */
  var gs = document.getElementById('gsearch');
  if (gs) {
    gs.addEventListener('input', function () {
      var q = gs.value.trim().toLowerCase();
      document.querySelectorAll('.term').forEach(function (t) {
        t.hidden = q && t.textContent.toLowerCase().indexOf(q) === -1;
      });
    });
  }
})();
