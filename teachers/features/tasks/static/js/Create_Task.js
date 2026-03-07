
/*Added by Saim Munshi: This is code block deal with the button and content for the side panel for task map and conetent summary */
const taskMapButton = document.getElementById("taskmap-btn");
const summaryButton = document.getElementById("summary-btn");
let summaryContent = document.getElementById("summary-content-div");
let taskMapContent = document.getElementById("task-map-content-div");

/*Added by Saim Munshi: This is code block deal with the button and content for the side panel for task map and conetent summary */


/*___________________________________________________________________________________________________________________________________*/

const courseTitle = document.getElementById("courseSelect");
const courseTitleContainer = document.getElementById("course-title-container");
const courseTitleNode = document.getElementById("course-node-title");
/*___________________________________________________________________________________________________________________________________*/

const courseDescriptionDisplay = document.getElementById("course-description-display");
/*Added by Saim Munshi: Add Button variable*/

const taskTypeSelect = document.getElementById("Task-Type");
const duetaskDateInput = document.getElementById("due_date");
const starttaskDateInput = document.getElementById("start_date");
const addButton = document.getElementById("Add-Task");
const courseTask = document.getElementById("title");
/*___________________________________________________________________________________________________________________________________*/
const updateButton = document.getElementById("Update-Course");

const deleteButton = document.getElementById("Delete-Task");


const courseDescription = document.getElementById("Course-Description");


const descriptionNodeDisplay = document.getElementById("roadmap-body-div");



/*___________________________________________________________________________________________________________________________________*/

/* Task Creation Panel And Task Map And Summary Panel Overview */

/** Added by Saim Munshi:  This is code block deal with the button and content for the side panel for task map and conetent summary and nav buttons **/

taskMapButton.addEventListener('click', (e) => {
    e.preventDefault();
    taskMapButton.style.backgroundColor = "#007bff"
    taskMapButton.style.color = "white"
    summaryButton.style.backgroundColor = "white"
    summaryButton.style.color = "black"
    taskMapContent.classList.remove("hidden-content1");
    summaryContent.classList.add("hidden-content1");
});


summaryButton.addEventListener('click', (e) => {
    e.preventDefault();
    summaryButton.style.backgroundColor = "#007bff"
    summaryButton.style.color = "white"
    taskMapButton.style.backgroundColor = "white"
    taskMapButton.style.color = "black"
    summaryContent.classList.remove("hidden-content1");
    taskMapContent.classList.add("hidden-content1");
});


/** Added by Saim Munshi: Shows Selected title on the side panel with its description **/
let taskArray = [];
let counter = 1;
courseTitle.addEventListener('change', function () {

    const selectedOption = this.options[this.selectedIndex];
    const selectedText = selectedOption.text;
    const selectedDesc = selectedOption.getAttribute("data-description");

    courseTitleContainer.textContent = selectedText;
    courseDescriptionDisplay.textContent = selectedDesc ? selectedDesc : "No course description available.";

});

  addButton.addEventListener('click', e => {
        e.preventDefault();

        /*Added by Saim Munshi: Retreiev taskValue from */
        const taskValue = courseTask.value.trim();

         /*Added by Saim Munshi: if taskvalue does not exist*/
        if (!taskValue) return;
         /* Added By Saim Munshi: this code deal with creating and adding task check box list  */

        const taskIdCheckBox = `task-${counter}`;
        counter++;
        const checkboxDiv = document.createElement("div");
        /* Added By Saim Munshi: creating input checkbox with id equal taskIdCheckBox */
        checkboxDiv.innerHTML = `
            <input class="form-check-input me-2"
                type="checkbox"
                id="${taskIdCheckBox}"
                data-status="not_started">
     
            
            <label class="form-check-label fw-bold" for="${taskIdCheckBox}">
                ${taskValue}
            </label>
   
            <span class="badge bg-secondary ms-2 status-badge mb-1">
                Not Started
            </span>

            <div class="small text-muted mb-3">
                Type: ${taskTypeSelect.value} |
                Start Date: ${starttaskDateInput.value ? starttaskDateInput.value : "No date"}
                Due: ${duetaskDateInput.value ? duetaskDateInput.value : "No date"}
            </div>
        `;
        /* ---------------------------------------------------------------------*/

        /* Added By Saim Munshi:  this logic to set the status for the tasks*/
       const checkboxElement = checkboxDiv.querySelector("input");
       const statusBadge = checkboxDiv.querySelector(".status-badge");

        /* Added By Saim Munshi:  this logic to set the status for the tasks*/
        checkboxElement.addEventListener("change", function () {
        let currentStatus = this.getAttribute("data-status");

        if (currentStatus === "not_started") {
            this.setAttribute("data-status", "in_progress");
            checkboxDiv.className = "form-check mb-2 text-warning";
            statusBadge.className = "badge bg-warning ms-2 status-badge";
            statusBadge.textContent = "In Progress";
            this.checked = false; 
        }
        else if (currentStatus === "in_progress") {
            this.setAttribute("data-status", "completed");
            checkboxDiv.className = "form-check mb-2 text-success";
            statusBadge.className = "badge bg-success ms-2 status-badge";
            statusBadge.textContent = "Completed";
            this.checked = true;
        }
        else {
            this.setAttribute("data-status", "not_started");
            checkboxDiv.className = "form-check mb-2 text-secondary";
            statusBadge.className = "badge bg-secondary ms-2 status-badge";
            statusBadge.textContent = "Not Started";
            this.checked = false;
        }
    });
        /*--------------------------------------------------------------------------*/

        /* Added By Saim Munshi: this code stores the date when the course was created */
        courseDescriptionDisplay.parentNode.appendChild(checkboxDiv);
        const taskType = taskTypeSelect.value;
        const dueDate = duetaskDateInput.value;
        const startDate = starttaskDateInput.value;
        /*------------------------------------------------------------------------------*/

        /*  Added By Saim Munshi: Bases on the type this determines the icon type based on type when type is selected appropriate bootstrap class  is added*/
        /* This is Bootstrap Icon Logic */
        let iconClass = "bi-lock-fill";
        let nodeColor = "bg-primary";
        if ((taskType === "Quiz")) {
            iconClass = "bi-question-circle-fill";
            nodeColor = "bg-warning";
        }
        if (taskType === "Project") {
            iconClass = "bi-clipboard-check-fill";
            nodeColor = "bg-danger";
        }
        if (taskType === "Assignment") {
            iconClass = "bi-journal-text";
            nodeColor = "bg-info";
        }
        /*-----------------------------------------------------------------------------------------------------------*/
         courseTask.value = "";
  })