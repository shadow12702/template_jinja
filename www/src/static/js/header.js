// User dropdown toggle
function toggleUserDropdown() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.classList.toggle('show');
    
    // Close when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInside = document.querySelector('.user-dropdown').contains(event.target);
        if (!isClickInside && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    });
}

// Sidebar toggle functionality
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar') || document.querySelector('.sidebar');
    const mainContent = document.getElementById('mainContent') || document.querySelector('.main-content');
    
    if (sidebar) {
        sidebar.classList.toggle('collapsed');
        
        if (mainContent) {
            mainContent.classList.toggle('expanded');
        }
    }
}

// Customer selection functionality
document.addEventListener('DOMContentLoaded', function() {
    // Customer selection
    const customerButtons = document.querySelectorAll('.customer-select-btn');
    const customerDropdown = document.getElementById('customerDropdown');
    const dbDropdownContainer = document.getElementById('databaseDropdownContainer');
    
    customerButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cusCode = this.getAttribute('data-cus-code');
            const cusName = this.getAttribute('data-cus-name');
            
            // Update dropdown button text
            customerDropdown.textContent = cusName;
            
            // Show database dropdown
            dbDropdownContainer.style.display = 'block';
            
            // Filter database options
            filterDatabases(cusCode);
        });
    });
    
    // Database selection
    const databaseButtons = document.querySelectorAll('.database-select-btn');
    const databaseDropdown = document.getElementById('databaseDropdown');
    
    databaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const dbName = this.getAttribute('data-db-name');
            
            // Update dropdown button text
            databaseDropdown.textContent = dbName;
            
            // Save selection to session storage for persistence
            sessionStorage.setItem('selectedCustomer', customerDropdown.textContent);
            sessionStorage.setItem('selectedDatabase', dbName);
        });
    });
    
    // Function to filter databases based on customer code
    function filterDatabases(customerCode) {
        const allDatabases = document.querySelectorAll('.database-select-btn');
        
        allDatabases.forEach(db => {
            const dbCusCode = db.getAttribute('data-cus-code');
            if (dbCusCode === customerCode) {
                db.closest('li').style.display = 'block';
            }
        });
        
        // Reset database dropdown text
        databaseDropdown.textContent = 'Select Database';
    }
    
    // Restore selections from session storage
    const savedCustomer = sessionStorage.getItem('selectedCustomer');
    const savedDatabase = sessionStorage.getItem('selectedDatabase');
    
    if (savedCustomer) {
        customerDropdown.textContent = savedCustomer;
        dbDropdownContainer.style.display = 'block';
    }
    
    if (savedDatabase) {
        databaseDropdown.textContent = savedDatabase;
    }
});