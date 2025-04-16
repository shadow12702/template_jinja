document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const form = document.getElementById('addCustomerForm');
    
    form.addEventListener('submit', function(event) {
        let valid = true;
        
        // Required fields
        const requiredFields = ['customer_code', 'customer_name'];
        requiredFields.forEach(field => {
            const input = document.getElementById(field);
            if (!input.value.trim()) {
                valid = false;
                input.classList.add('is-invalid');
                
                // Create error message if it doesn't exist
                let errorMsg = input.nextElementSibling;
                if (!errorMsg || !errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'invalid-feedback';
                    errorMsg.textContent = 'This field is required';
                    input.parentNode.appendChild(errorMsg);
                }
            } else {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
                
                // Remove error message if it exists
                const errorMsg = input.nextElementSibling;
                if (errorMsg && errorMsg.classList.contains('invalid-feedback')) {
                    errorMsg.remove();
                }
            }
        });
        
        // Email validation (if provided)
        const emailInput = document.getElementById('customer_email');
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
        } else if (emailInput.value.trim()) {
            emailInput.classList.remove('is-invalid');
            emailInput.classList.add('is-valid');
        }
        
        if (!valid) {
            event.preventDefault();
        }
    });
    
    // Email validation helper function
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
    
    // Clear validation styling when input changes
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid');
            this.classList.remove('is-valid');
            
            // Remove error message if it exists
            const errorMsg = this.nextElementSibling;
            if (errorMsg && errorMsg.classList.contains('invalid-feedback')) {
                errorMsg.remove();
            }
        });
    });
});