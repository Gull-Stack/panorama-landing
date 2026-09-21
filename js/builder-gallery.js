/* The dots under a builder's photos.
 *
 * ⛔ DEFERRED AND OPTIONAL ON PURPOSE. The strip is a scroll-snap container of
 * real <img> tags, so with no JavaScript it is still a working, swipeable set
 * of photos -- this file only adds click-to-jump and keeps the active dot in
 * sync. Ranee's complaint on 2026-09-21 was a page that renders blank until
 * script runs; nothing on a builder page is allowed to depend on this file.
 */
(function () {
  'use strict';
  document.querySelectorAll('.builder-gallery[data-count]').forEach(function (g) {
    var track = g.querySelector('.builder-track');
    var dots = Array.prototype.slice.call(g.querySelectorAll('.builder-dot'));
    var slides = Array.prototype.slice.call(g.querySelectorAll('.builder-slide'));
    if (!track || !dots.length || !slides.length) return;

    function mark(i) {
      dots.forEach(function (d, n) {
        if (n === i) { d.setAttribute('aria-current', 'true'); }
        else { d.removeAttribute('aria-current'); }
      });
    }
    mark(0);

    dots.forEach(function (d, i) {
      d.addEventListener('click', function () {
        track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: 'smooth' });
        mark(i);
      });
    });

    // Keep the dots honest when someone swipes instead of clicking.
    var tick;
    track.addEventListener('scroll', function () {
      clearTimeout(tick);
      tick = setTimeout(function () {
        var x = track.scrollLeft + track.offsetLeft;
        var best = 0, bestD = Infinity;
        slides.forEach(function (s, i) {
          var d = Math.abs(s.offsetLeft - x);
          if (d < bestD) { bestD = d; best = i; }
        });
        mark(best);
      }, 80);
    }, { passive: true });
  });
})();
