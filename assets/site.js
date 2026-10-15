/* CountryPilot minimal theme JS — vanilla. Scope: footer year, /search/ filter,
   contact-page article prefill. Nothing else. Budget: <=10KB. */
(function(){
  "use strict";
  /* Footer year — honest current-year fact */
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());

  /* Topbar date — honest current date for the editorial masthead */
  var today = document.querySelector("[data-today]");
  if (today) {
    try {
      today.textContent = new Date().toLocaleDateString("en-GB", {
        weekday: "long", day: "numeric", month: "long", year: "numeric"
      });
    } catch (e) {}
  }

  /* Search page: live filter over build-time JSON index. Zero-JS fallback is the
     full directory rendered server-side; this only enhances. */
  var form = document.getElementById("searchForm");
  var input = document.getElementById("q");
  var list = document.getElementById("searchResults");
  var count = document.getElementById("searchCount");
  var indexEl = document.getElementById("searchIndex");
  if (form && input && list && indexEl) {
    var data = [];
    try { data = JSON.parse(indexEl.textContent || "[]"); } catch (e) { data = []; }
    var esc = function(s){
      return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){
        return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
      });
    };
    var render = function(){
      var q = input.value.toLowerCase().trim();
      var rows = data.filter(function(x){
        return !q || ((x.title||"")+" "+(x.lede||"")+" "+(x.topic||"")).toLowerCase().indexOf(q) !== -1;
      });
      if (count) count.textContent = rows.length + (rows.length === 1 ? " result" : " results");
      var html = "";
      for (var i = 0; i < rows.length; i++) {
        var r = rows[i];
        html += '<li><a href="' + esc(r.url) + '">' + esc(r.title) + "</a>";
        if (r.lede) html += "<p>" + esc(r.lede) + "</p>";
        html += "</li>";
      }
      list.innerHTML = html || '<li><p>No guides match. Try a country or visa name.</p></li>';
    };
    /* Prefill from ?q= then filter live */
    try {
      var q0 = new URLSearchParams(window.location.search).get("q");
      if (q0 && !input.value) input.value = q0;
    } catch (e) {}
    input.addEventListener("input", render);
    form.addEventListener("submit", function(e){ e.preventDefault(); render(); });
    render();
  }

  /* Contact page: prefill the message when linked from "Report an error" (?article=...) */
  try {
    var art = new URLSearchParams(window.location.search).get("article");
    var msg = document.getElementById("contactMessage");
    if (art && msg && !msg.value) {
      msg.value = "Error report for: " + art + "\n\nWhat is wrong:\n";
    }
  } catch (e) {}

  /* Share row: progressive enhancement. Link intents work with zero JS;
     Copy-link and native Share buttons are injected only when supported. */
  (function(){
    var rows = document.querySelectorAll(".share-list");
    if (!rows.length) return;
    var canon = document.querySelector('link[rel="canonical"]');
    var url = canon ? canon.href : window.location.href;
    var title = document.title || "";
    function track(method){
      try {
        if (typeof gtag === "function") gtag("event", "share", {method: method, page_path: window.location.pathname});
      } catch (e) {}
    }
    rows.forEach(function(ul){
      ul.addEventListener("click", function(ev){
        var a = ev.target.closest("a[data-share]");
        if (a) track(a.getAttribute("data-share"));
      });
      if (navigator.clipboard && window.isSecureContext !== false) {
        var li = document.createElement("li");
        var b = document.createElement("button");
        b.type = "button"; b.textContent = "Copy link"; b.setAttribute("data-share", "copy");
        b.setAttribute("aria-live", "polite");
        b.addEventListener("click", function(){
          navigator.clipboard.writeText(url).then(function(){
            b.textContent = "Copied \u2713";
            setTimeout(function(){ b.textContent = "Copy link"; }, 2000);
          }).catch(function(){});
          track("copy");
        });
        li.appendChild(b); ul.appendChild(li);
      }
      if (navigator.share) {
        var li2 = document.createElement("li");
        var b2 = document.createElement("button");
        b2.type = "button"; b2.textContent = "Share\u2026"; b2.setAttribute("data-share", "native");
        b2.addEventListener("click", function(){
          try { navigator.share({title: title, url: url}).catch(function(){}); } catch (e) {}
          track("native");
        });
        li2.appendChild(b2); ul.appendChild(li2);
      }
    });
  })();
})();
