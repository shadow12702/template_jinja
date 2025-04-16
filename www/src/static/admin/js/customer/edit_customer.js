document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.getElementById('editCustomerForm');
    
    form.addEventListener('submit', function(event) {
        let valid = true;
        
        // Required fields validation
        const nameInput = document.querySelector('input[name="name"]');
        if (!nameInput.value.trim()) {
            valid = false;
            nameInput.classList.add('is-invalid');
            
            // Create error message if it doesn't exist
            let errorMsg = nameInput.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                errorMsg.textContent = 'Customer name is required';
                nameInput.parentNode.appendChild(errorMsg);
            }
        } else {
            nameInput.classList.remove('is-invalid');
        }
        
        // Email validation (if provided)
        const emailInput = document.querySelector('input[name="email"]');
        if (emailInput.value.trim() && !isValidEmail(emailInput.value.trim())) {
            valid = false;
            emailInput.classList.add('is-invalid');
            
            // Create error message
            let errorMsg = emailInput.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                errorMsg.textContent = 'Please enter a valid email address';
                emailInput.parentNode.appendChild(errorMsg);
            }
        } else {
            emailInput.classList.remove('is-invalid');
        }
        
        if (!valid) {
            event.preventDefault();
        }
    });
    
    // Email validation helper
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
    
    // Delete customer button
    const deleteBtn = document.getElementById('deleteCustomerBtn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
            deleteModal.show();
        });
    }
    
    // Initialize any tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
});