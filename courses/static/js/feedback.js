const students = [
{ id: 1, name: "Alice Johnson" },
{ id: 2, name: "Michael Smith" },
{ id: 3, name: "Sarah Lee" }
];

const tasks = [
{ id: 1, title: "Task 1" },
{ id: 2, title: "Task 2" },
{ id: 3, title: "Task 3" }
];

let feedbackData = [];
let notifications = [];

const selectStudent = document.getElementById("selectStudent");
const selectTask = document.getElementById("selectTask");
const feedbackForm = document.getElementById("feedbackForm");
const feedbackList = document.getElementById("feedbackList");
const studentNotificationList = document.getElementById("studentNotificationList");
const imageInput = document.getElementById("imageInput");

students.forEach(student => {
  const option = document.createElement("option");
  option.value = student.id;
  option.textContent = student.name;
  selectStudent.appendChild(option);
});

tasks.forEach(task => {
  const option = document.createElement("option");
  option.value = task.id;
  option.textContent = task.title;
  selectTask.appendChild(option);
});

feedbackForm.addEventListener("submit", function(e) {
  e.preventDefault();

  const studentId = parseInt(selectStudent.value);
  const taskId = parseInt(selectTask.value);
  const feedbackType = document.getElementById("feedbackType").value;
  const feedbackText = document.getElementById("feedbackText").value;

   if (!studentId || !taskId) {
    alert("Please select both a student and a task.");
    return;
  }

  const student = students.find(s => s.id === studentId);
  const task = tasks.find(t => t.id === taskId);
  const feedbackId = Date.now();

  const files = Array.from(imageInput.files || []);
  const attachments = files.map(file => ({
  name: file.name,
  url: URL.createObjectURL(file)
}));

  const newFeedback = {
  id: feedbackId,
  studentId,
  studentName: student.name,
  taskTitle: task.title,
  type: feedbackType,
  text: feedbackText,
  date: new Date().toLocaleString(),
  attachments: attachments
  };

  feedbackData.push(newFeedback);

  notifications.push({
  feedbackId: feedbackId,
  studentId: studentId,
  message: `New ${feedbackType} feedback for "${task.title}"`,
  date: new Date().toLocaleString(),
  read: false
});

  renderFeedback();
  renderStudentNotifications();
  feedbackForm.reset();
  imageInput.value = "";
});

function renderFeedback() {
feedbackList.innerHTML = "";
feedbackData.forEach(item => {
const relatedNotification = notifications.find(n => n.feedbackId === item.id);
const readStatus = relatedNotification?.read ? "Read" : "Unread";

feedbackList.innerHTML += `
  <div class="feedback-item">
  <div class="feedback-meta">
  <strong>${item.studentName}</strong> | ${item.taskTitle} | ${item.type} | ${item.date}
  </div>
  <div>${item.text}</div>
  ${item.attachments.length ? `
  <div class="attachment-preview">
  <strong>Attachments:</strong>
  ${item.attachments.map(a => `<a href="${a.url}" target="_blank">${a.name}</a>`).join("")}
  </div>` : ""}
  <small>Status: ${readStatus}</small>
  <div class="feedback-actions">
  <button onclick="editFeedback(${item.id})">Edit</button>
  <button onclick="deleteFeedback(${item.id})">Delete</button>
  </div>
  </div>
  `;
});
}

function renderStudentNotifications() {
studentNotificationList.innerHTML = "";
notifications.forEach(n => {
studentNotificationList.innerHTML += `
  <div class="notification-item">
  <strong>${n.message}</strong><br>
  <small>${n.date}</small><br>
  <small>Status: ${n.read ? "Read" : "Unread"}</small><br>
  ${!n.read ? `<button onclick="markAsRead(${n.feedbackId})">Mark as Read</button>` : ""}
   </div>
 `;
});
}

window.markAsRead = function(feedbackId) {
const notification = notifications.find(n => n.feedbackId === feedbackId);
if (notification) {
  notification.read = true;
  renderFeedback();
  renderStudentNotifications();
}
}

  window.editFeedback = function(id) {
  const item = feedbackData.find(f => f.id === id);
  const newText = prompt("Edit feedback:", item.text);
  if (newText !== null) {
    item.text = newText;
    renderFeedback();
  }
  }

  window.deleteFeedback = function(id) {
  feedbackData = feedbackData.filter(f => f.id !== id);
  notifications = notifications.filter(n => n.feedbackId !== id);
  renderFeedback();
  renderStudentNotifications();
}

