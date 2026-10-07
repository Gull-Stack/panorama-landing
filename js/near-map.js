/* Nearby map — Ranee, 2026-10-06 call: "that should be a map that has the
   dropped pins of where all the potential dining, recreation, shopping,
   schools, parks and trails exist ... in an actual Google map."

   Google Maps JavaScript API. One component, used on Around Herriman and
   Life at Panorama. Markup is a <div data-near-map> plus the legend chips
   already in the page, so with no script the page still lists the
   categories, and every chip's places link out to Google Maps.

   ⛔ Every pin below is a real place that is ALSO named in the page copy,
   and its coordinates came from OpenStreetMap's geocoder on 2026-10-06.
   Drive times are the ones the page already states. Nothing here is
   estimated by an agent. To add a place, add it to the page copy first,
   then here.

   The browser key in the page is referrer-restricted to this site's hosts
   and to the Maps JavaScript API only (GCP project gullstack-489321, key
   "panorama-landing map"). That is the normal shape of a public map key. */
(function () {
  "use strict";

  var PANORAMA = { lat: 40.4798, lng: -111.9861, name: "Panorama", note: "Herriman's foothills community" };

  var CATS = {
    dining:     { label: "Dining",         color: "#c9a96e" },
    shopping:   { label: "Shopping",       color: "#b5653a" },
    recreation: { label: "Recreation",     color: "#3f8c8a" },
    schools:    { label: "Schools",        color: "#3b5b9d" },
    parks:      { label: "Parks & Trails", color: "#5b8a3c" }
  };

  var PLACES = [
    { cat: "dining",     name: "Mountain View Village",           city: "Riverton",     time: "About 5 minutes",  lat: 40.5091, lng: -111.9984 },
    { cat: "dining",     name: "The District",                    city: "South Jordan", time: "About 10 minutes", lat: 40.5417, lng: -111.9804 },
    { cat: "shopping",   name: "Mountain View Village",           city: "Riverton",     time: "About 5 minutes",  lat: 40.5091, lng: -111.9984 },
    { cat: "shopping",   name: "Smith's, 13400 South",            city: "Herriman",     time: "About 5 minutes",  lat: 40.5094, lng: -112.0236 },
    { cat: "shopping",   name: "Walmart Neighborhood Market",     city: "Herriman",     time: "About 5 minutes",  lat: 40.5091, lng: -112.0115 },
    { cat: "shopping",   name: "The District",                    city: "South Jordan", time: "About 10 minutes", lat: 40.5417, lng: -111.9804 },
    { cat: "shopping",   name: "Costco",                          city: "South Jordan", time: "About 10 minutes", lat: 40.5593, lng: -111.9760 },
    { cat: "shopping",   name: "Lowe's",                          city: "Riverton",     time: "About 10 minutes", lat: 40.5249, lng: -111.9831 },
    { cat: "shopping",   name: "Jordan Landing",                  city: "West Jordan",  time: "About 15 minutes", lat: 40.6159, lng: -111.9798 },
    { cat: "shopping",   name: "IKEA",                            city: "Draper",       time: "About 15 minutes", lat: 40.5087, lng: -111.8931 },
    { cat: "shopping",   name: "Outlets at Traverse Mountain",    city: "Lehi",         time: "About 20 minutes", lat: 40.4352, lng: -111.8844 },
    { cat: "recreation", name: "J.L. Sorenson Recreation Center", city: "Herriman",     time: "About 5 minutes",  lat: 40.5174, lng: -112.0172 },
    { cat: "recreation", name: "Thanksgiving Point Golf Club",    city: "Lehi",         time: "About 15 minutes", lat: 40.4274, lng: -111.9049 },
    { cat: "recreation", name: "Glenmoor Golf Course",            city: "South Jordan", time: "About 15 minutes", lat: 40.5718, lng: -112.0020 },
    { cat: "recreation", name: "Snowbird",                        city: "Little Cottonwood Canyon", time: "About 45 minutes", lat: 40.5830, lng: -111.6560 },
    { cat: "recreation", name: "Brighton Resort",                 city: "Big Cottonwood Canyon",    time: "About an hour",    lat: 40.5983, lng: -111.5837 },
    { cat: "schools",    name: "Butterfield Canyon Elementary",   city: "Herriman",     time: "About 4 miles",    lat: 40.5010, lng: -112.0543 },
    { cat: "schools",    name: "Fort Herriman Middle",            city: "Herriman",     time: "About 3 miles",    lat: 40.4947, lng: -112.0349 },
    { cat: "schools",    name: "Herriman High School",            city: "Herriman",     time: "About 5 miles",    lat: 40.5350, lng: -112.0307 },
    { cat: "parks",      name: "Oquirrh Lake",                    city: "Daybreak",     time: "About 10 minutes", lat: 40.5544, lng: -112.0010 },
    { cat: "parks",      name: "J.L. Sorenson Recreation Center", city: "Herriman",     time: "About 5 minutes",  lat: 40.5174, lng: -112.0172 }
  ];
  // Rose Canyon arrives from the page's data-extra-pins (geocoded 10/6), so
  // the list above never carries a coordinate nobody looked up.

  function gmapsLink(p) {
    return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(p.name + ", " + p.city + ", UT");
  }

  // A teardrop pin filled with the category color, the same color as the
  // legend dot, so the legend reads as the key to the map.
  function pinIcon(color, big) {
    var s = big ? 44 : 34, h = s * 32 / 24;
    var svg =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 32" width="' + s + '" height="' + h + '">' +
      '<path d="M12 1C6 1 1.5 5.6 1.5 11.4c0 7.6 9 18 10.5 19.6 1.5-1.6 10.5-12 10.5-19.6C22.5 5.6 18 1 12 1z" fill="' + color + '" stroke="' + (big ? "#c9a96e" : "#ffffff") + '" stroke-width="' + (big ? 2.2 : 1.6) + '"/>' +
      (big ? '<circle cx="12" cy="11.4" r="3.4" fill="#c9a96e"/>' : '<circle cx="12" cy="11.4" r="3" fill="#ffffff" fill-opacity="0.9"/>') +
      "</svg>";
    return {
      url: "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg),
      scaledSize: new google.maps.Size(s, h),
      anchor: new google.maps.Point(s / 2, h)
    };
  }

  function popupHtml(p, isHome) {
    return (
      '<div class="near-popup-body"><strong class="near-popup-title">' + p.name + "</strong>" +
      "<p>" + (isHome ? p.note : p.city + (p.time ? " &middot; " + p.time : "")) + "</p>" +
      (isHome ? "" : '<a href="' + gmapsLink(p) + '" target="_blank" rel="noopener">Open in Google Maps &rarr;</a>') +
      "</div>"
    );
  }

  function mount(root) {
    if (root.getAttribute("data-mounted")) return;
    root.setAttribute("data-mounted", "1");
    var legend = document.querySelector("[data-near-legend]");
    var extra = [];
    try { extra = JSON.parse(root.getAttribute("data-extra-pins") || "[]"); } catch (e) { extra = []; }
    var places = PLACES.concat(extra);

    if (typeof google === "undefined" || !google.maps) {
      root.innerHTML = '<div class="near-fallback"><p>The map could not load. Every place is listed below, and each category opens in Google Maps.</p></div>';
      return;
    }

    var map = new google.maps.Map(root, {
      center: PANORAMA,
      zoom: 11,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: true,
      gestureHandling: "cooperative",
      clickableIcons: false,
      backgroundColor: "#e9e5dc"
    });
    var info = new google.maps.InfoWindow();

    var home = new google.maps.Marker({ position: PANORAMA, map: map, title: PANORAMA.name, icon: pinIcon("#0a1628", true), zIndex: 1000 });
    home.addListener("click", function () { info.setContent(popupHtml(PANORAMA, true)); info.open({ anchor: home, map: map }); });

    var markers = {};
    Object.keys(CATS).forEach(function (k) { markers[k] = []; });
    places.forEach(function (p) {
      var c = CATS[p.cat];
      if (!c) return;
      var m = new google.maps.Marker({ position: { lat: p.lat, lng: p.lng }, map: map, title: p.name + " (" + c.label + ")", icon: pinIcon(c.color, false) });
      m.addListener("click", function () { info.setContent(popupHtml(p, false)); info.open({ anchor: m, map: map }); });
      markers[p.cat].push(m);
    });

    var active = {};
    Object.keys(markers).forEach(function (k) { active[k] = true; });

    function fit() {
      var b = new google.maps.LatLngBounds();
      b.extend(PANORAMA);
      places.forEach(function (p) { if (active[p.cat]) b.extend({ lat: p.lat, lng: p.lng }); });
      map.fitBounds(b, 28);
      google.maps.event.addListenerOnce(map, "idle", function () { if (map.getZoom() > 13) map.setZoom(13); });
    }
    fit();

    if (legend) {
      legend.querySelectorAll("[data-cat]").forEach(function (btn) {
        var k = btn.getAttribute("data-cat");
        var n = btn.querySelector(".near-count");
        if (n) n.textContent = (markers[k] || []).length;
        btn.setAttribute("aria-pressed", "true");
        btn.addEventListener("click", function () {
          active[k] = !active[k];
          btn.setAttribute("aria-pressed", active[k] ? "true" : "false");
          (markers[k] || []).forEach(function (m) { m.setMap(active[k] ? map : null); });
          info.close();
          fit();
        });
      });
    }
  }

  // The Maps script is loaded with loading=async&callback=initNearMap.
  window.initNearMap = function () { document.querySelectorAll("[data-near-map]").forEach(mount); };
  // If the Maps script never arrives (blocked, offline), show the fallback
  // after a beat so the box is not blank.
  window.addEventListener("load", function () {
    setTimeout(function () {
      if (typeof google === "undefined" || !google.maps) document.querySelectorAll("[data-near-map]").forEach(mount);
    }, 4000);
  });
})();
