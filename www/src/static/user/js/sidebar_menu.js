document.addEventListener('DOMContentLoaded', function () {
    // JavaScript để highlight menu đang active
    const currentLocation = window.location.pathname;
    const menuLinks = document.querySelectorAll('.nav-link');

    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');

            // Mở rộng submenu cha nếu menu con đang active
            let parent = link.closest('.submenu');
            while (parent) {
                if (parent.classList.contains('collapse')) {
                    parent.classList.add('show');
                    const toggler = document.querySelector(`[data-bs-target="#${parent.id}"]`);
                    if (toggler) {
                        toggler.setAttribute('aria-expanded', 'true');
                    }
                }
                parent = parent.parentElement.closest('.submenu');
            }
        }
    });
});
function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("collapsed");
}