document.addEventListener("DOMContentLoaded", function() {
    const flashMessage = document.querySelector('.flash-message')
    if (flashMessage.style.display !== 'none') {
      setTimeout(function() {
        flashMessage.style.display = 'none'
      }, 1000)
    }
  })