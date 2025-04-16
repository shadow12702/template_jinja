document.addEventListener('DOMContentLoaded', function() {
    // Form submission for adding a new account
    const addAccountForm = document.getElementById('addAccountForm');
    
    if (addAccountForm) {
        addAccountForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(addAccountForm);
            const accountData = {};
            
            formData.forEach((value, key) => {
                accountData[key] = value;
            });

            // Send data to server via AJAX
            fetch('/add-account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(accountData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Close modal
                $('#addAccountModal').modal('hide');
                
                // Optionally, refresh the table or add the new row
                console.log('Account added successfully:', data);
                
                // Reset form
                addAccountForm.reset();
                
                // Optionally show a success message
                alert('Account added successfully!');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add account. Please try again.');
            });
        });
    }

    // Existing account management JavaScript from previous implementation
    const searchInput = document.querySelector('.search-box input');
    const tabs = document.querySelectorAll('.tab');
    const selectAllCheckbox = document.querySelector('.select-all');
    const rowCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]');
    const roleDropdown = document.querySelector('.dropdown-btn');
    const pageSelect = document.querySelector('select');
    const prevBtn = document.querySelector('.page-btn:first-child');
    const nextBtn = document.querySelector('.page-btn:last-child');

    // Tabs filtering
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            // Get the status from the tab
            const status = this.textContent.split(' ')[0].toLowerCase();
            filterUsers(status);
        });
    });

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterUsers(null, searchTerm);
    });

    // Select all checkboxes
    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });

    // Role dropdown (placeholder - you might want to implement actual filtering)
    roleDropdown.addEventListener('click', function() {
        // Toggle dropdown or implement role filtering
        console.log('Role dropdown clicked');
    });

    // Page size selection
    pageSelect.addEventListener('change', function() {
        const selectedPageSize = this.value;
        // Implement page size change logic
        console.log(`Page size changed to ${selectedPageSize}`);
    });

    // Pagination buttons
    prevBtn.addEventListener('click', function() {
        // Implement previous page logic
        console.log('Previous page');
    });

    nextBtn.addEventListener('click', function() {
        // Implement next page logic
        console.log('Next page');
    });

    // Filtering function
    function filterUsers(status = null, searchTerm = '') {
        const rows = document.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const nameCell = row.querySelector('.user-name');
            const emailCell = row.querySelector('.user-email');
            const statusCell = row.querySelector('.status-badge');
            
            const nameMatch = nameCell.textContent.toLowerCase().includes(searchTerm);
            const emailMatch = emailCell.textContent.toLowerCase().includes(searchTerm);
            const statusMatch = !status || statusCell.textContent.toLowerCase() === status;

            row.style.display = (nameMatch || emailMatch) && statusMatch ? '' : 'none';
        });
    }
});