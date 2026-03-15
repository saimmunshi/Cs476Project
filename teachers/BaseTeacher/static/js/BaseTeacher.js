function removeNotification(notificationId) {
    // Get the specific button element
    const btn = document.getElementById('remove-notification-' + notificationId);
    // Find the card container to remove it later
    const card = btn.closest('.chat-message');
    // Get the CSRF token from the nearby input
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send the POST request to your URL
    fetch(`/users/teachers/notification/delete/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            // Success: Remove the element from the DOM
            card.remove();
        } else {
            console.error("Deletion failed. Server returned error.");
        }
    })
    .catch(error => console.error('Error:', error));
}