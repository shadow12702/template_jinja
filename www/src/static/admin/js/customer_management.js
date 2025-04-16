document.addEventListener('DOMContentLoaded', function() {
    // Form submission for adding a new customer
    const addCustomerForm = document.getElementById('addCustomerForm');
    
    if (addCustomerForm) {
        addCustomerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(addCustomerForm);
            const customerData = {};
            
            formData.forEach((value, key) => {
                customerData[key] = value;
            });

            // Send data to server via AJAX
            fetch('/add-customer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(customerData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Close modal
                $('#addCustomerModal').modal('hide');
                
                // Optionally, refresh the table or add the new row
                console.log('Customer added successfully:', data);
                
                // Reset form
                addCustomerForm.reset();
                
                // Optionally show a success message
                alert('Customer added successfully!');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add customer. Please try again.');
            });
        });
    }

    // Existing customer management JavaScript
    const searchInput = document.querySelector('.search-box input');
    const tabs = document.querySelectorAll('.tab');
    const selectAllCheckbox = document.querySelector('.select-all');
    const rowCheckboxes = document.querySelectorAll('tbody input[type="checkbox"]');
    const industryDropdown = document.querySelector('.dropdown-btn');
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
            filterCustomers(status);
        });
    });

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        filterCustomers(null, searchTerm);
    });

    // Select all checkboxes
    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });

    // Industry dropdown (placeholder - you might want to implement actual filtering)
    industryDropdown.addEventListener('click', function() {
        // Toggle dropdown or implement industry filtering
        console.log('Industry dropdown clicked');
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
    function filterCustomers(status = null, searchTerm = '') {
        const rows = document.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const nameCell = row.querySelector('.user-name');
            const companyCell = row.querySelector('td:nth-child(3)');
            const statusCell = row.querySelector('.status-badge');
            
            const nameMatch = nameCell.textContent.toLowerCase().includes(searchTerm);
            const companyMatch = companyCell.textContent.toLowerCase().includes(searchTerm);
            const statusMatch = !status || statusCell.textContent.toLowerCase() === status;

            row.style.display = (nameMatch || companyMatch) && statusMatch ? '' : 'none';
        });
    }
});