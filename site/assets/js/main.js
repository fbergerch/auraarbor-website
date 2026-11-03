/* Aura Arbor — site script: menu, image fallbacks, beta form → HubSpot */
(function () {
  "use strict";

  /* HubSpot form the beta application is sent to (Forms API v3, no API key needed) */
  var HUBSPOT = {
    portalId: "146961124",
    formGuid: "990b16c2-4f05-4b2a-bd91-cb6632b121a1" // share-link id 2mQsWwk8FSyq9kctmMrEhoQ
  };

  /* Image frames: show a tinted stand-in when an image is missing */
  document.querySelectorAll(".frame img").forEach(function (img) {
    function mark() { img.closest(".frame").classList.add("is-missing"); }
    if (img.complete && img.naturalWidth === 0) mark();
    img.addEventListener("error", mark);
  });

  /* Mobile menu */
  var toggle = document.getElementById("menu-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && links.classList.contains("open")) { links.classList.remove("open"); toggle.setAttribute("aria-expanded", false); toggle.focus(); }
    });
  }

  /* Beta form */
  var form = document.getElementById("beta-form");
  if (!form) return;
  var step1 = document.getElementById("step-1");
  var step2 = document.getElementById("step-2");
  var done = document.getElementById("done");
  var bar2 = document.getElementById("bar-2");
  var none = document.getElementById("d-none");
  var submit = document.getElementById("submit");
  var SUBMIT_LABEL = submit.textContent;

  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; }
  function check(id, msg, test) {
    var el = document.getElementById(id), wrap = el.closest(".field"), err = wrap.querySelector(".err");
    var ok = test(el.value.trim());
    wrap.classList.toggle("invalid", !ok);
    el.setAttribute("aria-invalid", !ok);
    err.textContent = ok ? "" : msg;
    return ok;
  }
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  document.getElementById("next").addEventListener("click", function () {
    var results = [
      check("firstname", "Please enter your first name.", function (x) { return x.length > 0; }),
      check("lastname", "Please enter your last name.", function (x) { return x.length > 0; }),
      check("email", "Please enter a valid email, like name@example.com.", function (x) { return EMAIL.test(x); })
    ];
    if (results.indexOf(false) !== -1) { form.querySelector(".invalid input").focus(); return; }
    step1.hidden = true; step2.hidden = false; bar2.classList.add("on");
    document.getElementById("prev_app").focus();
  });
  document.getElementById("back").addEventListener("click", function () {
    step2.hidden = true; step1.hidden = false; bar2.classList.remove("on");
    document.getElementById("firstname").focus();
  });
  document.getElementById("prev_app").addEventListener("change", function (e) {
    document.getElementById("prev_other_wrap").hidden = e.target.value !== "Other";
  });

  var devices = form.querySelectorAll("input[name=vr_device]");
  devices.forEach(function (c) {
    c.addEventListener("change", function () {
      if (c === none && c.checked) devices.forEach(function (o) { if (o !== none) o.checked = false; });
      else if (c.checked) none.checked = false;
      var onlyNone = none.checked;
      document.getElementById("horizon_wrap").hidden = onlyNone;
      document.getElementById("horizon_mail_wrap").hidden = onlyNone;
    });
  });

  function cookie(name) {
    var m = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
    return m ? decodeURIComponent(m[1]) : undefined;
  }
  function showError(msg) {
    var p = document.getElementById("form-error");
    if (!p) { p = document.createElement("p"); p.id = "form-error"; p.className = "err"; p.setAttribute("role", "alert"); step2.querySelector(".form-actions").after(p); }
    p.textContent = msg;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (step2.hidden) { document.getElementById("next").click(); return; }
    if (val("website")) return; // honeypot: bots fill hidden fields

    var picked = Array.prototype.filter.call(devices, function (c) { return c.checked; }).map(function (c) { return c.value; }).join(";");
    var raw = [
      ["0-1", "firstname", val("firstname")],
      ["0-1", "lastname", val("lastname")],
      ["0-1", "email", val("email")],
      ["0-2", "name", val("company")],
      ["0-1", "previous_applications_used", val("prev_app")],
      ["0-1", "previous_other_application_used", val("prev_other")],
      ["0-1", "i_m_interested_in_becoming_a_beta_tester_", document.getElementById("beta_tester").checked ? "true" : "false"],
      ["0-1", "vr_device", picked],
      ["0-1", "meta_horizon_username", val("horizon_user")],
      ["0-1", "meta_horizon_account_email", val("horizon_mail")],
      ["0-1", "other_vr_devices", val("other_device")]
    ];
    var fields = raw.filter(function (f) { return f[2] !== ""; }).map(function (f) { return { objectTypeId: f[0], name: f[1], value: f[2] }; });
    var context = { pageUri: location.href, pageName: document.title };
    var hutk = cookie("hubspotutk"); if (hutk) context.hutk = hutk;

    submit.disabled = true; submit.textContent = "Sending…";
    fetch("https://api.hsforms.com/submissions/v3/integration/submit/" + HUBSPOT.portalId + "/" + HUBSPOT.formGuid, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fields: fields, context: context })
    }).then(function (res) {
      if (!res.ok) return res.json().catch(function () { return {}; }).then(function (b) { throw new Error((b && b.message) || ("HTTP " + res.status)); });
      document.getElementById("done-mail").textContent = val("email");
      step2.hidden = true; done.hidden = false;
      document.getElementById("form-foot").hidden = true;
      done.querySelector("h3").focus();
    }).catch(function (err) {
      console.error("[AuraArbor] form submit failed:", err);
      submit.disabled = false; submit.textContent = SUBMIT_LABEL;
      showError("We couldn't send your application. Check your connection and try again, or email hello@auraarbor.com.");
    });
  });
})();
