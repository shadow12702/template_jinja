        // Toggle user dropdown
        function toggleUserDropdown() {
            document.getElementById("userDropdown").classList.toggle("show");
        }

        // Toggle sidebar
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const contentArea = document.querySelector('.content-area');
            const toggleBtn = document.getElementById('sidebarToggleBtn');
            
            sidebar.classList.toggle('collapsed');
            contentArea.classList.toggle('expanded');
            
            if (sidebar.classList.contains('collapsed')) {
                toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
                localStorage.setItem('sidebarState', 'collapsed');
            } else {
                toggleBtn.innerHTML = '<i class="fas fa-times"></i>';
                localStorage.setItem('sidebarState', 'expanded');
            }
        }

        // Global variables
        let selectedCustomer = null;
        let selectedCustomerCode = null;
        let selectedDatabase = null;
        let selectedDatabaseCode = null;

        // Initialize on document load
        document.addEventListener("DOMContentLoaded", function () {
            // Apply saved sidebar state
            const sidebar = document.getElementById('sidebar');
            const contentArea = document.querySelector('.content-area');
            const toggleBtn = document.getElementById('sidebarToggleBtn');
            const savedState = localStorage.getItem('sidebarState');
            
            if (savedState === 'collapsed') {
                sidebar.classList.add('collapsed');
                contentArea.classList.add('expanded');
                toggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
            } else {
                toggleBtn.innerHTML = '<i class="fas fa-times"></i>';
            }
        
            // Set up customer selection
            const customerButtons = document.querySelectorAll(".customer-select-btn");
            customerButtons.forEach((button) => {
                button.addEventListener("click", function () {
                    selectCustomer(
                        this.getAttribute("data-cus-name"),
                        this.value
                    );
                });
            });

            // Set up database selection
            const databaseButtons = document.querySelectorAll(".database-select-btn");
            databaseButtons.forEach((button) => {
                button.addEventListener("click", function () {
                    selectDatabase(
                        this.getAttribute("data-db-name"),
                        this.value
                    );
                });
            });
        });

        // Customer selection handler
        function selectCustomer(cusName, cusCode) {
            selectedCustomer = cusName;
            selectedCustomerCode = cusCode;
            document.getElementById("customerDropdown").textContent = cusName;
            document.getElementById("databaseDropdownContainer").style.display = "block";
            
            // Reset database selection
            selectedDatabase = null;
            selectedDatabaseCode = null;
            document.getElementById("databaseDropdown").textContent = "Select Database";
        }

        // Database selection handler
        function selectDatabase(dbName, cusCode) {
            selectedDatabase = dbName;
            selectedDatabaseCode = cusCode;
            document.getElementById("databaseDropdown").textContent = dbName;
        }

        // Close dropdowns when clicking outside
        window.addEventListener("click", function (event) {
            // Close user dropdown
            if (!event.target.matches('.avatar') && !event.target.closest('#userDropdown')) {
                const userDropdown = document.getElementById('userDropdown');
                if (userDropdown && userDropdown.classList.contains('show')) {
                    userDropdown.classList.remove('show');
                }
            }
            
            // Close other dropdowns
            if (!event.target.matches(".dropdown-toggle") && !event.target.matches(".dropdown-item")) {
                const dropdowns = document.getElementsByClassName("dropdown-menu");
                for (let i = 0; i < dropdowns.length; i++) {
                    const openDropdown = dropdowns[i];
                    if (openDropdown.classList.contains("show")) {
                        openDropdown.classList.remove("show");
                    }
                }
            }
        });