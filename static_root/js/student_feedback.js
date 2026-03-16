document.addEventListener("DOMContentLoaded", () => {

    const unreadCards = document.querySelectorAll(".feedback-card.unread");

    unreadCards.forEach(card => {

        card.style.border = "2px solid #ff9800";

    });

});