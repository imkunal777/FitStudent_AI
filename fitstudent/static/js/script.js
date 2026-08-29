/**
 * FitStudent AI – script.js
 * Minimal JavaScript for UI interactions and client-side form validation.
 * All critical logic remains on the Python/Flask backend.
 */

// ---------------------------------------------------------------
// Mobile navigation toggle
// ---------------------------------------------------------------
(function () {
  const toggle = document.getElementById("navToggle");
  const links  = document.getElementById("navLinks");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }
})();

// ---------------------------------------------------------------
// Auto-dismiss flash alerts after 5 seconds
// ---------------------------------------------------------------
(function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.5s";
      alert.style.opacity = "0";
      setTimeout(function () { alert.remove(); }, 500);
    }, 5000);
  });
})();

// ---------------------------------------------------------------
// Profile form – basic client-side validation
// ---------------------------------------------------------------
(function () {
  const form = document.getElementById("profileForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const errors = [];

    const name = form.querySelector("#name").value.trim();
    if (!name) errors.push("Name is required.");

    const age = parseInt(form.querySelector("#age").value, 10);
    if (isNaN(age) || age < 10 || age > 100)
      errors.push("Age must be between 10 and 100.");

    const height = parseFloat(form.querySelector("#height").value);
    if (isNaN(height) || height < 50 || height > 300)
      errors.push("Height must be between 50 and 300 cm.");

    const weight = parseFloat(form.querySelector("#weight").value);
    if (isNaN(weight) || weight < 20 || weight > 500)
      errors.push("Weight must be between 20 and 500 kg.");

    if (errors.length > 0) {
      e.preventDefault();
      _showErrors(errors);
    }
  });
})();

// ---------------------------------------------------------------
// Preferences form – basic client-side validation
// ---------------------------------------------------------------
(function () {
  const form = document.getElementById("preferencesForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const errors = [];

    const mins = parseInt(form.querySelector("#daily_workout_time").value, 10);
    if (isNaN(mins) || mins < 10 || mins > 240)
      errors.push("Workout time must be between 10 and 240 minutes.");

    const dietType = form.querySelector("#diet_type").value;
    if (!dietType) errors.push("Please select a diet type.");

    const equipment = form.querySelector("#available_equipment").value;
    if (!equipment) errors.push("Please select available equipment.");

    const budgetChecked = form.querySelector("input[name='budget']:checked");
    if (!budgetChecked) errors.push("Please select a budget option.");

    if (errors.length > 0) {
      e.preventDefault();
      _showErrors(errors);
    }
  });

  // Budget option visual toggle
  const budgetLabels = form.querySelectorAll(".budget-option");
  budgetLabels.forEach(function (label) {
    const radio = label.querySelector("input[type='radio']");
    if (radio) {
      radio.addEventListener("change", function () {
        budgetLabels.forEach(function (l) { l.classList.remove("active"); });
        label.classList.add("active");
      });
    }
  });
})();

// ---------------------------------------------------------------
// Progress form – set today's date if empty
// ---------------------------------------------------------------
(function () {
  const dateInput = document.getElementById("record_date");
  if (dateInput && !dateInput.value) {
    dateInput.value = new Date().toISOString().split("T")[0];
  }
})();

// ---------------------------------------------------------------
// Progress form – basic client-side validation
// ---------------------------------------------------------------
(function () {
  const form = document.getElementById("progressForm");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const errors = [];

    const w = parseFloat(form.querySelector("#weight").value);
    if (isNaN(w) || w < 20 || w > 500)
      errors.push("Weight must be between 20 and 500 kg.");

    const d = form.querySelector("#record_date").value;
    if (!d) errors.push("Date is required.");

    if (errors.length > 0) {
      e.preventDefault();
      _showErrors(errors);
    }
  });
})();

// ---------------------------------------------------------------
// Helper – inject error messages above the first form-group
// ---------------------------------------------------------------
function _showErrors(errors) {
  // Remove any previous error list
  const existing = document.querySelector(".js-error-list");
  if (existing) existing.remove();

  const list = document.createElement("div");
  list.className = "alert alert-danger js-error-list";
  list.innerHTML = errors.map(function (e) { return "• " + e; }).join("<br>");

  // Insert before the first form-group inside the active form
  const firstGroup = document.querySelector("form .form-group");
  if (firstGroup) {
    firstGroup.parentNode.insertBefore(list, firstGroup);
  }

  // Scroll to top of form
  const formEl = document.querySelector("form");
  if (formEl) formEl.scrollIntoView({ behavior: "smooth", block: "start" });
}
