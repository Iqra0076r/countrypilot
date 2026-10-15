/* CountryPilot minimal theme JS — vanilla. Scope: footer year, /search/ filter,
   contact-page article prefill. Nothing else. Budget: <=10KB. */
(function(){
  "use strict";
  /* Footer year — honest current-year fact */
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());

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
})();
