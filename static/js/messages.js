$(function() {
  $('.alert').alert();

  // Hide alerts after 5 seconds
  setTimeout(function() {
    $('.alert').alert('close');
  }, 5000);
});
