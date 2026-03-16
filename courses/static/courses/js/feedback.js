document.addEventListener("DOMContentLoaded", () => {

    const submitBtn = document.getElementById("submitFeedbackBtn");
    const feedbackList = document.getElementById("feedbackList");

    async function submitFeedback() {
        //Added by Matthew/Spooky: Collect form data and send feedback via API.
        const form = document.querySelector(".feedback-form");
        const formData = new FormData(form);

        try {
            const result = await apiRequest(
                "/courses/send-feedback/",
                "POST",
                formData
            );
            //Added by Matthew/Spooky: Immediately show new feedback.
            addFeedbackToList(result);
            //Added by Matthew/Spooky: Clear after submission.
            form.reset();

            alert("Feedback sent successfully!");
        } catch (error) {
            console.error(error);
            alert("Error sending feedback");
        }
    }

    if (submitBtn) {
        //Added by Matthew/Spooky: Attach click handler to feedback button.
        submitBtn.addEventListener("click", (e) => {
            e.preventDefault();
            submitFeedback();
        });
    }

    function addFeedbackToList(data) {
        if (!feedbackList) return;

        const item = document.createElement("div");

        item.className = "feedback-item";
        item.id = `feedback-${data.id}`;

        let attachmentHTML = "";

        if (data.attachment_url) {
            attachmentHTML = `<a href="${data.attachment_url}" target="_blank">View Attachment</a>`;
        }

        item.innerHTML = `
            <div class="feedback-meta">
                <strong>${data.receiver}</strong> | ${data.task || "General"} | ${data.created_at}
            </div>

            <p>${data.message}</p>

            ${attachmentHTML}

            <p class="feedback-status">Status: Unread</p>

            <button class="mark-read-btn" data-id="${data.id}">Mark as Read</button>
            <button class="delete-feedback" data-id="${data.id}">Delete</button>
        `;
        //Added by Matthew/Spooky: Add new feedback to top of list.
        feedbackList.prepend(item);
    }

});