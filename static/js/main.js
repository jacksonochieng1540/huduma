// Real-time updates for staff dashboard
function updateTicketStatus() {
  if (document.getElementById('pendingTicketsTable')) {
    fetch(window.location.href)
      .then(response => response.text())
      .then(html => {
        const newContent = new DOMParser()
          .parseFromString(html, 'text/html')
          .getElementById('pendingTicketsTable');
        document.getElementById('pendingTicketsTable').innerHTML = newContent.innerHTML;
      });
  }
}

// Auto-refresh every 30 seconds
setInterval(updateTicketStatus, 30000);

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (el) {
    return new bootstrap.Tooltip(el);
  });
});