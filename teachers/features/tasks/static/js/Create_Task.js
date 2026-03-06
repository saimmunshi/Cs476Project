
/*Added by Saim Munshi: This is code block deal with the button and content for the side panel for task map and conetent summary */
const taskMapButton = document.getElementById("taskmap-btn");
const summaryButton = document.getElementById("summary-btn");
let summaryContent = document.getElementById("summary-content-div");
let taskMapContent = document.getElementById("task-map-content-div");

/*Added by Saim Munshi: This is code block deal with the button and content for the side panel for task map and conetent summary */


/*___________________________________________________________________________________________________________________________________*/
/*Added by Saim Munshi: Course title*/
const courseTitle = document.getElementById("courseSelect");
const courseTitleContainer = document.getElementById("course-title-container");
const courseTitleNode = document.getElementById("course-node-title");
/*___________________________________________________________________________________________________________________________________*/

const courseDescriptionDisplay = document.getElementById("course-description-display");


const updateButton = document.getElementById("Update-Course");
const addButton = document.getElementById("Add-Task");
const deleteButton = document.getElementById("Delete-Task");

const courseTask = document.getElementById("title");
const courseDescription = document.getElementById("Course-Description");


const descriptionNodeDisplay = document.getElementById("roadmap-body-div");
const taskDateInput = document.getElementById("Task-Date");
const taskTypeSelect = document.getElementById("Task-Type");

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

