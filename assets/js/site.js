// philipagain.com: small enhancements, no tracking, no third parties.

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
