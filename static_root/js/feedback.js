document.addEventListener("DOMContentLoaded", () => {

  const courseSelect = document.getElementById("courseSelect");
  const taskSelect = document.getElementById("taskSelect");
  const studentSelect = document.getElementById("studentSelect");

  const messageInput = document.getElementById("messageInput");
  const attachmentInput = document.getElementById("attachmentInput");

  const submitBtn = document.getElementById("submitFeedbackBtn");

  const feedbackList = document.getElementById("feedbackList");


  function getCSRFToken() {
      const name = "csrftoken";
      const cookies = document.cookie.split(";");

      for (let cookie of cookies) {
          cookie = cookie.trim();

          if (cookie.startsWith(name + "=")) {
              return decodeURIComponent(cookie.substring(name.length + 1));
          }
      }

      return null;
  }


  async function loadTasks(courseId) {

      taskSelect.innerHTML = '<option value="">Loading...</option>';

      try {

          const response = await fetch(`/courses/api/tasks/${courseId}/`);

          if (!response.ok) {
              throw new Error("Failed to load tasks");
          }

          const tasks = await response.json();

          taskSelect.innerHTML = '<option value="">Select Task</option>';

          tasks.forEach(task => {

              const option = document.createElement("option");

              option.value = task.id;
              option.textContent = task.title;

              taskSelect.appendChild(option);

          });

      } catch (error) {

          console.error("Task load error:", error);

          taskSelect.innerHTML = '<option value="">Error loading tasks</option>';

      }

  }


  if (courseSelect) {

      courseSelect.addEventListener("change", () => {

          const courseId = courseSelect.value;

          if (courseId) {
              loadTasks(courseId);
          }

      });

  }


  async function submitFeedback() {

      const receiver = studentSelect.value;
      const course = courseSelect.value;
      const task = taskSelect.value;
      const message = messageInput.value;
      const file = attachmentInput.files[0];

      if (!receiver || !course || !task || !message) {

          alert("Please complete all required fields.");
          return;

      }

      const formData = new FormData();

      formData.append("receiver", receiver);
      formData.append("course", course);
      formData.append("task", task);
      formData.append("message", message);

      if (file) {
          formData.append("attachment", file);
      }

      try {

          const response = await fetch("/courses/send_feedback/", {

              method: "POST",

              headers: {
                  "X-CSRFToken": getCSRFToken()
              },

              body: formData

          });

          if (!response.ok) {
              throw new Error("Failed to send feedback");
          }

          const result = await response.json();

          addFeedbackToList(result);

          messageInput.value = "";
          attachmentInput.value = "";

          alert("Feedback sent successfully!");

      } catch (error) {

          console.error("Submission error:", error);
          alert("Error sending feedback");

      }

  }


  if (submitBtn) {

      submitBtn.addEventListener("click", (e) => {

          e.preventDefault();
          submitFeedback();

      });

  }


  function addFeedbackToList(data) {

      if (!feedbackList) return;

      const item = document.createElement("div");

      item.className = "feedback-item";

      let attachmentHTML = "";

      if (data.attachment_url) {

          attachmentHTML = `
              <a href="${data.attachment_url}" target="_blank">
                  View Attachment
              </a>
          `;

      }

      item.innerHTML = `

          <div class="feedback-meta">
              <strong>${data.receiver}</strong> |
              ${data.task} |
              ${data.created_at}
          </div>

          <p>${data.message}</p>

          ${attachmentHTML}

          <p>Status: Unread</p>

      `;

      feedbackList.prepend(item);

  }


  async function markAsRead(feedbackId, button) {

      try {

          const response = await fetch(`/courses/mark_read/${feedbackId}/`, {

              method: "POST",

              headers: {
                  "X-CSRFToken": getCSRFToken()
              }

          });

          if (!response.ok) {
              throw new Error("Failed to mark as read");
          }

          button.textContent = "Read ✔";
          button.disabled = true;

      } catch (error) {

          console.error("Read update error:", error);

      }

  }


  document.querySelectorAll(".mark-read-btn").forEach(btn => {

      btn.addEventListener("click", () => {

          const feedbackId = btn.dataset.id;

          markAsRead(feedbackId, btn);

      });

  });

});