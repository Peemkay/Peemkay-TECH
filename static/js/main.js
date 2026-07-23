(function () {
  "use strict";

  // Sticky navbar background on scroll
  var navbar = document.getElementById("navbar");
  var backToTop = document.getElementById("backToTop");

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (navbar) navbar.classList.toggle("is-scrolled", y > 8);
    if (backToTop) backToTop.classList.toggle("is-visible", y > 500);
  }
  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Mobile menu toggle
  var navToggle = document.getElementById("navToggle");
  var mobileMenu = document.getElementById("mobileMenu");

  function closeMenu() {
    if (!mobileMenu) return;
    mobileMenu.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  if (navToggle && mobileMenu) {
    navToggle.addEventListener("click", function () {
      var isOpen = mobileMenu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      document.body.style.overflow = isOpen ? "hidden" : "";
    });

    mobileMenu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  // Reveal-on-scroll animations
  var revealEls = document.querySelectorAll("[data-reveal]");
  if (revealEls.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  // Project filter (Projects page)
  var filterBar = document.querySelector("[data-filter-bar]");
  if (filterBar) {
    var buttons = filterBar.querySelectorAll(".filter-btn");
    var cards = document.querySelectorAll("[data-project-category]");

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) { b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        var category = btn.getAttribute("data-filter");

        cards.forEach(function (card) {
          var match = category === "all" || card.getAttribute("data-project-category") === category;
          card.style.display = match ? "" : "none";
        });
      });
    });
  }

  // 3D tilt-on-hover for cards and the hero panel. Skipped for touch
  // devices (no real pointer to track) and for prefers-reduced-motion.
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasFinePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  if (!reduceMotion && hasFinePointer) {
    var makeTilt = function (el, opts) {
      opts = opts || {};
      var max = opts.max || 6;
      var baseRX = opts.baseRX || 0;
      var baseRY = opts.baseRY || 0;
      var lift = opts.lift !== undefined ? opts.lift : -6;
      var scale = opts.scale || 1.02;
      var rect = null;

      el.addEventListener("mouseenter", function () {
        rect = el.getBoundingClientRect();
        el.style.transition = "transform 0.12s linear";
      });

      el.addEventListener("mousemove", function (e) {
        if (!rect) rect = el.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width;
        var py = (e.clientY - rect.top) / rect.height;
        var rx = baseRX + (0.5 - py) * max * 2;
        var ry = baseRY + (px - 0.5) * max * 2;
        el.style.transform =
          "perspective(1400px) rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg) " +
          "translateY(" + lift + "px) scale(" + scale + ")";
      });

      el.addEventListener("mouseleave", function () {
        el.style.transition = "transform 0.6s cubic-bezier(0.22, 1, 0.36, 1)";
        el.style.transform = "";
        rect = null;
      });
    };

    document.querySelectorAll(".card").forEach(function (el) {
      makeTilt(el, { max: 5, lift: -6, scale: 1.015 });
    });

    var heroPanel = document.querySelector(".hero__panel");
    if (heroPanel) {
      makeTilt(heroPanel, { max: 4, baseRX: 4, baseRY: -8, lift: 0, scale: 1.01 });
    }
  }

  // Contact form: client-side enhancement (native validation still applies)
  var contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", function () {
      var submitBtn = contactForm.querySelector("[type='submit']");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = "Sending…";
      }
    });
  }
})();
