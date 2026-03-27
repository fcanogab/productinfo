function copyContactEmails(e) {
  e.preventDefault();
  var link = document.getElementById('copy-emails-link');
  var emails = [
    link.dataset.engEmail,
    link.dataset.bizEmail,
    link.dataset.psrdEmail
  ].filter(Boolean);
  if (emails.length === 0) {
    alert('No contact emails to copy.');
    return;
  }
  navigator.clipboard.writeText(emails.join('; ')).then(function() {
    var original = link.innerHTML;
    link.innerHTML = '&#10003; Copied!';
    setTimeout(function() { link.innerHTML = original; }, 2000);
  });
}

function openContactModal(contactType, targetSelectId) {
  document.getElementById('contactModalType').value = contactType;
  document.getElementById('contactModalTarget').value = targetSelectId;
  document.getElementById('contactModalName').value = '';
  document.getElementById('contactModalEmail').value = '';
  document.getElementById('contactModalError').classList.add('d-none');
  document.getElementById('contactModalLabel').textContent = 'New ' + contactType + ' Contact';
  new bootstrap.Modal(document.getElementById('contactModal')).show();
}

function saveContact() {
  var modal = document.getElementById('contactModal');
  var name = document.getElementById('contactModalName').value.trim();
  var email = document.getElementById('contactModalEmail').value.trim();
  var contactType = document.getElementById('contactModalType').value;
  var targetSelectId = document.getElementById('contactModalTarget').value;
  var errorDiv = document.getElementById('contactModalError');

  if (!name) {
    errorDiv.textContent = 'Name is required.';
    errorDiv.classList.remove('d-none');
    return;
  }

  var ajaxUrl = modal.dataset.ajaxUrl;
  var csrfToken = modal.dataset.csrfToken;

  var formData = new FormData();
  formData.append('name', name);
  formData.append('email', email);
  formData.append('type', contactType);
  formData.append('csrfmiddlewaretoken', csrfToken);

  fetch(ajaxUrl, {
    method: 'POST',
    body: formData,
  })
  .then(function(response) {
    return response.json().then(function(data) {
      return {ok: response.ok, data: data};
    });
  })
  .then(function(result) {
    if (!result.ok) {
      errorDiv.textContent = result.data.error || 'An error occurred.';
      errorDiv.classList.remove('d-none');
      return;
    }
    var select = document.getElementById(targetSelectId);
    var option = new Option(result.data.name, result.data.id, true, true);
    select.appendChild(option);
    bootstrap.Modal.getInstance(modal).hide();
  })
  .catch(function() {
    errorDiv.textContent = 'An unexpected error occurred.';
    errorDiv.classList.remove('d-none');
  });
}

function copySelectedFeatures(e) {
  e.preventDefault();
  var all = document.querySelectorAll('#id_features input[type="checkbox"]');
  var lines = Array.from(all).map(function(cb) { return cb.parentElement.textContent.trim(); });
  if (lines.length === 0) {
    return;
  }
  var btn = document.getElementById('copyFeaturesBtn');
  navigator.clipboard.writeText(lines.join('\n')).then(function() {
    var original = btn.innerHTML;
    btn.innerHTML = '<i class="bi bi-check"></i> Copied!';
    setTimeout(function() { btn.innerHTML = original; }, 1500);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('standard-compliance-form');
  var dataEl = document.getElementById('standard-compliance-data');
  if (form && dataEl) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var select = document.getElementById('standard-select');
      var standardPk = select.value;
      if (!standardPk) {
        alert('Please select a standard.');
        return;
      }
      var componentPk = dataEl.dataset.componentPk;
      window.location.href = '/components/' + componentPk + '/standard/' + standardPk + '/';
    });
  }
});
