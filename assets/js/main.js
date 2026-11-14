(function () {
  var root = document.documentElement;

  // ---- Theme toggle (light / dark, remembered per browser) ----
  function currentTheme() {
    var t = root.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // ---- Total visits (GoatCounter public counter; stays hidden if unavailable) ----
  var visits = document.querySelector("[data-goatcounter-total]");
  if (visits && window.fetch) {
    fetch(visits.getAttribute("data-goatcounter-total"))
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (data) {
        var n = parseInt(String(data.count).replace(/\D/g, ""), 10);
        if (!n) return;
        visits.textContent = " · " + n.toLocaleString(root.lang || "en") + " " + visits.getAttribute("data-label");
        visits.hidden = false;
      })
      .catch(function () {});
  }

  // ---- Copy buttons on code blocks ----
  var fr = (root.lang || "").indexOf("fr") === 0;
  var COPY = fr ? "copier" : "copy";
  var COPIED = fr ? "copié" : "copied";
  document.querySelectorAll(".prose div.highlighter-rouge").forEach(function (block) {
    var code = block.querySelector("pre code") || block.querySelector("pre");
    if (!code || !navigator.clipboard) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = COPY;
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(code.innerText).then(function () {
        btn.textContent = COPIED;
        setTimeout(function () { btn.textContent = COPY; }, 1500);
      });
    });
    block.appendChild(btn);
  });

  // ---- Tag filter on /blog/ ----
  var chips = document.querySelectorAll(".tag-filter .chip");
  if (chips.length) {
    var items = document.querySelectorAll(".post-item");
    var groups = document.querySelectorAll(".year-group");
    var noMatch = document.getElementById("no-match");

    function apply(tag) {
      var shown = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.tag === tag)); });
      items.forEach(function (li) {
        var tags = (li.dataset.tags || "").trim().split(/\s+/);
        var ok = !tag || tags.indexOf(tag) !== -1;
        li.hidden = !ok;
        if (ok) shown++;
      });
      groups.forEach(function (g) { g.hidden = !g.querySelector(".post-item:not([hidden])"); });
      if (noMatch) noMatch.hidden = shown > 0;
    }

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var tag = c.dataset.tag;
        apply(tag);
        var url = new URL(window.location);
        if (tag) url.searchParams.set("tag", tag); else url.searchParams.delete("tag");
        history.replaceState(null, "", url);
      });
    });

    var initial = new URLSearchParams(window.location.search).get("tag");
    if (initial) apply(initial.toLowerCase());
  }
})();
