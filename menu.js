/* Menu mobile — partagé par toutes les pages. */
(function () {
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('mobileNav');
  if (!toggle || !nav) return;

  var plus = [].slice.call(nav.querySelectorAll('.m-plus'));

  function replier() {
    plus.forEach(function (b) {
      b.setAttribute('aria-expanded', 'false');
      var sous = document.getElementById(b.getAttribute('aria-controls'));
      if (sous) sous.hidden = true;
    });
  }

  function closeNav() {
    nav.classList.remove('is-open');
    toggle.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    replier();
  }

  /* Accordéon : le libellé reste un lien vers la mère, le chevron déplie. */
  plus.forEach(function (b) {
    b.addEventListener('click', function () {
      var sous = document.getElementById(b.getAttribute('aria-controls'));
      if (!sous) return;
      var ouvert = b.getAttribute('aria-expanded') === 'true';
      replier();
      if (!ouvert) {
        b.setAttribute('aria-expanded', 'true');
        sous.hidden = false;
        b.parentNode.scrollIntoView({ block: 'nearest' });
      }
    });
  });

  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) closeNav();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeNav();
  });
})();

/* Méga-menu — un panneau par axe. Le lien reste un lien : un clic sur le
   libellé navigue, un clic sur le chevron ouvre le panneau de CET axe. */
(function () {
  var boutons = [].slice.call(document.querySelectorAll('[data-mega]'));
  if (!boutons.length) return;

  function panneau(b) { return document.getElementById(b.getAttribute('aria-controls')); }

  function fermer() {
    boutons.forEach(function (b) {
      b.setAttribute('aria-expanded', 'false');
      var p = panneau(b);
      if (p) p.setAttribute('data-ouvert', 'false');
    });
  }

  boutons.forEach(function (b) {
    b.addEventListener('click', function (e) {
      if (!e.target.closest('.chev')) return;   // le libellé navigue normalement
      e.preventDefault();
      e.stopPropagation();
      var p = panneau(b);
      if (!p) return;
      var ouvert = p.getAttribute('data-ouvert') === 'true';
      fermer();
      if (!ouvert) {
        p.setAttribute('data-ouvert', 'true');
        b.setAttribute('aria-expanded', 'true');
      }
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.mega') && !e.target.closest('[data-mega]')) fermer();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') fermer();
  });
})();
