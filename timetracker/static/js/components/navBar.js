// Inspired by https://bulma.io/documentation/components/navbar/

export default function() {
    // Get all "navbar-burger" elements
    for(const burger of document.querySelectorAll('.navbar-burger')) {
        burger.addEventListener('click', () => {

            const target = document.getElementById(burger.dataset.target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            burger.classList.toggle('is-active');
            target.classList.toggle('is-active');

        });
    }
};
