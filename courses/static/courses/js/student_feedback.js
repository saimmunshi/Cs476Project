document.addEventListener("DOMContentLoaded", () => {

    const feedbackItems = document.querySelectorAll("#activeFeedbackList .feedback-item");

    function getCSRFToken() {
        const tokenElem = document.querySelector('[name=csrfmiddlewaretoken]');
        return tokenElem ? tokenElem.value : '';
    }

    //Added by Matthew/Spooky: Mark as read.
    feedbackItems.forEach(item => {
        const id = item.id.replace("feedback-", "");

        fetch(`/courses/mark-feedback-read/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const statusElem = item.querySelector(".feedback-status");
                if (statusElem) statusElem.textContent = "Status: Read ✔"; // Added by Matthew/Spooky: Update status text
            }
        })
        .catch(err => console.error("Mark read error:", err));
    });

    //Added by Matthew/Spooky: Archive after refresh.
    window.addEventListener("beforeunload", (e) => {
        feedbackItems.forEach(item => {
            const id = item.id.replace("feedback-", "");

            //Added by Matthew/Spooky: Use sendBeacon to archive feedback reliably.
            const url = `/courses/archive-feedback/${id}/`;
            const data = new FormData();
            data.append("csrfmiddlewaretoken", getCSRFToken());

            navigator.sendBeacon(url, data);
        });
    });

});