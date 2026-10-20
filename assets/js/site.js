// philipagain.com: small enhancements, no tracking, no third parties.
//
// Signup forms: until a newsletter service is connected, they only check the
// address and say the newsletter is coming soon. Nothing is stored or sent.
// To connect a service later, replace the "coming soon" branch below with the
// provider's form endpoint (and add a privacy notice).

(function () {
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  document.querySelectorAll("[data-signup]").forEach(function (form) {
    var input = form.querySelector("input[type=email]");
    var msg = form.querySelector(".msg");

    input.addEventListener("input", function () {
      msg.textContent = "";
      input.removeAttribute("aria-invalid");
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var value = input.value.trim();
      if (!EMAIL.test(value)) {
        input.setAttribute("aria-invalid", "true");
        msg.textContent = "Please enter a full email address, like you@example.com.";
        input.focus();
        return;
      }
      msg.textContent = "Thanks! The newsletter isn't open yet. It's coming soon, so check back here.";
      input.value = "";
    });
  });
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
