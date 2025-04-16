document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Initialize table functionality
    initTableFunctionality();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize dropdown filters
    initDropdowns();
});

// Initialize table functionality
function initTableFunctionality() {
    // Make rows expandable for details
    const tableRows = document.querySelectorAll('.db-table tbody tr');
    tableRows.forEach(row => {
        // Add click event to expand/collapse detail
        row.addEventListener('click', function(e) {
            // Ignore click on checkbox or buttons
            if (e.target.closest('input[type="checkbox"]') || 
                e.target.closest('button')) {
                return;
            }
            
            // Toggle expanded state
            this.classList.toggle('expanded');
            
            // Get the data attributes for expansion
            const cdbDbid = this.dataset.cdbDbid;
            const pdbDbid = this.dataset.pdbDbid || '';
            const dbName = this.dataset.dbName;
            const pdbName = this.dataset.pdbName || 'N/A';
            
            // Check if detail row already exists
            let detailRow = this.nextElementSibling;
            if (detailRow && detailRow.classList.contains('detail-row')) {
                // Toggle visibility
                detailRow.style.display = detailRow.style.display === 'none' ? 'table-row' : 'none';
            } else {
                // Create new detail row
                detailRow = document.createElement('tr');
                detailRow.className = 'detail-row';
                detailRow.innerHTML = `
                    <td colspan="${this.children.length}">
                        <div class="detail-content">
                            <h5>Database Details: ${dbName}${pdbName !== 'N/A' ? ' / ' + pdbName : ''}</h5>
                            <div class="detail-grid">
                                <div class="detail-item">
                                    <span class="detail-label">CDB DBID</span>
                                    <span class="detail-value">${cdbDbid}</span>
                                </div>
                                ${pdbDbid ? `
                                <div class="detail-item">
                                    <span class="detail-label">PDB DBID</span>
                                    <span class="detail-value">${pdbDbid}</span>
                                </div>` : ''}
                                <div class="detail-item">
                                    <span class="detail-label">Snapshot Range</span>
                                    <span class="detail-value">${this.dataset.minSnap} - ${this.dataset.lastSnap}</span>
                                </div>
                                <div class="detail-item">
                                    <span class="detail-label">Time Range</span>
                                    <span class="detail-value">${this.dataset.minTime} - ${this.dataset.maxTime}</span>
                                </div>
                            </div>
                            <div class="actions mt-3">
                                <button class="btn btn-primary btn-sm view-report-btn" data-cdb-dbid="${cdbDbid}" data-pdb-dbid="${pdbDbid}">
                                    <i class="fas fa-chart-line me-1"></i> View Performance Report
                                </button>
                                <button class="btn btn-outline-secondary btn-sm ms-2">
                                    <i class="fas fa-download me-1"></i> Download AWR
                                </button>
                            </div>
                        </div>
                    </td>
                `;
                
                // Insert after current row
                this.parentNode.insertBefore(detailRow, this.nextSibling);
                
                // Add event listener to the "View Performance Report" button
                const viewReportBtn = detailRow.querySelector('.view-report-btn');
                if (viewReportBtn) {
                    viewReportBtn.addEventListener('click', function(e) {
                        e.stopPropagation();
                        
                        // Show performance metrics section
                        showPerformanceMetrics(cdbDbid, pdbDbid, dbName, pdbName);
                    });
                }
            }
        });
        
        // Add hover effect
        row.style.cursor = 'pointer';
    });
    
    // Make headers sortable
    const headers = document.querySelectorAll('.db-table th[data-sortable="true"]');
    headers.forEach(header => {
        header.addEventListener('click', function(e) {
            e.stopPropagation();
            
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
            sortIcon.className = `fas fa-sort-${newSort === 'asc' ? 'up' : 'down'} sort-icon ms-1`;
            this.appendChild(sortIcon);
            
            // Sort the table
            sortTable(column, newSort);
        });
        
        // Add sortable cursor and hint
        header.style.cursor = 'pointer';
        header.setAttribute('title', 'Click to sort');
    });
    
    // Select all checkbox
    const selectAllCheckbox = document.querySelector('.select-all');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.db-table tbody input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
                
                // Update row selected state
                const row = checkbox.closest('tr');
                if (row) {
                    if (this.checked) {
                        row.classList.add('selected');
                    } else {
                        row.classList.remove('selected');
                    }
                }
            });
            
            // Update any UI dependent on selection
            updateSelectionDependentUI();
        });
    }
    
    // Individual row checkboxes
    const rowCheckboxes = document.querySelectorAll('.db-table tbody input[type="checkbox"]');
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function(e) {
            e.stopPropagation();
            
            // Update row selected state
            const row = this.closest('tr');
            if (row) {
                if (this.checked) {
                    row.classList.add('selected');
                } else {
                    row.classList.remove('selected');
                }
            }
            
            // Update selection dependent UI
            updateSelectionDependentUI();
            
            // Update "select all" checkbox state
            updateSelectAllCheckboxState();
        });
    });
}

// Update UI elements that depend on selected rows
function updateSelectionDependentUI() {
    const selectedCount = document.querySelectorAll('.db-table tbody input[type="checkbox"]:checked').length;
    
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
    const rowCheckboxes = document.querySelectorAll('.db-table tbody input[type="checkbox"]');
    
    if (selectAllCheckbox && rowCheckboxes.length > 0) {
        const allChecked = Array.from(rowCheckboxes).every(checkbox => checkbox.checked);
        const someChecked = Array.from(rowCheckboxes).some(checkbox => checkbox.checked);
        
        selectAllCheckbox.checked = allChecked;
        selectAllCheckbox.indeterminate = !allChecked && someChecked;
    }
}

// Sort table function
function sortTable(column, direction) {
    const tbody = document.querySelector('.db-table tbody');
    const rows = Array.from(tbody.querySelectorAll('tr:not(.detail-row)'));
    
    // Sort rows based on column and direction
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.dataset[column.toLowerCase()] || a.querySelector(`[data-column="${column}"]`)?.textContent.trim() || '';
        const bValue = b.dataset[column.toLowerCase()] || b.querySelector(`[data-column="${column}"]`)?.textContent.trim() || '';
        
        // Try numeric sort
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return direction === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // Fallback to string sort
        return direction === 'asc' ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });
    
    // Remove any detail rows
    document.querySelectorAll('.detail-row').forEach(row => row.remove());
    
    // Remove existing rows
    rows.forEach(row => tbody.removeChild(row));
    
    // Add sorted rows back
    sortedRows.forEach(row => tbody.appendChild(row));
}

// Initialize search functionality
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.db-table tbody tr:not(.detail-row)');
            
            rows.forEach(row => {
                const customerCode = row.dataset.cusCode?.toLowerCase() || '';
                const dbName = row.dataset.dbName?.toLowerCase() || '';
                const pdbName = row.dataset.pdbName?.toLowerCase() || '';
                const version = row.dataset.version?.toLowerCase() || '';
                
                // Check if any column contains the search term
                const matches = customerCode.includes(searchTerm) || 
                                dbName.includes(searchTerm) || 
                                pdbName.includes(searchTerm) || 
                                version.includes(searchTerm);
                
                // Hide/show the row
                row.style.display = matches ? '' : 'none';
                
                // Also hide any detail row
                const detailRow = row.nextElementSibling;
                if (detailRow && detailRow.classList.contains('detail-row')) {
                    detailRow.style.display = 'none';
                }
            });
        });
    }
}

// Initialize dropdown filters
function initDropdowns() {
    const dropdownButtons = document.querySelectorAll('.dropdown-btn');
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function() {
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('dropdown-menu')) {
                dropdown.classList.toggle('show');
                
                // Close when clicking outside
                document.addEventListener('click', function closeDropdown(e) {
                    if (!dropdown.contains(e.target) && e.target !== button) {
                        dropdown.classList.remove('show');
                        document.removeEventListener('click', closeDropdown);
                    }
                });
            }
        });
    });
    
    // Add functionality to dropdown items
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Get filter value and type
            const filterValue = this.dataset.value;
            const filterType = this.closest('.dropdown-menu').dataset.filter;
            
            // Apply filter to table
            filterTable(filterType, filterValue);
            
            // Update dropdown button text
            const dropdownButton = this.closest('.dropdown-menu').previousElementSibling;
            if (dropdownButton) {
                const originalText = dropdownButton.dataset.originalText || dropdownButton.textContent.split(':')[0].trim();
                dropdownButton.dataset.originalText = originalText;
                
                if (filterValue === 'all') {
                    dropdownButton.innerHTML = `${originalText} <i class="fas fa-chevron-down"></i>`;
                } else {
                    dropdownButton.innerHTML = `${originalText}: ${this.textContent} <i class="fas fa-chevron-down"></i>`;
                }
            }
            
            // Hide dropdown
            this.closest('.dropdown-menu').classList.remove('show');
        });
    });
}

// Filter table by a specific column and value
function filterTable(column, value) {
    const rows = document.querySelectorAll('.db-table tbody tr:not(.detail-row)');
    
    rows.forEach(row => {
        // If filter is 'all', show all rows
        if (value === 'all') {
            row.style.display = '';
            return;
        }
        
        // Get the value from the row's data attribute
        const rowValue = row.dataset[column.toLowerCase()] || '';
        
        // Show/hide row based on filter
        if (rowValue === value) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
            
            // Also hide any detail row
            const detailRow = row.nextElementSibling;
            if (detailRow && detailRow.classList.contains('detail-row')) {
                detailRow.style.display = 'none';
            }
        }
    });
}

// Show performance metrics section
function showPerformanceMetrics(cdbDbid, pdbDbid, dbName, pdbName) {
    // Get or create metrics container
    let metricsContainer = document.querySelector('.metrics-container');
    if (!metricsContainer) {
        metricsContainer = document.createElement('div');
        metricsContainer.className = 'metrics-container';
        
        // Add container at the end of the main content
        document.querySelector('.container').appendChild(metricsContainer);
    }
    
    // Show loading state
    metricsContainer.innerHTML = `
        <div class="d-flex justify-content-center py-5">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span class="ms-3">Loading performance metrics...</span>
        </div>
    `;
    
    // Show the container
    metricsContainer.style.display = 'block';
    
    // Scroll to metrics section
    metricsContainer.scrollIntoView({ behavior: 'smooth' });
    
    // Simulate API call to get performance metrics
    setTimeout(() => {
        // Update metrics container with content
        metricsContainer.innerHTML = `
            <div class="metrics-header">
                <h2 class="metrics-title">Performance Metrics: ${dbName}${pdbName !== 'N/A' ? ' / ' + pdbName : ''}</h2>
                <div class="metrics-controls">
                    <button class="btn btn-outline-secondary btn-sm">
                        <i class="fas fa-calendar-alt me-1"></i> Date Range
                    </button>
                    <button class="btn btn-outline-secondary btn-sm">
                        <i class="fas fa-download me-1"></i> Export
                    </button>
                    <button class="btn btn-outline-danger btn-sm close-metrics-btn">
                        <i class="fas fa-times me-1"></i> Close
                    </button>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-header">
                        <h5 class="metric-title">CPU Utilization</h5>
                        <i class="fas fa-microchip text-success"></i>
                    </div>
                    <div class="metric-value">76%</div>
                    <div class="metric-trend">
                        <span class="text-danger"><i class="fas fa-arrow-up"></i> 12%</span> since last week
                    </div>
                    <div class="metric-chart" id="cpu-chart"></div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-header">
                        <h5 class="metric-title">Memory Usage</h5>
                        <i class="fas fa-memory text-primary"></i>
                    </div>
                    <div class="metric-value">8.2 GB</div>
                    <div class="metric-trend">
                        <span class="text-success"><i class="fas fa-arrow-down"></i> 3%</span> since last week
                    </div>
                    <div class="metric-chart" id="memory-chart"></div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-header">
                        <h5 class="metric-title">Disk I/O</h5>
                        <i class="fas fa-hdd text-warning"></i>
                    </div>
                    <div class="metric-value">245 IOPS</div>
                    <div class="metric-trend">
                        <span class="text-danger"><i class="fas fa-arrow-up"></i> 8%</span> since last week
                    </div>
                    <div class="metric-chart" id="io-chart"></div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-header">
                        <h5 class="metric-title">SQL Response Time</h5>
                        <i class="fas fa-tachometer-alt text-danger"></i>
                    </div>
                    <div class="metric-value">0.8 sec</div>
                    <div class="metric-trend">
                        <span class="text-success"><i class="fas fa-arrow-down"></i> 15%</span> since last week
                    </div>
                    <div class="metric-chart" id="sql-chart"></div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">Top Consuming SQL Statements</h5>
                        </div>
                        <div class="card-body">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>SQL ID</th>
                                        <th>Executions</th>
                                        <th>CPU Time (s)</th>
                                        <th>Elapsed Time (s)</th>
                                <th>Buffer Gets</th>
                                <th>Disk Reads</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code>a1b2c3d4e5f6g7</code></td>
                                <td>3,254</td>
                                <td>420.2</td>
                                <td>865.7</td>
                                <td>1,245,632</td>
                                <td>8,542</td>
                            </tr>
                            <tr>
                                <td><code>h8i9j0k1l2m3n4</code></td>
                                <td>12,587</td>
                                <td>325.6</td>
                                <td>548.3</td>
                                <td>987,421</td>
                                <td>4,215</td>
                            </tr>
                            <tr>
                                <td><code>o5p6q7r8s9t0u1</code></td>
                                <td>865</td>
                                <td>254.8</td>
                                <td>312.5</td>
                                <td>654,789</td>
                                <td>3,698</td>
                            </tr>
                            <tr>
                                <td><code>v2w3x4y5z6a7b8</code></td>
                                <td>2,154</td>
                                <td>187.4</td>
                                <td>243.9</td>
                                <td>523,147</td>
                                <td>2,874</td>
                            </tr>
                            <tr>
                                <td><code>c9d0e1f2g3h4i5</code></td>
                                <td>5,487</td>
                                <td>145.2</td>
                                <td>186.3</td>
                                <td>412,658</td>
                                <td>1,954</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
        // Add event listener to close button
        const closeBtn = metricsContainer.querySelector('.close-metrics-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                metricsContainer.style.display = 'none';
            });
        }
        
        // Simulate chart rendering (would use a real charting library in production)
        simulateCharts();
        
        // Show toast notification
        showToast(`Performance report loaded for ${dbName}${pdbName !== 'N/A' ? ' / ' + pdbName : ''}`, 'success');
    }, 1500);
}

// Simulate chart rendering (placeholder for actual chart implementation)
function simulateCharts() {
    // In a real implementation, you would use a charting library like Chart.js, ApexCharts, or ECharts
    const chartContainers = document.querySelectorAll('.metric-chart');
    
    chartContainers.forEach(container => {
        // Create a simple canvas-based chart simulation
        const canvas = document.createElement('canvas');
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        container.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        
        // Draw a placeholder chart (line chart)
        ctx.beginPath();
        ctx.moveTo(0, canvas.height * 0.8);
        
        // Generate random points
        for (let i = 1; i <= 10; i++) {
            const x = (canvas.width / 10) * i;
            const y = canvas.height * (0.2 + Math.random() * 0.6);
            ctx.lineTo(x, y);
        }
        
        // Style and stroke the path
        ctx.strokeStyle = container.id.includes('cpu') ? '#28a745' : 
                          container.id.includes('memory') ? '#007bff' : 
                          container.id.includes('io') ? '#ffc107' : '#dc3545';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Fill area under the line
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.closePath();
        ctx.fillStyle = container.id.includes('cpu') ? 'rgba(40, 167, 69, 0.1)' : 
                        container.id.includes('memory') ? 'rgba(0, 123, 255, 0.1)' : 
                        container.id.includes('io') ? 'rgba(255, 193, 7, 0.1)' : 'rgba(220, 53, 69, 0.1)';
        ctx.fill();
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