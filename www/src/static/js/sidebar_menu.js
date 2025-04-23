function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("collapsed");

    if (sidebar.classList.contains("collapsed")) {
        localStorage.setItem("sidebarState", "collapsed");
        sidebar.style.width = "60px";
        
        // Close all open submenus when collapsing
        const openSubmenus = sidebar.querySelectorAll('.submenu.show');
        openSubmenus.forEach(submenu => {
            submenu.classList.remove('show');
        });
    } else {
        localStorage.setItem("sidebarState", "expanded");
        sidebar.style.width = "250px";
    }
}

document.addEventListener("DOMContentLoaded", function () {
	const sidebar = document.getElementById("sidebar");
	const savedState = localStorage.getItem("sidebarState");

	if (savedState === "collapsed") {
		sidebar.classList.add("collapsed");
		sidebar.style.width = "60px";
	}
});
