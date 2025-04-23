document.addEventListener("DOMContentLoaded", function() {
    // Pagination variables
    const itemsPerPage = 10;
    let currentPage = 1;
    const rows = document.querySelectorAll("#config-tbody tr");
    const totalPages = Math.ceil(rows.length / itemsPerPage);
    
    // Initialize pagination
    updatePagination();
    
    // Add event listeners to pagination buttons
    document.querySelectorAll(".pagination .page-item:not(#prevPageBtn):not(#nextPageBtn)").forEach(item => {
        item.addEventListener("click", function(e) {
            e.preventDefault();
            currentPage = parseInt(this.getAttribute("data-page"));
            updatePagination();
        });
    });
    
    // Previous page button
    document.getElementById("prevPageBtn").addEventListener("click", function(e) {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });
    
    // Next page button
    document.getElementById("nextPageBtn").addEventListener("click", function(e) {
        e.preventDefault();
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });
    
    // Function to update pagination
    function updatePagination() {
        // Update current page display
        document.getElementById("currentPage").textContent = currentPage;
        
        // Show/hide rows based on current page
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        
        rows.forEach((row, index) => {
            if (index >= startIndex && index < endIndex) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
        
        // Update active page button
        document.querySelectorAll(".pagination .page-item:not(#prevPageBtn):not(#nextPageBtn)").forEach(item => {
            if (parseInt(item.getAttribute("data-page")) === currentPage) {
                item.classList.add("active");
            } else {
                item.classList.remove("active");
            }
        });
        
        // Update prev/next buttons
        if (currentPage === 1) {
            document.getElementById("prevPageBtn").classList.add("disabled");
        } else {
            document.getElementById("prevPageBtn").classList.remove("disabled");
        }
        
        if (currentPage === totalPages || totalPages === 0) {
            document.getElementById("nextPageBtn").classList.add("disabled");
        } else {
            document.getElementById("nextPageBtn").classList.remove("disabled");
        }
    }
});