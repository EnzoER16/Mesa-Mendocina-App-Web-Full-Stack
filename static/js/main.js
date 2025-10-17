// Abrir modal login al hacer click
document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
        loginButton.addEventListener('click', () => {
            const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
            loginModal.show();
        });
    }

    // Scroll a platos
    const scrollButtons = document.querySelectorAll('.scroll-to-plates');
    scrollButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(btn.getAttribute('href'));
            target.scrollIntoView({ behavior: 'smooth' });
        });
    });
});
