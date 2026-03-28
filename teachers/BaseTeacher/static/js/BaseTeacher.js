document.addEventListener("DOMContentLoaded", function () {
    const hideBtn = document.getElementById("hideSidebarBtn");
    const showBtn = document.getElementById("showSidebarBtn");
    const body = document.body;

    if (!hideBtn || !showBtn) return;

    hideBtn.addEventListener("click", function () {
        body.classList.add("sidebar-hidden");
    });

    showBtn.addEventListener("click", function () {
        body.classList.remove("sidebar-hidden");
    });
});