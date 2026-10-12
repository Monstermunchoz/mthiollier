/* M. Thiollier Conseils — scripts partagés (aucune dépendance) */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- En-tête : filet au défilement ---------- */
  var hdr = $('.site-header');
  if (hdr) { var onS = function () { hdr.classList.toggle('scrolled', window.scrollY > 8); }; window.addEventListener('scroll', onS, { passive: true }); onS(); }

  /* ---------- Bouton rendez-vous flottant ---------- */
  var fab = $('#fab');
  if (fab) {
    if (/rendez-vous(\.html)?$/.test(location.pathname)) { fab.remove(); }
    else {
      document.body.classList.add('has-fab');
      var hero = $('.hero, .page-head, .art-head');
      var limit = hero ? hero.offsetTop + hero.offsetHeight - 80 : 400;
      var ctaBox = $('.cta-box');
      var onF = function () {
        var y = window.scrollY, show = y > limit;
        if (ctaBox) { var r = ctaBox.getBoundingClientRect(); if (r.top < window.innerHeight && r.bottom > 0) show = false; }
        fab.classList.toggle('show', show);
      };
      window.addEventListener('scroll', onF, { passive: true }); window.addEventListener('resize', onF); onF();
    }
  }

  /* ---------- Menu mobile ---------- */
  var burger = $('#burger'), links = $('#links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      var o = links.classList.toggle('open');
      burger.setAttribute('aria-expanded', o);
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { links.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* ---------- Onglets "Vous êtes" ---------- */
  var tabs = $$('.tab'), panels = $$('.panel[data-panel]');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t); });
      panels.forEach(function (p) { p.hidden = p.dataset.panel !== t.dataset.p; });
    });
  });

  /* ---------- Simulateur ---------- */
  var sim = $('#sim');
  if (sim) {
    var ans = {}, step = 0, TOTAL = 4;
    var prev = $('#sim-prev'), next = $('#sim-next'), count = $('#sim-count');
    var bars = $$('.progress i', sim);
    $$('.opts', sim).forEach(function (g) {
      g.addEventListener('click', function (e) {
        var b = e.target.closest('.opt'); if (!b) return;
        $$('.opt', g).forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true'); ans[g.dataset.key] = b.dataset.v; next.disabled = false;
      });
    });
    var show = function () {
      $$('[data-step]', sim).forEach(function (s) { s.hidden = +s.dataset.step !== step; });
      bars.forEach(function (b, i) { b.classList.toggle('on', i <= Math.min(step, TOTAL - 1)); });
      prev.disabled = step === 0;
      if (step < TOTAL) {
        var key = $('[data-step="' + step + '"] .opts', sim).dataset.key;
        next.disabled = !ans[key]; next.textContent = step === TOTAL - 1 ? 'Voir mon orientation' : 'Suivant';
        count.textContent = (step + 1) + ' / ' + TOTAL;
      } else { next.textContent = 'Recommencer'; next.disabled = false; count.textContent = 'Résultat'; render(); }
    };
    next.addEventListener('click', function () {
      if (step >= TOTAL) { ans = {}; step = 0; $$('.opt', sim).forEach(function (o) { o.setAttribute('aria-pressed', 'false'); }); show(); return; }
      step++; show();
    });
    prev.addEventListener('click', function () { if (step > 0) { step--; show(); } });

    var render = function () {
      var t = $('#r-title'), x = $('#r-text'), l = $('#r-list');
      var recos = [], title = '', text = '';
      var ir = +ans.ir, o = ans.obj, h = ans.horizon, p = ans.pro;
      if (o === 'fisc' || ir >= 2) {
        title = 'La fiscalité est votre premier levier.';
        text = 'Avec un impôt significatif, chaque euro déduit ou réduit améliore directement le rendement de votre épargne. Nous commencerons par là.';
        recos.push(['PER individuel', 'Versements déductibles du revenu imposable' + (p === 'liberal' || p === 'dirigeant' ? ', plafond majoré pour les indépendants' : '') + '.']);
        if (h !== 'court') recos.push(['Investissement immobilier', 'Dispositifs immobiliers adaptés à votre tranche d\u2019imposition.']);
        if (p === 'dirigeant') recos.push(['Optimisation de la rémunération', 'Arbitrage entre rémunération et dividendes selon votre statut.']);
      } else if (o === 'revenus') {
        title = 'Construire des revenus réguliers sans gestion.';
        text = 'Vous cherchez des compléments de revenus prévisibles. La priorité est un socle immobilier mutualisé, complété par des supports plus souples.';
        recos.push(['SCPI de rendement', 'Revenus trimestriels, diversification immobilière, en direct ou via assurance-vie.']);
        recos.push(['Assurance-vie avec retraits programmés', 'Fiscalité allégée après huit ans, capital disponible.']);
        if (p === 'retraite') recos.push(['Transmission', 'Préparer la transmission de votre patrimoine dans les meilleures conditions.']);
      } else if (o === 'transmettre') {
        title = 'Transmettre dans les meilleures conditions.';
        text = 'Anticiper la transmission permet souvent de diviser les droits par deux ou plus. Les outils dépendent de votre âge, de vos bénéficiaires et de la nature des actifs.';
        recos.push(['Assurance-vie', 'Transmission hors succession, abattement de 152 500 € par bénéficiaire pour les versements avant 70 ans.']);
        recos.push(['Donation', 'Abattements renouvelables tous les quinze ans pour transmettre de votre vivant.']);
        if (p === 'dirigeant') recos.push(['Statuts et montage juridique', 'Organiser le patrimoine professionnel en vue de sa transmission.']);
      } else {
        title = h === 'court' ? 'Sécuriser d’abord, investir ensuite.' : 'Mettre en place une épargne qui compose dans le temps.';
        text = h === 'court' ? 'Sur moins de trois ans, l’objectif est de préserver le capital tout en préparant la suite.' : 'Votre horizon vous permet d’accepter des variations à court terme pour viser un rendement supérieur sur la durée.';
        if (h === 'court') { recos.push(['Fonds euros et supports monétaires', 'Capital garanti, disponibilité immédiate.']); recos.push(['Épargne programmée', 'Préparer l’investissement de demain sans y renoncer.']); }
        else { recos.push(['Assurance-vie', 'Répartition progressive entre fonds euros, unités de compte et SCPI.']); recos.push(['Immobilier et SCPI', 'Se constituer un patrimoine immobilier, en direct ou en SCPI.']); if (h === 'long') recos.push(['Investissement responsable', 'Supports labellisés sur un horizon long.']); }
      }
      if (ir === 0 && o === 'fisc') { title = 'Peu d’impôt : visons le rendement plutôt que la déduction.'; text = 'Sans impôt à réduire, les dispositifs de défiscalisation perdent leur intérêt. Nous privilégierons la constitution d’un capital.'; recos = [['Assurance-vie', 'Le socle de toute stratégie patrimoniale.'], ['Optimisation de l\u2019épargne', 'Un effort d\u2019épargne régulier adapté à votre budget.']]; }
      t.textContent = title; x.textContent = text; l.innerHTML = '';
      recos.forEach(function (r) {
        var li = document.createElement('li');
        li.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-top:2px;color:var(--ok)"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg><div><b></b><br><span></span></div>';
        li.querySelector('b').textContent = r[0]; li.querySelector('span').textContent = r[1]; l.appendChild(li);
      });
      try { var link = $('#r-link'); if (link) link.href = '/rendez-vous?objet=' + encodeURIComponent(o || ''); } catch (e) {}
    };
  }

  /* ---------- Boutons copier ---------- */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.dataset.copy, done = function () { var o = b.textContent; b.textContent = 'Copié'; setTimeout(function () { b.textContent = o; }, 1500); };
      var sel = function () { var el = b.previousElementSibling; if (!el) return; var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(done, sel); else sel();
    });
  });

  /* ---------- Formulaires (contact, rendez-vous, candidature) ----------
     Envoi : les champs sont POSTés en JSON vers /api/send (fonction Vercel, SMTP). */
  var validators = {
    nom: function (v) { return v.trim().length >= 2 || 'Indiquez votre nom.'; },
    tel: function (v) { return /^(\+33|0)\s?[1-9]([\s.-]?\d{2}){4}$/.test(v.trim()) || 'Numéro français attendu, ex. 06 12 34 56 78.'; },
    email: function (v) { return /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v.trim()) || 'Adresse e-mail invalide.'; }
  };
  $$('form[data-form]').forEach(function (form) {
    var endpoint = form.dataset.endpoint || '';
    var mailto = form.dataset.mailto || 'mickael@mthiollierconseils.fr';
    var fields = $$('[data-validate]', form);
    var check = function (el, live) {
      var fn = validators[el.dataset.validate]; if (!fn) return true;
      var r = el.required || el.value ? fn(el.value) : true;
      var err = el.closest('label, .fieldset') ? $('.err', el.closest('label, .fieldset')) : null;
      if (r === true) { el.setAttribute('aria-invalid', 'false'); if (err) err.textContent = ''; return true; }
      if (!live || el.dataset.touched) { el.setAttribute('aria-invalid', 'true'); if (err) err.textContent = r; }
      return false;
    };
    fields.forEach(function (el) {
      el.addEventListener('blur', function () { el.dataset.touched = '1'; check(el); });
      el.addEventListener('input', function () { check(el, true); });
    });
    /* Brouillon local (confort, jamais transmis) */
    var key = 'mt-' + form.dataset.form;
    try { var d = JSON.parse(localStorage.getItem(key) || '{}'); Object.keys(d).forEach(function (k) { var el = form.elements[k]; if (el && !el.value && el.type !== 'checkbox' && el.type !== 'radio') el.value = d[k]; }); } catch (e) {}
    form.addEventListener('input', function () {
      try { var o = {}; $$('input[type=text],input[type=tel],input[type=email],textarea', form).forEach(function (el) { if (el.name && el.name !== 'website') o[el.name] = el.value; }); localStorage.setItem(key, JSON.stringify(o)); } catch (e) {}
    });
    /* Préremplissage depuis l'URL (?objet=…) */
    try { var qs = new URLSearchParams(location.search); var ob = qs.get('objet'); if (ob) { var r = form.querySelector('input[name="objet"][value="' + ob + '"]'); if (r) r.checked = true; } } catch (e) {}

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; /* pot de miel anti-spam */
      var ok = true, first = null;
      fields.forEach(function (el) { el.dataset.touched = '1'; if (!check(el)) { ok = false; first = first || el; } });
      if (!ok) { first.focus(); return; }
      var btn = $('[type=submit]', form); btn.disabled = true; var old = btn.textContent; btn.textContent = 'Envoi…';
      var data = {}; new FormData(form).forEach(function (v, k) { if (k === 'website') return; data[k] = data[k] ? data[k] + ', ' + v : v; });
      data._page = location.pathname; data._date = new Date().toISOString();
      data._subject = form.dataset.subject || 'Demande via le site';
      var fail = $('.form-fail', form);
      if (!fail) { fail = document.createElement('p'); fail.className = 'form-fail'; fail.setAttribute('role', 'alert'); btn.parentNode.insertBefore(fail, btn.nextSibling); }
      fail.textContent = '';
      var finish = function () {
        var done = $('[data-done]', form) || $('#' + form.dataset.form + '-done');
        var body = $('[data-body]', form);
        if (body) body.hidden = true;
        if (done) {
          done.hidden = false;
          var recap = $('[data-recap]', done);
          if (recap) { recap.innerHTML = ''; ['nom', 'tel', 'email', 'objet', 'creneau'].forEach(function (k) { if (data[k]) { var p = document.createElement('div'); var b = document.createElement('b'); b.textContent = ({ nom: 'Nom', tel: 'Téléphone', email: 'E-mail', objet: 'Objet', creneau: 'Créneau' })[k] + ' : '; p.appendChild(b); p.appendChild(document.createTextNode(data[k])); recap.appendChild(p); } }); }
          done.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        try { localStorage.removeItem(key); } catch (e) {}
        btn.textContent = old; btn.disabled = false;
      };
      var failed = function () {
        btn.textContent = old; btn.disabled = false;
        fail.textContent = "L'envoi n'a pas abouti. Réessayez dans un instant ou écrivez à " + mailto + '.';
      };
      fetch(endpoint || '/api/send', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { if (r.ok) finish(); else failed(); }).catch(failed);
    });
  });

  /* ---------- Rendez-vous : assistant en 3 étapes ---------- */
  var rdv = $('#rdv');
  if (rdv) {
    var steps = $$('.wz-step', rdv), cur = 0;
    var ind = $$('.wz-steps li', rdv), bar = $('.wz-bar i', rdv);
    var prevB = $('[data-wz-prev]', rdv), nextB = $('[data-wz-next]', rdv), subB = $('[data-wz-submit]', rdv);
    var go = function (n) {
      cur = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (st, i) { st.hidden = i !== cur; });
      ind.forEach(function (li, i) { li.classList.toggle('on', i === cur); li.classList.toggle('done', i < cur); });
      if (bar) bar.style.width = ((cur + 1) / steps.length * 100) + '%';
      prevB.hidden = cur === 0;
      nextB.hidden = cur === steps.length - 1;
      subB.hidden = cur !== steps.length - 1;
      var f = $('input, textarea', steps[cur]);
      if (cur === steps.length - 1 && f) setTimeout(function () { f.focus({ preventScroll: true }); }, 50);
      var top = rdv.getBoundingClientRect().top;
      if (top < 0) rdv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    nextB.addEventListener('click', function () { go(cur + 1); });
    prevB.addEventListener('click', function () { go(cur - 1); });
    /* Entrée dans un champ texte des étapes 1-2 : passer à la suite */
    rdv.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && cur < steps.length - 1 && e.target.tagName !== 'TEXTAREA') { e.preventDefault(); go(cur + 1); }
    });
    var mode = $$('input[name="format"]', rdv), cren = $('#creneau-wrap');
    var upd = function () { var v = (mode.filter(function (m) { return m.checked; })[0] || {}).value; if (cren) cren.hidden = false; };
    mode.forEach(function (m) { m.addEventListener('change', upd); }); upd();
    go(0);
  }

  /* ---------- Sommaire d'article : section active ---------- */
  var toc = $('.toc ol');
  if (toc && 'IntersectionObserver' in window) {
    var map = {}; $$('a', toc).forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { $$('a', toc).forEach(function (a) { a.classList.remove('on'); }); var a = map[en.target.id]; if (a) a.classList.add('on'); } });
    }, { rootMargin: '-80px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) io.observe(h); });
  }

  /* ---------- Actualités : filtre par catégorie ---------- */
  var filters = $$('.filters .tab');
  if (filters.length) {
    filters.forEach(function (f) {
      f.addEventListener('click', function () {
        filters.forEach(function (x) { x.setAttribute('aria-selected', x === f); });
        var c = f.dataset.cat;
        $$('.post').forEach(function (p) { p.hidden = !(c === 'all' || p.dataset.cat === c); });
      });
    });
  }
})();

/* Barre de progression de lecture (articles) */
(function () {
  var bar = document.querySelector('.read-progress i'); if (!bar) return;
  var art = document.querySelector('.art-body'); var raf = 0;
  var upd = function () { raf = 0; var r = art.getBoundingClientRect(); var p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight))); bar.style.transform = 'scaleX(' + p + ')'; };
  addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(upd); }, { passive: true }); upd();
})();
