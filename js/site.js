/* Panorama — the one page script. Menu, header, reveal, lightbox.
   Nothing on a page depends on it to be readable: see .js .reveal in site.css. */
(function () {
  "use strict";
  var doc = document.documentElement;
  /* ⛔ Ranee, 9/21: "The white looks like an error ... it loads late." Anything
     already on screen is marked revealed BEFORE .js turns hiding on, so the
     first paint never blanks. Only what is below the fold fades in. */
  document.querySelectorAll(".reveal").forEach(function (el) {
    if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add("in");
  });
  doc.classList.add("js");

  /* Header goes solid once the hero is behind it. Pages with no hero are
     solid from the start (class set in the markup). */
  var header = document.querySelector(".header");
  if (header && !header.classList.contains("solid")) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 40); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Phone menu. A top item with a mega menu opens it on first tap and follows
     the link on the second, so every section stays one tap away. */
  var btn = document.querySelector(".menu-btn");
  if (btn) {
    btn.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    });
    document.querySelectorAll(".menu > li.has-mega > .menu-link").forEach(function (a) {
      a.addEventListener("click", function (e) {
        if (window.innerWidth > 960) return;
        var li = a.parentElement;
        if (!li.classList.contains("open")) { e.preventDefault(); li.classList.add("open"); }
      });
    });
    // Choosing a section closes the menu, including a jump on this same page.
    document.querySelectorAll(".menu a").forEach(function (a) {
      a.addEventListener("click", function () {
        if (window.innerWidth > 960 || a.parentElement.classList.contains("has-mega")) return;
        document.body.classList.remove("menu-open");
        document.body.style.overflow = "";
      });
    });
  }

  /* Landing on /things-to-do#dining: the map and photos above the target
     load after the browser has already scrolled, and push it down. Scroll
     again once the page has settled. Ranee, 10/29: "None of the drop downs
     are working." */
  if (location.hash.length > 1) {
    var settle = function () {
      var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (t) t.scrollIntoView();
    };
    window.addEventListener("load", function () { settle(); setTimeout(settle, 600); });
  }

  /* Reveal on scroll. */
  var items = document.querySelectorAll(".reveal:not(.in)");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  /* Lightbox: any [data-full] opens its large copy. Small copies load on the
     page; the large one loads only when someone asks for it. */
  var zoomables = Array.prototype.slice.call(document.querySelectorAll("[data-full]"));
  if (zoomables.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Photo viewer");
    lb.innerHTML = '<img alt=""><button class="lb-close" aria-label="Close">&times;</button>' +
      '<button class="lb-prev" aria-label="Previous">&lsaquo;</button><button class="lb-next" aria-label="Next">&rsaquo;</button><div class="lb-count"></div>';
    document.body.appendChild(lb);
    var img = lb.querySelector("img"), count = lb.querySelector(".lb-count"), at = 0, opener = null;
    var show = function (i) {
      at = (i + zoomables.length) % zoomables.length;
      var el = zoomables[at];
      img.src = el.getAttribute("data-full");
      img.alt = el.getAttribute("data-alt") || "";
      count.textContent = zoomables.length > 1 ? (at + 1) + " / " + zoomables.length : "";
    };
    var close = function () { lb.classList.remove("open"); document.body.style.overflow = ""; if (opener) opener.focus(); };
    var single = zoomables.length < 2;
    lb.querySelector(".lb-prev").hidden = single;
    lb.querySelector(".lb-next").hidden = single;
    zoomables.forEach(function (el, i) {
      el.addEventListener("click", function () { opener = el; show(i); lb.classList.add("open"); document.body.style.overflow = "hidden"; lb.querySelector(".lb-close").focus(); });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(at - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(at + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft" && !single) show(at - 1);
      if (e.key === "ArrowRight" && !single) show(at + 1);
    });
  }
})();
