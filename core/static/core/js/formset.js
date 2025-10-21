document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("add-form");
    const totalForms = document.getElementById("id_component_features-TOTAL_FORMS");
    const formTable = document.querySelector("#feature-table tbody");
    const formRows = document.querySelectorAll(".formset-row");
  
    addButton.addEventListener("click", function () {
      const formNum = parseInt(totalForms.value);
      const newForm = formRows[0].cloneNode(true);
      const formRegex = new RegExp(`component_features-(\\d+)-`, "g");
  
      newForm.innerHTML = newForm.innerHTML.replace(formRegex, `component_features-${formNum}-`);
      formTable.appendChild(newForm);
      totalForms.value = formNum + 1;
  
      newForm.querySelectorAll("input, select, textarea").forEach(el => {
        // Don't clear id field in blank row template.
        if (el.name && el.name.endsWith('-id')) {
          el.value = '';
          return;
        }
        if (el.type === "checkbox" || el.type === "radio") {
          el.checked = false;
        } else {
          el.value = "";
        }
      });
    });
  
    // Handle removing unsaved rows
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("remove-row")) {
        e.target.closest("tr").remove();
        const rows = document.querySelectorAll(".formset-row");
        totalForms.value = rows.length;
      }
    });
  });
