document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initTooltips();
    
    // Set up table functionality
    initTableFunctionality();
    
    // Set up delete confirmations
    setupDeleteButtons();
    
    // Initialize search functionality
    setupSearch();
    
    // Demo data for adding customers if needed
    const demoCustomers = [
        { code: 'CUS001', name: 'Acme Corporation', status: 'active' },
        { code: 'CUS002', name: 'Global Industries', status: 'inactive' },
        { code: 'CUS003', name: 'Tech Solutions', status: 'pending' }
    ];
    
    // Add customer button
    const addCustomerBtn = document.querySelector('.add-new-btn');
    if (addCustomerBtn) {
        addCustomerBtn.addEventListener('click', function() {
            window.location.href = '/add_new_customer';
        });
    }
    
    // Demo add button (for development)
    const demoAddBtn = document.getElementById('demo-add-btn');
    if (demoAddBtn) {
        demoAddBtn.addEventListener('click', function() {
            addDemoCustomer(demoCustomers);
        });
    }
});

// Initialize Bootstrap tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Set up table sorting and pagination
function initTableFunctionality() {
    const table = document.querySelector('.customer-table');
    if (!table) return;
    
    // Make headers sortable
    const headers = table.querySelectorAll('th[data-sortable="true"]');
    headers.forEach(header => {
        header.addEventListener('click', function() {
            const column = this.dataset.column;
            const currentSort = this.dataset.sort || 'none';
            
            // Reset all header sort states
            headers.forEach(h => {
                h.dataset.sort = 'none';
                h.querySelector('.sort-icon')?.remove();
            });
            
            // Set new sort state
            let newSort = 'asc';
            if (currentSort === 'asc') newSort = 'desc';
            this.dataset.sort = newSort;
            
            // Add sort icon
            const sortIcon = document.createElement('i');
            sortIcon.className = `fas fa-sort-${newSort === 'asc' ? 'up' : 'down'} sort-icon ml-1`;
            this.appendChild(sortIcon);
            
            // Sort the table
            sortTable(table, column, newSort);
        });
    });
}

// Sort table function
function sortTable(table, column, direction) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aCol = a.querySelector(`[data-column="${column}"]`).textContent.trim();
        const bCol = b.querySelector(`[data-column="${column}"]`).textContent.trim();
        
        // Try numeric sort first
        const aNum = parseFloat(aCol);
        const bNum = parseFloat(bCol);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return direction === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // Fallback to string sort
        return direction === 'asc' ? 
            aCol.localeCompare(bCol) : 
            bCol.localeCompare(aCol);
    });
    
    // Remove existing rows
    rows.forEach(row => row.remove());
    
    // Add sorted rows
    sortedRows.forEach(row => tbody.appendChild(row));
}

// Setup delete confirmations
function setupDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const row = this.closest('tr');
            const customerName = row.querySelector('.customer-name').textContent;
            const customerCode = row.querySelector('.customer-code').textContent;
            
            if (confirm(`Are you sure you want to delete customer "${customerName}" (${customerCode})?`)) {
                // Show loading state
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                this.disabled = true;
                
                // Simulate API call with timeout
                setTimeout(() => {
                    // Remove row with animation
                    row.style.backgroundColor = "#ffebee";
                    setTimeout(() => {
                        row.style.transition = "opacity 0.5s, transform 0.5s";
                        row.style.opacity = "0";
                        row.style.transform = "translateX(20px)";
                        
                        setTimeout(() => {
                            row.remove();
                            showToast(`Customer "${customerName}" was successfully deleted.`, 'success');
                        }, 500);
                    }, 300);
                }, 800);
            }
        });
    });
}

// Setup search functionality
function setupSearch() {
    const searchInput = document.querySelector('.search-container input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('.customer-table tbody tr');
        
        rows.forEach(row => {
            const customerName = row.querySelector('.customer-name').textContent.toLowerCase();
            const customerCode = row.querySelector('.customer-code').textContent.toLowerCase();
            
            if (customerName.includes(searchTerm) || customerCode.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    toast.innerHTML = `
        <div class="toast-content">
            ${message}
        </div>
        <button class="toast-close">&times;</button>
    `;
    
    // Add close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.style.animation = 'slideOut 0.3s forwards';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    });
    
    // Add to container
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (container.contains(toast)) {
            toast.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => {
                if (container.contains(toast)) {
                    container.removeChild(toast);
                }
            }, 300);
        }
    }, 5000);
}

// Demo function to add a random customer
function addDemoCustomer(customers) {
    if (!customers || !customers.length) return;
    
    // Get random customer
    const customer = customers[Math.floor(Math.random() * customers.length)];
    
    // Create new row
    const tbody = document.querySelector('.customer-table tbody');
    if (!tbody) return;
    
    const newRow = document.createElement('tr');
    
    // Add class for animation
    newRow.style.opacity = '0';
    newRow.style.transform = 'translateY(-20px)';
    
    // Get the first letter of the customer name
    const firstLetter = customer.name.charAt(0);
    
    // Create row content
    newRow.innerHTML = `
        <td><input type="checkbox"></td>
        <td>${customer.code}</td>
        <td class="customer-info">
            <div class="customer-avatar">${firstLetter}</div>
            <div class="customer-details">
                <div class="customer-name">${customer.name}</div>
                <div class="customer-code">${customer.code}</div>
            </div>
        </td>
        <td>
            <span class="status-indicator status-${customer.status}"></span>
            ${customer.status.charAt(0).toUpperCase() + customer.status.slice(1)}
        </td>
        <td class="action-buttons">
            <button class="btn-icon btn-view" data-bs-toggle="tooltip" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button class="btn-icon btn-edit" data-bs-toggle="tooltip" title="Edit Customer">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon btn-delete" data-bs-toggle="tooltip" title="Delete Customer">
                <i class="fas fa-trash-alt"></i>
            </button>
        </td>
    `;
    
    // Add to table
    tbody.insertBefore(newRow, tbody.firstChild);
    
    // Animate in
    setTimeout(() => {
        newRow.style.transition = 'opacity 0.5s, transform 0.5s';
        newRow.style.opacity = '1';
        newRow.style.transform = 'translateY(0)';
    }, 50);
    
    // Show notification
    showToast(`New customer "${customer.name}" added successfully!`, 'success');
    
    // Initialize tooltips on new buttons
    initTooltips();
    
    // Add delete functionality to new delete button
    const deleteBtn = newRow.querySelector('.btn-delete');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm(`Are you sure you want to delete customer "${customer.name}" (${customer.code})?`)) {
                // Show loading state
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                this.disabled = true;
                
                // Simulate API call with timeout
                setTimeout(() => {
                    // Remove row with animation
                    newRow.style.backgroundColor = "#ffebee";
                    setTimeout(() => {
                        newRow.style.opacity = "0";
                        newRow.style.transform = "translateX(20px)";
                        
                        setTimeout(() => {
                            newRow.remove();
                            showToast(`Customer "${customer.name}" was successfully deleted.`, 'success');
                        }, 500);
                    }, 300);
                }, 800);
            }
        });
    }
}
$(document).ready(function() {
    // Xử lý khi nút Delete được nhấn
    $('.btn-delete').click(function() {
        const customerCode = $(this).data('customer-code');
        const customerName = $(this).data('customer-name');

        // Cập nhật thông tin trong modal
        $('#customer-name').text(customerName);
        $('#deleteCustomerForm').attr('action', `/delete_customer/${customerCode}`);

        // Mở modal
        $('#deleteConfirmModal').modal('show');
    });
});
