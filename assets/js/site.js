// philipagain.com: small enhancements, no tracking, no third parties.

// Logo: every click turns it a third, so it lands on the same shape with the colours
// one place further round. Every 9 to 14 seconds the leaves drift apart and gather in
// again; a click restarts that wait, and nothing runs while the tab is hidden.
(function () {
  var btn = document.querySelector(".logo-btn");
  if (!btn) return;
  var svg = btn.querySelector(".logo");
  var spin = svg.querySelector(".spin");
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var turns = 0, timer;

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
    schedule();
  });
  schedule();
})();

// "again...": clicking starts (and stops) a band of "again..." running out of "Philip".
(function () {
  var btn = document.querySelector(".again-btn");
  if (!btn) return;
  btn.addEventListener("click", function () {
    btn.setAttribute("aria-pressed", btn.getAttribute("aria-pressed") === "true" ? "false" : "true");
  });
})();

// "So far": the path moves on its own unless the visitor prefers reduced motion.
// A copy of the steps (hidden from screen readers) makes the loop seamless.
// Hover or keyboard focus stops it; the Pause button stops it for good and
// lets visitors scroll by hand.
(function () {
  var section = document.querySelector(".path");
  if (!section || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var track = section.querySelector(".path-track");
  var group = section.querySelector(".path-group");
  var button = section.querySelector(".path-pause");
  var copy = group.cloneNode(true);
  copy.setAttribute("aria-hidden", "true");
  copy.setAttribute("inert", "");
  track.appendChild(copy);

  function run(on) {
    section.classList.toggle("is-running", on);
    copy.hidden = !on;
    button.textContent = on ? "Pause" : "Play";
    button.setAttribute("aria-pressed", on ? "false" : "true");
  }
  button.hidden = false;
  button.addEventListener("click", function () { run(!section.classList.contains("is-running")); });
  run(true);
})();
