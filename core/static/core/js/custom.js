function copyContactsToClipboard(eng, bus, psrd) {
  const text = [eng, bus, psrd].join(';');
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(function() {
      alert('Contacts copied to clipboard: ' + text);
    }, function(err) {
      alert('Failed to copy: ' + err);
    });
  } else {
    // Fallback for very old browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      alert('Contacts copied to clipboard: ' + text);
    } catch (err) {
      alert('Failed to copy: ' + err);
    }
    document.body.removeChild(textarea);
  }
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
