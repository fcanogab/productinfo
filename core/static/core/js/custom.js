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
