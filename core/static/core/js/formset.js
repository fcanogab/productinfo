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


function toggleRequirements(id) {
    var el = document.getElementById(id);
    if (el.style.display === "none" || el.style.display === "") {
        el.style.display = "block";
    } else {
        el.style.display = "none";
    }
}
