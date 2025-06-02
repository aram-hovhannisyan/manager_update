let allWhite_tds = document.querySelectorAll('td');

document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    allWhite_tds.forEach((td) => {
      if (td.style.color === 'white' && parseInt(td.textContent.trim()) !== 0) {
        td.style.color = 'rgb(20, 20, 20)';
      }
    });
  }, 2000); // Add a 2000 millisecond (2 second) delay
});