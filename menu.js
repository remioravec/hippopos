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

/* Méga-menu — ouvert par les entrées d'axe, fermé au clic extérieur et à Échap.
   Le lien reste un lien : un clic sur le libellé navigue, un clic sur le chevron
   ouvre le panneau. */
(function () {
  var pan = document.getElementById('mega');
  var boutons = [].slice.call(document.querySelectorAll('[data-mega]'));
  if (!pan || !boutons.length) return;

  function fermer() {
    pan.setAttribute('data-ouvert', 'false');
    boutons.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
  }
  boutons.forEach(function (b) {
    b.addEventListener('click', function (e) {
      if (!e.target.closest('.chev')) return;   // le libellé navigue normalement
      e.preventDefault();
      e.stopPropagation();
      var ouvert = pan.getAttribute('data-ouvert') === 'true';
      fermer();
      if (!ouvert) {
        pan.setAttribute('data-ouvert', 'true');
        b.setAttribute('aria-expanded', 'true');
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!pan.contains(e.target)) fermer();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') fermer();
  });
})();
