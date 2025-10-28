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


function addFormsetForm(prefix) {
    var totalForms = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
    var formCount = parseInt(totalForms.value);
    var formsetDiv = document.getElementById(prefix + '_formset');
    var lastForm = formsetDiv.querySelector('.dynamic-form:last-child');
    var newForm = lastForm.cloneNode(true);
    // Regex replace the form number in all input names/ids
    newForm.innerHTML = newForm.innerHTML.replace(
        new RegExp(prefix + '-(\\d+)-', 'g'), prefix + '-' + formCount + '-'
    );
    // Clear inputs in the new form
    Array.from(newForm.querySelectorAll('input')).forEach(function(input){
        input.value = '';
        if(input.type === 'checkbox' || input.type === 'radio') input.checked = false;
    });
    formsetDiv.appendChild(newForm);
    totalForms.value = formCount + 1;
}

document.getElementById('add-jira').addEventListener('click', function(){
    addFormsetForm('jira');
});
document.getElementById('add-result').addEventListener('click', function(){
    addFormsetForm('result');
});
document.getElementById('add-document').addEventListener('click', function(){
    addFormsetForm('document');
});
