document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Initialize tab switching
    initTabs();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize table actions
    initTableActions();
    
    // Initialize modal form
    initModalForm();
    
    // Initialize role dropdown in filter section
    initRoleDropdown();
});

// Tab switching functionality
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Get the filter value from the tab text
            const status = this.textContent.trim().split(' ')[0].toLowerCase();
            
            // Filter the table rows
            filterTableByStatus(status);
        });
    });
}

// Filter table rows by status
function filterTableByStatus(status) {
    const rows = document.querySelectorAll('.user-table tbody tr');
    
    if (status === 'all') {
        // Show all rows
        rows.forEach(row => row.style.display = '');
        return;
    }
    
    rows.forEach(row => {
        const statusCell = row.querySelector('.status-badge');
        if (statusCell) {
            const rowStatus = statusCell.textContent.trim().toLowerCase();
            row.style.display = rowStatus === status ? '' : 'none';
        }
    });
}

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.user-table tbody tr');
            
            rows.forEach(row => {
                const name = row.querySelector('.user-name')?.textContent.toLowerCase() || '';
                const email = row.querySelector('.user-email')?.textContent.toLowerCase() || '';
                const phone = row.querySelector('td:nth-child(3)')?.textContent.toLowerCase() || '';
                const company = row.querySelector('td:nth-child(4)')?.textContent.toLowerCase() || '';
                const role = row.querySelector('td:nth-child(5)')?.textContent.toLowerCase() || '';
                
                const matches = name.includes(searchTerm) || 
                               email.includes(searchTerm) || 
                               phone.includes(searchTerm) || 
                               company.includes(searchTerm) || 
                               role.includes(searchTerm);
                
                row.style.display = matches ? '' : 'none';
            });
        });
    }
}

// Table actions
function initTableActions() {
    // Select all checkbox
    const selectAllCheckbox = document.querySelector('.select-all');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.user-table tbody input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            
            // Update any UI dependent on selection (e.g., bulk action buttons)
            updateSelectionDependentUI();
        });
    }
    
    // Individual checkboxes
    const rowCheckboxes = document.querySelectorAll('.user-table tbody input[type="checkbox"]');
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectionDependentUI();
            
            // Update "select all" checkbox state
            updateSelectAllCheckboxState();
        });
    });
    
    // Edit buttons
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const userName = row.querySelector('.user-name').textContent;
            const userEmail = row.querySelector('.user-email').textContent;
            const phone = row.querySelector('td:nth-child(3)').textContent;
            const company = row.querySelector('td:nth-child(4)').textContent;
            const role = row.querySelector('td:nth-child(5)').textContent;
            const status = row.querySelector('.status-badge').textContent.trim();
            
            // Populate the edit modal with user data
            populateEditModal({
                name: userName,
                email: userEmail,
                phone: phone,
                company: company,
                role: role,
                status: status
            });
            
            // Show the modal (using Bootstrap's modal API if available)
            const editModal = document.getElementById('editAccountModal');
            if (editModal && typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                const modal = new bootstrap.Modal(editModal);
                modal.show();
            } else {
                // Fallback if Bootstrap is not available
                editModal.style.display = 'block';
            }
        });
    });
    
    // Options buttons (three dots)
    const optionsButtons = document.querySelectorAll('.options-btn');
    optionsButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Create and show dropdown menu
            showOptionsDropdown(this);
        });
    });
}

// Update UI elements that depend on selected rows
function updateSelectionDependentUI() {
    const selectedCount = document.querySelectorAll('.user-table tbody input[type="checkbox"]:checked').length;
    
    // Example: Enable/disable bulk action buttons
    const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
    bulkActionButtons.forEach(button => {
        button.disabled = selectedCount === 0;
    });
    
    // Example: Update selected count indicator
    const selectedCountElement = document.querySelector('.selected-count');
    if (selectedCountElement) {
        selectedCountElement.textContent = selectedCount;
        selectedCountElement.style.display = selectedCount > 0 ? 'inline-block' : 'none';
    }
}

// Update "select all" checkbox state based on individual checkboxes
function updateSelectAllCheckboxState() {
    const selectAllCheckbox = document.querySelector('.select-all');
    const rowCheckboxes = document.querySelectorAll('.user-table tbody input[type="checkbox"]');
    
    if (selectAllCheckbox && rowCheckboxes.length > 0) {
        const allChecked = Array.from(rowCheckboxes).every(checkbox => checkbox.checked);
        const someChecked = Array.from(rowCheckboxes).some(checkbox => checkbox.checked);
        
        selectAllCheckbox.checked = allChecked;
        selectAllCheckbox.indeterminate = !allChecked && someChecked;
    }
}

// Show options dropdown menu
function showOptionsDropdown(button) {
    // Remove any existing dropdowns
    const existingDropdown = document.querySelector('.options-dropdown');
    if (existingDropdown) {
        existingDropdown.remove();
    }
    
    // Create dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'options-dropdown dropdown-menu';
    dropdown.style.position = 'absolute';
    dropdown.style.zIndex = '1000';
    dropdown.style.minWidth = '150px';
    
    // Add dropdown items
    dropdown.innerHTML = `
        <a class="dropdown-item" href="#" data-action="view">
            <i class="fas fa-eye me-2"></i> View Details
        </a>
        <a class="dropdown-item" href="#" data-action="edit">
            <i class="fas fa-pen me-2"></i> Edit
        </a>
        <div class="dropdown-divider"></div>
        <a class="dropdown-item text-danger" href="#" data-action="delete">
            <i class="fas fa-trash-alt me-2"></i> Delete
        </a>
    `;
    
    // Position dropdown
    const rect = button.getBoundingClientRect();
    dropdown.style.top = (rect.bottom + window.scrollY) + 'px';
    dropdown.style.left = (rect.left + window.scrollX - 100) + 'px'; // Align to right
    
    // Add to document
    document.body.appendChild(dropdown);
    
    // Add click event listeners
    dropdown.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const action = this.dataset.action;
            const row = button.closest('tr');
            
            handleOptionAction(action, row);
            
            // Close dropdown
            dropdown.remove();
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function closeDropdown(e) {
        if (!dropdown.contains(e.target) && e.target !== button) {
            dropdown.remove();
            document.removeEventListener('click', closeDropdown);
        }
    });
    
    // Show dropdown with animation
    setTimeout(() => {
        dropdown.classList.add('show');
    }, 10);
}

// Handle option action (view, edit, delete)
function handleOptionAction(action, row) {
    const userName = row.querySelector('.user-name').textContent;
    
    switch (action) {
        case 'view':
            showToast(`Viewing details for ${userName}`, 'info');
            // Implement view details functionality
            break;
        
        case 'edit':
            // Trigger click on the edit button
            row.querySelector('.edit-btn').click();
            break;
        
        case 'delete':
            if (confirm(`Are you sure you want to delete the account for ${userName}?`)) {
                // Animate row deletion
                row.style.backgroundColor = '#ffebee';
                setTimeout(() => {
                    row.style.transition = 'opacity 0.5s, transform 0.5s';
                    row.style.opacity = '0';
                    row.style.transform = 'translateX(20px)';
                    
                    setTimeout(() => {
                        row.remove();
                        showToast(`${userName}'s account has been deleted`, 'success');
                        
                        // Update counts
                        updateTabCounts();
                    }, 500);
                }, 300);
            }
            break;
    }
}

// Initialize modal form
function initModalForm() {
    // Add account form
    const addAccountForm = document.getElementById('addAccountForm');
    if (addAccountForm) {
        addAccountForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state on submit button
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
            
            // Get form data
            const formData = new FormData(this);
            const accountData = {
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                company: formData.get('company'),
                role: formData.get('role'),
                status: formData.get('status')
            };
            
            // Simulate API call
            setTimeout(() => {
                // Add new row to table
                addNewAccountRow(accountData);
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                
                // Hide modal (using Bootstrap's modal API if available)
                const modal = document.getElementById('addAccountModal');
                if (modal && typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    bsModal.hide();
                } else {
                    // Fallback
                    modal.style.display = 'none';
                }
                
                // Reset form
                addAccountForm.reset();
                
                // Show toast notification
                showToast(`New account for ${accountData.name} has been created`, 'success');
                
                // Update tab counts
                updateTabCounts();
            }, 1000);
        });
    }
    
    // Edit account form (if exists)
    const editAccountForm = document.getElementById('editAccountForm');
    if (editAccountForm) {
        editAccountForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Updating...';
            
            // Get form data
            const formData = new FormData(this);
            const accountData = {
                id: formData.get('id'),
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                company: formData.get('company'),
                role: formData.get('role'),
                status: formData.get('status')
            };
            
            // Simulate API call
            setTimeout(() => {
                // Update the row in the table
                updateAccountRow(accountData);
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                
                // Hide modal
                const modal = document.getElementById('editAccountModal');
                if (modal && typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    bsModal.hide();
                } else {
                    // Fallback
                    modal.style.display = 'none';
                }
                
                // Show toast notification
                showToast(`${accountData.name}'s account has been updated`, 'success');
                
                // Update tab counts if status changed
                updateTabCounts();
            }, 1000);
        });
    }
}

// Initialize role dropdown in filter section
function initRoleDropdown() {
    const roleDropdown = document.querySelector('.dropdown-btn');
    if (roleDropdown) {
        roleDropdown.addEventListener('click', function() {
            const dropdownMenu = this.nextElementSibling;
            if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                dropdownMenu.classList.toggle('show');
                
                // Add click event to document to close dropdown when clicking outside
                document.addEventListener('click', function closeDropdown(e) {
                    if (!dropdownMenu.contains(e.target) && e.target !== roleDropdown) {
                        dropdownMenu.classList.remove('show');
                        document.removeEventListener('click', closeDropdown);
                    }
                });
            }
        });
    }
}

// Populate edit modal with user data
function populateEditModal(userData) {
    const editForm = document.getElementById('editAccountForm');
    if (!editForm) return;
    
    // Set form field values
    const nameInput = editForm.querySelector('input[name="name"]');
    const emailInput = editForm.querySelector('input[name="email"]');
    const phoneInput = editForm.querySelector('input[name="phone"]');
    const companyInput = editForm.querySelector('input[name="company"]');
    const roleSelect = editForm.querySelector('select[name="role"]');
    const statusSelect = editForm.querySelector('select[name="status"]');
    
    if (nameInput) nameInput.value = userData.name;
    if (emailInput) emailInput.value = userData.email;
    if (phoneInput) phoneInput.value = userData.phone;
    if (companyInput) companyInput.value = userData.company;
    if (roleSelect) {
        const roleOption = Array.from(roleSelect.options).find(option => option.text === userData.role);
        if (roleOption) roleOption.selected = true;
    }
    if (statusSelect) {
        const statusOption = Array.from(statusSelect.options).find(option => option.text === userData.status);
        if (statusOption) statusOption.selected = true;
    }
    
    // Update modal title to include user name
    const modalTitle = document.querySelector('#editAccountModal .modal-title');
    if (modalTitle) {
        modalTitle.textContent = `Edit Account: ${userData.name}`;
    }
}

// Add new account row to table
function addNewAccountRow(userData) {
    const tbody = document.querySelector('.user-table tbody');
    if (!tbody) return;
    
    // Create new row
    const newRow = document.createElement('tr');
    
    // Get status class
    let statusClass = '';
    switch (userData.status) {
        case 'Active':
            statusClass = 'success';
            break;
        case 'Pending':
            statusClass = 'warning';
            break;
        case 'Banned':
            statusClass = 'danger';
            break;
        default:
            statusClass = 'secondary';
    }
    
    // Get first letter for avatar
    const firstLetter = userData.name.charAt(0).toUpperCase();
    
    // Set row HTML
    newRow.innerHTML = `
        <td><input type="checkbox"></td>
        <td class="user-info">
            <div class="avatar">${firstLetter}</div>
            <div class="user-details">
                <div class="user-name">${userData.name}</div>
                <div class="user-email">${userData.email}</div>
            </div>
        </td>
        <td>${userData.phone}</td>
        <td>${userData.company}</td>
        <td>${userData.role}</td>
        <td>
            <span class="status-badge ${statusClass}">${userData.status}</span>
        </td>
    <td class="actions">
            <button class="edit-btn" data-bs-toggle="tooltip" title="Edit"><i class="fas fa-pen"></i></button>
            <button class="options-btn" data-bs-toggle="tooltip" title="More Options"><i class="fas fa-ellipsis-v"></i></button>
        </td>
    `;
    
    // Set initial style for animation
    newRow.style.opacity = '0';
    newRow.style.transform = 'translateY(-20px)';
    
    // Add to table (at the beginning)
    tbody.insertBefore(newRow, tbody.firstChild);
    
    // Animate in
    setTimeout(() => {
        newRow.style.transition = 'opacity 0.5s, transform 0.5s';
        newRow.style.opacity = '1';
        newRow.style.transform = 'translateY(0)';
    }, 10);
    
    // Add event listeners to the new row
    const checkbox = newRow.querySelector('input[type="checkbox"]');
    if (checkbox) {
        checkbox.addEventListener('change', function() {
            updateSelectionDependentUI();
            updateSelectAllCheckboxState();
        });
    }
    
    const editBtn = newRow.querySelector('.edit-btn');
    if (editBtn) {
        editBtn.addEventListener('click', function() {
            populateEditModal(userData);
            
            // Show modal
            const editModal = document.getElementById('editAccountModal');
            if (editModal && typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                const modal = new bootstrap.Modal(editModal);
                modal.show();
            } else {
                editModal.style.display = 'block';
            }
        });
    }
    
    const optionsBtn = newRow.querySelector('.options-btn');
    if (optionsBtn) {
        optionsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            showOptionsDropdown(this);
        });
    }
    
    // Initialize tooltips on new buttons
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltips = newRow.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(el => {
            new bootstrap.Tooltip(el);
        });
    }
}

// Update existing account row
function updateAccountRow(userData) {
    // Find the row to update (could use id or other identifier)
    // For demo, just update first row that matches the name
    const rows = document.querySelectorAll('.user-table tbody tr');
    let targetRow = null;
    
    for (const row of rows) {
        const nameElement = row.querySelector('.user-name');
        if (nameElement && nameElement.textContent === userData.name) {
            targetRow = row;
            break;
        }
    }
    
    if (!targetRow) return;
    
    // Update row data
    const emailElement = targetRow.querySelector('.user-email');
    const phoneElement = targetRow.querySelector('td:nth-child(3)');
    const companyElement = targetRow.querySelector('td:nth-child(4)');
    const roleElement = targetRow.querySelector('td:nth-child(5)');
    const statusElement = targetRow.querySelector('.status-badge');
    
    if (emailElement) emailElement.textContent = userData.email;
    if (phoneElement) phoneElement.textContent = userData.phone;
    if (companyElement) companyElement.textContent = userData.company;
    if (roleElement) roleElement.textContent = userData.role;
    
    if (statusElement) {
        // Update status text
        statusElement.textContent = userData.status;
        
        // Update status class
        statusElement.classList.remove('success', 'warning', 'danger', 'secondary');
        
        switch (userData.status) {
            case 'Active':
                statusElement.classList.add('success');
                break;
            case 'Pending':
                statusElement.classList.add('warning');
                break;
            case 'Banned':
                statusElement.classList.add('danger');
                break;
            default:
                statusElement.classList.add('secondary');
        }
    }
    
    // Highlight the updated row
    targetRow.style.transition = 'background-color 1s';
    targetRow.style.backgroundColor = '#e7f5e7';
    
    setTimeout(() => {
        targetRow.style.backgroundColor = '';
    }, 2000);
}

// Update tab counts
function updateTabCounts() {
    const rows = document.querySelectorAll('.user-table tbody tr');
    
    // Count by status
    const counts = {
        all: rows.length,
        active: 0,
        pending: 0,
        banned: 0,
        rejected: 0
    };
    
    rows.forEach(row => {
        const statusElement = row.querySelector('.status-badge');
        if (statusElement) {
            const status = statusElement.textContent.trim().toLowerCase();
            if (counts.hasOwnProperty(status)) {
                counts[status]++;
            }
        }
    });
    
    // Update tab badges
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        const badgeElement = tab.querySelector('.badge');
        if (badgeElement) {
            const status = tab.textContent.trim().split(' ')[0].toLowerCase();
            if (counts.hasOwnProperty(status)) {
                badgeElement.textContent = counts[status];
            }
        }
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Get icon based on type
    let icon = 'info-circle';
    switch (type) {
        case 'success':
            icon = 'check-circle';
            break;
        case 'error':
            icon = 'exclamation-circle';
            break;
        case 'warning':
            icon = 'exclamation-triangle';
            break;
    }
    
    // Create toast
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-${icon} toast-icon ${type}"></i>
            <strong class="toast-title">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
            <button type="button" class="toast-close">&times;</button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Add close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', function() {
        toast.style.animation = 'slideOut 0.3s forwards';
        setTimeout(() => {
            if (toastContainer.contains(toast)) {
                toastContainer.removeChild(toast);
            }
        }, 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toastContainer.contains(toast)) {
            toast.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => {
                if (toastContainer.contains(toast)) {
                    toastContainer.removeChild(toast);
                }
            }, 300);
        }
    }, 5000);
}