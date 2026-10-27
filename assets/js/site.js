// philipagain.com: small enhancements, no tracking, no third parties.
// Everything here is extra: without this script the page is complete and readable.

var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Logo: every click turns it a third, so it lands on the same shape with the colours
// one place further round. Three turns make a full circle, and it says so. Every 9 to
// 14 seconds the leaves drift apart and gather in again; a click restarts that wait,
// and nothing runs while the tab is hidden.
(function () {
  var btn = document.querySelector(".logo-btn");
  if (!btn) return;
  var svg = btn.querySelector(".logo");
  var spin = svg.querySelector(".spin");
  var note = document.querySelector(".full-circle");
  var turns = 0, timer, noteTimer;

  function schedule() {
    clearTimeout(timer);
    if (calm) return;
    timer = setTimeout(function () {
      if (!document.hidden) {
        svg.classList.remove("regather");
        void svg.getBoundingClientRect();
        svg.classList.add("regather");
      }
      schedule();
    }, 9000 + Math.random() * 5000);
  }

  btn.addEventListener("click", function () {
    turns += 1;
    spin.style.transform = "rotate(" + turns * 120 + "deg)";
    if (note && turns % 3 === 0) {
      note.textContent = "Full circle. Again?";
      note.classList.add("is-on");
      clearTimeout(noteTimer);
      noteTimer = setTimeout(function () { note.classList.remove("is-on"); }, 2600);
    }
    schedule();
  });
  schedule();
})();

// "again...": clicking runs a band of "again..." out of "Philip", or stops it.
(function () {
  var btn = document.querySelector(".again-btn");
  if (!btn) return;
  btn.addEventListener("click", function () {
    btn.setAttribute("aria-pressed", btn.getAttribute("aria-pressed") === "true" ? "false" : "true");
  });
})();

// Top bar: transparent over the photo, plaster once the page scrolls past it.
(function () {
  var bar = document.querySelector("[data-bar]");
  var hero = document.querySelector(".hero");
  if (!bar || !hero) return;
  function update() { bar.classList.toggle("is-scrolled", window.scrollY > hero.offsetHeight - 90); }
  window.addEventListener("scroll", update, { passive: true });
  update();
})();

// So far: on wide screens the section holds still while scrolling moves the steps up
// through the window on the right; once the last one has passed, the page carries on.
// Opening a step makes the list longer, so the section grows with it.
(function () {
  var section = document.querySelector("[data-pin]");
  if (!section) return;
  var win = section.querySelector(".rows-window");
  var rows = section.querySelector(".rows");
  var wide = window.matchMedia("(min-width: 861px)");
  var travel = 0;
  var pace = 2; // pixels of page scroll per pixel the list moves

  function move() {
    if (!section.classList.contains("is-pinned")) return;
    var progress = (window.scrollY - section.offsetTop) / (travel * pace || 1);
    progress = Math.min(Math.max(progress, 0), 1);
    rows.style.transform = "translateY(" + (-progress * travel).toFixed(1) + "px)";
  }
  function measure() {
    if (!wide.matches) {
      section.classList.remove("is-pinned");
      section.style.height = "";
      rows.style.transform = "";
      return;
    }
    section.classList.add("is-pinned");
    travel = Math.max(0, rows.scrollHeight - win.clientHeight);
    section.style.height = window.innerHeight + travel * pace + "px";
    move();
  }

  window.addEventListener("scroll", move, { passive: true });
  window.addEventListener("resize", measure);
  section.addEventListener("toggle", measure, true);
  if (document.fonts) document.fonts.ready.then(measure);
  measure();
})();

// Entrances: the parts of each section arrive in reading order, once. The started-again
// counter ticks up as each step comes into view.
(function () {
  if (!("IntersectionObserver" in window)) {
    document.documentElement.classList.remove("js");
    return;
  }
  document.querySelectorAll("[data-enter]").forEach(function (el) {
    Array.prototype.forEach.call(el.children, function (child, i) { child.style.setProperty("--i", i); });
  });
  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      seen.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -12% 0px" });
  document.querySelectorAll("[data-enter]").forEach(function (el) { seen.observe(el); });

  var count = document.querySelector("[data-count]");
  if (!count || calm) return;
  var total = parseInt(count.getAttribute("data-count"), 10) || 0;
  var steps = Array.prototype.slice.call(document.querySelectorAll(".row:not(.row-next)"));
  var passed = 0;
  count.textContent = "0";
  var tick = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      tick.unobserve(entry.target);
      passed = Math.min(passed + 1, total);
      count.textContent = String(passed);
    });
  }, { rootMargin: "0px 0px -25% 0px" });
  steps.forEach(function (row) { tick.observe(row); });
})();

// Rolls of film: the arrows show only when there is more to see in that direction,
// older rolls wait behind a button, and a photo opens large (arrows, keys, Esc).
(function () {
  var rolls = Array.prototype.slice.call(document.querySelectorAll(".roll"));
  if (!rolls.length) return;

  rolls.forEach(function (roll) {
    var strip = roll.querySelector(".roll-strip");
    var back = roll.querySelector(".roll-back");
    var on = roll.querySelector(".roll-on");
    function update() {
      back.hidden = strip.scrollLeft < 8;
      on.hidden = strip.scrollLeft + strip.clientWidth > strip.scrollWidth - 8;
    }
    function go(direction) {
      strip.scrollBy({ left: direction * strip.clientWidth * 0.8, behavior: calm ? "auto" : "smooth" });
    }
    back.addEventListener("click", function () { go(-1); });
    on.addEventListener("click", function () { go(1); });
    strip.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  var older = document.querySelector("[data-older]");
  if (older) {
    older.addEventListener("click", function () {
      var first = null;
      rolls.forEach(function (roll) {
        if (roll.classList.contains("is-older") && !roll.classList.contains("is-shown")) {
          roll.classList.add("is-shown");
          first = first || roll;
          roll.querySelector(".roll-on").hidden = roll.querySelector(".roll-strip").scrollWidth <= roll.querySelector(".roll-strip").clientWidth + 8;
        }
      });
      older.parentNode.hidden = true;
      if (first) first.querySelector(".roll-strip").focus();
    });
  }

  var box = document.querySelector(".lightbox");
  if (!box || typeof box.showModal !== "function") return;
  var big = box.querySelector("img");
  var set = [], index = 0, opener = null;

  function show(i) {
    index = (i + set.length) % set.length;
    var link = set[index];
    big.src = link.getAttribute("href");
    big.alt = link.querySelector("img").alt;
  }
  rolls.forEach(function (roll) {
    var links = Array.prototype.slice.call(roll.querySelectorAll(".photo"));
    links.forEach(function (link, i) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        set = links;
        opener = link;
        show(i);
        box.showModal();
      });
    });
  });
  box.querySelector(".lb-back").addEventListener("click", function () { show(index - 1); });
  box.querySelector(".lb-on").addEventListener("click", function () { show(index + 1); });
  box.querySelector(".lb-close").addEventListener("click", function () { box.close(); });
  box.addEventListener("click", function (event) { if (event.target === box) box.close(); });
  box.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });
  box.addEventListener("close", function () { if (opener) opener.focus(); });
})();

// When you switch to another tab, this one asks you to come back.
(function () {
  var title = document.title;
  document.addEventListener("visibilitychange", function () {
    document.title = document.hidden ? "Come back again..." : title;
  });
})();
