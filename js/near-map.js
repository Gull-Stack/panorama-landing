/* Nearby map — Ranee, 2026-10-06 call: "that should be a map that has the
   dropped pins of where all the potential dining, recreation, shopping,
   schools, parks and trails exist ... an actual map."

   One component, used on Around Herriman and Life at Panorama. Markup is a
   <div data-near-map> plus the legend chips already in the page, so with no
   script the page still lists the categories and links out to Google Maps.

   ⛔ Every pin below is a real place that is ALSO named in the page copy, and
   its coordinates came from OpenStreetMap's geocoder on 2026-10-06. Drive
   times are the ones the page already states. Nothing here is estimated by
   an agent. To add a place, add it to the page copy first, then here.

   Tiles: OpenStreetMap (no key; attribution required and rendered). Leaflet
   1.9.4 from unpkg. If either fails to load, the fallback text shows and
   the legend chips still open Google Maps. */
(function () {
  "use strict";

  var PANORAMA = { lat: 40.4798, lng: -111.9861, name: "Panorama", note: "Herriman's foothills community" };

  var CATS = {
    dining:     { label: "Dining",          color: "#c9a96e" },
    shopping:   { label: "Shopping",        color: "#b5653a" },
    recreation: { label: "Recreation",      color: "#3f8c8a" },
    schools:    { label: "Schools",         color: "#3b5b9d" },
    parks:      { label: "Parks & Trails",  color: "#5b8a3c" }
  };

  var PLACES = [
    { cat: "dining",     name: "Mountain View Village",          city: "Riverton",     time: "About 5 minutes",  lat: 40.5091, lng: -111.9984 },
    { cat: "dining",     name: "The District",                   city: "South Jordan", time: "About 10 minutes", lat: 40.5417, lng: -111.9804 },
    { cat: "shopping",   name: "Mountain View Village",          city: "Riverton",     time: "About 5 minutes",  lat: 40.5091, lng: -111.9984 },
    { cat: "shopping",   name: "Smith's, 13400 South",           city: "Herriman",     time: "About 5 minutes",  lat: 40.5094, lng: -112.0236 },
    { cat: "shopping",   name: "Walmart Neighborhood Market",    city: "Herriman",     time: "About 5 minutes",  lat: 40.5091, lng: -112.0115 },
    { cat: "shopping",   name: "The District",                   city: "South Jordan", time: "About 10 minutes", lat: 40.5417, lng: -111.9804 },
    { cat: "shopping",   name: "Costco",                         city: "South Jordan", time: "About 10 minutes", lat: 40.5593, lng: -111.9760 },
    { cat: "shopping",   name: "Lowe's",                         city: "Riverton",     time: "About 10 minutes", lat: 40.5249, lng: -111.9831 },
    { cat: "shopping",   name: "Jordan Landing",                 city: "West Jordan",  time: "About 15 minutes", lat: 40.6159, lng: -111.9798 },
    { cat: "shopping",   name: "IKEA",                           city: "Draper",       time: "About 15 minutes", lat: 40.5087, lng: -111.8931 },
    { cat: "shopping",   name: "Outlets at Traverse Mountain",   city: "Lehi",         time: "About 20 minutes", lat: 40.4352, lng: -111.8844 },
    { cat: "recreation", name: "J.L. Sorenson Recreation Center", city: "Herriman",    time: "About 5 minutes",  lat: 40.5174, lng: -112.0172 },
    { cat: "recreation", name: "Thanksgiving Point Golf Club",   city: "Lehi",         time: "About 15 minutes", lat: 40.4274, lng: -111.9049 },
    { cat: "recreation", name: "Glenmoor Golf Course",           city: "South Jordan", time: "About 15 minutes", lat: 40.5718, lng: -112.0020 },
    { cat: "recreation", name: "Snowbird",                       city: "Little Cottonwood Canyon", time: "About 45 minutes", lat: 40.5830, lng: -111.6560 },
    { cat: "recreation", name: "Brighton Resort",                city: "Big Cottonwood Canyon",    time: "About an hour",    lat: 40.5983, lng: -111.5837 },
    { cat: "schools",    name: "Butterfield Canyon Elementary",  city: "Herriman",     time: "About 4 miles",    lat: 40.5010, lng: -112.0543 },
    { cat: "schools",    name: "Fort Herriman Middle",           city: "Herriman",     time: "About 3 miles",    lat: 40.4947, lng: -112.0349 },
    { cat: "schools",    name: "Herriman High School",           city: "Herriman",     time: "About 5 miles",    lat: 40.5350, lng: -112.0307 },
    { cat: "parks",      name: "Oquirrh Lake",                   city: "Daybreak",     time: "About 10 minutes", lat: 40.5544, lng: -112.0010 },
    { cat: "parks",      name: "J.L. Sorenson Recreation Center", city: "Herriman",    time: "About 5 minutes",  lat: 40.5174, lng: -112.0172 }
  ];
  // Butterfield Canyon and Rose Canyon are pushed in by the page if the
  // geocoder had them (see data-extra-pins), so the list above never carries
  // a coordinate nobody looked up.

  function gmaps(p) {
    return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(p.name + ", " + p.city + ", UT");
  }

  function mount(root) {
    var legend = document.querySelector("[data-near-legend]");
    var extra = [];
    try { extra = JSON.parse(root.getAttribute("data-extra-pins") || "[]"); } catch (e) { extra = []; }
    var places = PLACES.concat(extra);

    if (typeof L === "undefined") {
      root.innerHTML = '<div class="near-fallback"><p>The map could not load. Every place is listed below, and each category opens in Google Maps.</p></div>';
      return;
    }

    var map = L.map(root, { scrollWheelZoom: false, zoomControl: true, attributionControl: true });
    // ⛔ CARTO's free basemap started stamping "API KEY REQUIRED" across every
    // tile (seen in the 2026-10-06 render). OpenStreetMap's own tiles need no
    // key; attribution is required and rendered. Swap to Google Maps here
    // once a Maps Platform key exists on the GullStack GCP project.
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var home = L.marker([PANORAMA.lat, PANORAMA.lng], {
      icon: L.divIcon({ className: "", html: '<div class="near-pin home"></div>', iconSize: [34, 34], iconAnchor: [17, 34], popupAnchor: [0, -30] }),
      title: PANORAMA.name, alt: PANORAMA.name, zIndexOffset: 1000
    }).addTo(map).bindPopup('<div class="near-popup-body"><strong class="near-popup-title">' + PANORAMA.name + "</strong><p>" + PANORAMA.note + "</p></div>", { className: "near-popup" });

    var groups = {};
    Object.keys(CATS).forEach(function (k) { groups[k] = L.layerGroup(); });

    places.forEach(function (p) {
      var c = CATS[p.cat];
      if (!c) return;
      var m = L.marker([p.lat, p.lng], {
        icon: L.divIcon({ className: "", html: '<div class="near-pin" style="background:' + c.color + '"></div>', iconSize: [26, 26], iconAnchor: [13, 26], popupAnchor: [0, -24] }),
        title: p.name + " (" + c.label + ")", alt: p.name
      });
      m.bindPopup(
        '<div class="near-popup-body"><strong class="near-popup-title">' + p.name + "</strong><p>" + p.city + (p.time ? " &middot; " + p.time : "") + "</p>" +
        '<a href="' + gmaps(p) + '" target="_blank" rel="noopener">Open in Google Maps &rarr;</a></div>',
        { className: "near-popup" }
      );
      groups[p.cat].addLayer(m);
    });

    var active = {};
    Object.keys(groups).forEach(function (k) { active[k] = true; groups[k].addTo(map); });

    function fit() {
      var pts = [[PANORAMA.lat, PANORAMA.lng]];
      places.forEach(function (p) { if (active[p.cat]) pts.push([p.lat, p.lng]); });
      map.fitBounds(pts, { padding: [28, 28], maxZoom: 13 });
    }
    fit();

    if (legend) {
      legend.querySelectorAll("[data-cat]").forEach(function (btn) {
        var k = btn.getAttribute("data-cat");
        var count = places.filter(function (p) { return p.cat === k; }).length;
        var n = btn.querySelector(".near-count");
        if (n) n.textContent = count;
        btn.setAttribute("aria-pressed", "true");
        btn.addEventListener("click", function () {
          active[k] = !active[k];
          btn.setAttribute("aria-pressed", active[k] ? "true" : "false");
          if (active[k]) groups[k].addTo(map); else map.removeLayer(groups[k]);
          fit();
        });
      });
    }

    // Leaflet measures its box at init; if the section was hidden by a
    // scroll-reveal at that moment the tiles stay blank until a resize.
    setTimeout(function () { map.invalidateSize(); fit(); }, 400);
    window.addEventListener("resize", function () { map.invalidateSize(); });
  }

  function init() {
    document.querySelectorAll("[data-near-map]").forEach(mount);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
