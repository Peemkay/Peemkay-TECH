(function () {
  "use strict";

  // Mobile sidebar toggle
  var sidebar = document.getElementById("adminSidebar");
  var toggle = document.getElementById("adminSidebarToggle");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("is-open");
    });
    document.addEventListener("click", function (e) {
      if (sidebar.classList.contains("is-open") && !sidebar.contains(e.target) && e.target !== toggle && !toggle.contains(e.target)) {
        sidebar.classList.remove("is-open");
      }
    });
  }

  // Confirm before submitting destructive forms (delete buttons)
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!window.confirm(form.getAttribute("data-confirm"))) {
        e.preventDefault();
      }
    });
  });

  // Tag-list repeater widget: add/remove text rows for list-shaped fields
  // (highlights, tech tags, bullets, skills, related project names).
  document.querySelectorAll("[data-tag-list]").forEach(function (widget) {
    var itemsContainer = widget.querySelector("[data-tag-list-items]");
    var addBtn = widget.querySelector("[data-tag-list-add]");
    if (!itemsContainer || !addBtn) return;
    var fieldName = addBtn.getAttribute("data-field-name");

    function makeRow(value) {
      var row = document.createElement("div");
      row.className = "tag-list__item";
      row.setAttribute("data-tag-list-item", "");

      var input = document.createElement("input");
      input.type = "text";
      input.name = fieldName;
      input.value = value || "";
      row.appendChild(input);

      var removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "tag-list__remove";
      removeBtn.setAttribute("data-tag-list-remove", "");
      removeBtn.setAttribute("aria-label", "Remove item");
      removeBtn.innerHTML =
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
        'stroke-linecap="round" stroke-linejoin="round" class="icon"><line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/></svg>';
      row.appendChild(removeBtn);

      return row;
    }

    addBtn.addEventListener("click", function () {
      var row = makeRow("");
      itemsContainer.appendChild(row);
      row.querySelector("input").focus();
    });

    itemsContainer.addEventListener("click", function (e) {
      var removeBtn = e.target.closest("[data-tag-list-remove]");
      if (removeBtn) {
        removeBtn.closest("[data-tag-list-item]").remove();
      }
    });

    // Submit an empty row on Enter -> add a new one instead of submitting the form
    itemsContainer.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && e.target.tagName === "INPUT") {
        e.preventDefault();
        var row = makeRow("");
        itemsContainer.appendChild(row);
        row.querySelector("input").focus();
      }
    });
  });

  // File input: show the chosen filename + a live preview before upload
  document.querySelectorAll('.admin-form-grid input[type="file"]').forEach(function (input) {
    input.addEventListener("change", function () {
      if (!input.files || !input.files[0]) return;
      var wrap = input.closest(".field");
      if (!wrap) return;
      var existing = wrap.querySelector(".admin-image-preview");
      var url = URL.createObjectURL(input.files[0]);
      if (existing) {
        var img = existing.querySelector("img");
        if (img) img.src = url;
      } else {
        var preview = document.createElement("div");
        preview.className = "admin-image-preview";
        preview.innerHTML = '<img src="' + url + '" alt="Selected image preview">';
        wrap.appendChild(preview);
      }
    });
  });

  // Auto-dismiss success/info flash messages after a few seconds
  document.querySelectorAll(".admin-flash--success, .admin-flash--info").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity 0.4s ease";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 400);
    }, 4000);
  });
})();
