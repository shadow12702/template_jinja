// bp_management.js

document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('best-practices-tbody');
    const rows = tbody.getElementsByTagName('tr');
    const totalBestPractices = rows.length;
    const itemsPerPage = 10; // Number of best practices per page
    let currentPage = 1;

    const paginationInfo = document.getElementById('pagination-info');
    const totalBestPracticesSpan = document.getElementById('total-best_practice');
    const paginationControls = document.getElementById('pagination-controls');

    // Display total number of best practices
    totalBestPracticesSpan.textContent = totalBestPractices;

    // Function to display rows for the current page
    function displayRows(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        // Hide all rows
        for (let i = 0; i < rows.length; i++) {
            rows[i].style.display = 'none';
        }

        // Show rows for the current page
        for (let i = start; i < end && i < totalBestPractices; i++) {
            rows[i].style.display = '';
        }

        // Update pagination info (e.g., "Showing 10 of 25 best practices")
        const showingCount = Math.min(itemsPerPage, totalBestPractices - start);
        paginationInfo.textContent = showingCount;
    }

    // Function to create pagination controls
    function createPagination() {
        const pageCount = Math.ceil(totalBestPractices / itemsPerPage);
        paginationControls.innerHTML = ''; // Clear existing controls

        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = 'page-item' + (currentPage === 1 ? ' disabled' : '');
        prevLi.innerHTML = `<a class="page-link" href="#" aria-label="Previous">Previous</a>`;
        prevLi.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                displayRows(currentPage);
                createPagination();
            }
        });
        paginationControls.appendChild(prevLi);

        // Page number buttons
        for (let i = 1; i <= pageCount; i++) {
            const li = document.createElement('li');
            li.className = 'page-item' + (i === currentPage ? ' active' : '');
            li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            li.addEventListener('click', (e) => {
                e.preventDefault();
                currentPage = i;
                displayRows(currentPage);
                createPagination();
            });
            paginationControls.appendChild(li);
        }

        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = 'page-item' + (currentPage === pageCount ? ' disabled' : '');
        nextLi.innerHTML = `<a class="page-link" href="#" aria-label="Next">Next</a>`;
        nextLi.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentPage < pageCount) {
                currentPage++;
                displayRows(currentPage);
                createPagination();
            }
        });
        paginationControls.appendChild(nextLi);
    }

    // Initialize pagination
    if (totalBestPractices > 0) {
        displayRows(currentPage);
        createPagination();
    }
});