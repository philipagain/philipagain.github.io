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
