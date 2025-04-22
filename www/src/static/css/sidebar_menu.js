/**
 * Clean Sidebar JS with Single Dropdown Icon
 * Removes duplicate dropdown icons and adds popup functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const sidebar = document.getElementById('sidebar');
    const contentArea = document.querySelector('.content-area');
    const toggleBtn = document.querySelector('.toggle-sidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const menuItems = document.querySelectorAll('.menu-item');
    const menuToggles = document.querySelectorAll('.menu-toggle');
    
    // Apply saved sidebar state on load
    const savedState = localStorage.getItem('sidebarState');
    if (savedState === 'collapsed') {
        sidebar.classList.add('collapsed');
        if (contentArea) contentArea.classList.add('expanded');
    }
    
    // Cleanup duplicate icons
    function cleanupDuplicateIcons() {
        // Remove the second chevron in each menu toggle
        menuToggles.forEach(toggle => {
            const icons = toggle.querySelectorAll('i.fa-chevron-right, i.fa-angle-right');
        });
    }
    
    // Call cleanup on page load
    cleanupDuplicateIcons();
    
    // Create popup menus for menu items with submenus
    function createPopupMenus() {
        menuItems.forEach(item => {
            const submenu = item.querySelector('.submenu');
            const menuLink = item.querySelector('.menu-toggle') || item.querySelector('.menu-link');
            
            // Only create popup for items with submenu
            if (submenu && menuLink) {
                const menuText = menuLink.querySelector('.menu-text')?.textContent || '';
                const submenuLinks = submenu.querySelectorAll('.submenu-link');
                
                if (submenuLinks.length > 0) {
                    // Create popup menu
                    const popupMenu = document.createElement('div');
                    popupMenu.className = 'popup-menu';
                    
                    // Add header with menu name
                    const popupHeader = document.createElement('div');
                    popupHeader.className = 'popup-header';
                    popupHeader.textContent = menuText;
                    popupMenu.appendChild(popupHeader);
                    
                    // Add submenu items to popup
                    submenuLinks.forEach(link => {
                        const popupItem = document.createElement('a');
                        popupItem.className = 'popup-item';
                        popupItem.href = link.getAttribute('href');
                        popupItem.textContent = link.textContent.trim();
                        popupMenu.appendChild(popupItem);
                    });
                    
                    // Add popup to menu item
                    item.appendChild(popupMenu);
                    
                    // Toggle popup when clicking menu item in collapsed state
                    menuLink.addEventListener('click', function(e) {
                        if (sidebar.classList.contains('collapsed')) {
                            e.preventDefault();
                            
                            // Close other popups
                            document.querySelectorAll('.popup-menu.show').forEach(popup => {
                                if (popup !== popupMenu) {
                                    popup.classList.remove('show');
                                }
                            });
                            
                            // Toggle this popup
                            popupMenu.classList.toggle('show');
                        }
                    });
                }
            }
        });
        
        // Close all popups when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.menu-toggle') && !e.target.closest('.menu-link') && !e.target.closest('.popup-menu')) {
                document.querySelectorAll('.popup-menu.show').forEach(popup => {
                    popup.classList.remove('show');
                });
            }
        });
    }
    
    // Call on page load to create popup menus
    createPopupMenus();
    
    // Handle sidebar toggle from sidebar
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            toggleSidebar();
        });
    }
    
    // Handle sidebar toggle from header button
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function() {
            toggleSidebar();
        });
    }
    
    // Toggle sidebar function
    function toggleSidebar() {
        const isCollapsing = !sidebar.classList.contains('collapsed');
        
        // Track which submenus were open
        let openSubmenus = [];
        if (isCollapsing) {
            menuItems.forEach((item, index) => {
                const submenu = item.querySelector('.submenu');
                if (submenu && submenu.classList.contains('show')) {
                    openSubmenus.push(index);
                }
            });
        }
        
        // Toggle sidebar state
        sidebar.classList.toggle('collapsed');
        if (contentArea) contentArea.classList.toggle('expanded');
        
        // Close any open popups
        document.querySelectorAll('.popup-menu.show').forEach(popup => {
            popup.classList.remove('show');
        });
        
        // After expanding, restore open submenus
        if (!isCollapsing) {
            setTimeout(() => {
                openSubmenus.forEach(index => {
                    if (menuItems[index]) {
                        const submenu = menuItems[index].querySelector('.submenu');
                        const dropdownIcon = menuItems[index].querySelector('.dropdown-icon');
                        
                        if (submenu) {
                            submenu.classList.add('show');
                            if (dropdownIcon) {
                                dropdownIcon.style.transform = 'rotate(-180deg)';
                            }
                        }
                    }
                });
            }, 300);
        }
        
        // Save state to localStorage
        if (sidebar.classList.contains('collapsed')) {
            localStorage.setItem('sidebarState', 'collapsed');
        } else {
            localStorage.setItem('sidebarState', 'expanded');
        }
    }
    
    // Handle dropdown toggle clicks for expanded sidebar
    menuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // Only process clicks when sidebar is expanded
            if (!sidebar.classList.contains('collapsed')) {
                e.preventDefault();
                const menuItem = this.closest('.menu-item');
                const submenu = menuItem.querySelector('.submenu');
                const dropdownIcon = menuItem.querySelector('.dropdown-icon');
                
                if (submenu) {
                    // Toggle submenu visibility
                    submenu.classList.toggle('show');
                    
                    // Update dropdown icon
                    if (dropdownIcon) {
                        dropdownIcon.style.transform = submenu.classList.contains('show') 
                            ? 'rotate(-180deg)' 
                            : 'rotate(0deg)';
                    }
                    
                    // Update aria-expanded attribute
                    menuItem.setAttribute('aria-expanded', submenu.classList.contains('show'));
                }
            }
        });
    });
    
    // Handle responsive behavior
    function handleResponsive() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            if (contentArea) contentArea.classList.add('expanded');
        }
    }
    
    // Handle window resize
    window.addEventListener('resize', handleResponsive);
    
    // Initial responsive check
    handleResponsive();
});