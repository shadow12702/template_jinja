document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('awr-tbody');
    const rows = tbody.getElementsByTagName('tr');
    const totalRecords = rows.length;
    const itemsPerPage = 10; // Số bản ghi mỗi trang
    let currentPage = 1;

    const paginationInfo = document.querySelector('.pagination-info');
    const currentRowsSpan = document.querySelector('.current-rows');
    const totalRowsSpan = document.querySelector('.total-rows');
    const paginationControls = document.getElementById('databaseTable-pagination');

    // Hàm hiển thị các hàng cho trang hiện tại
    function displayRows(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        // Ẩn tất cả các hàng
        for (let i = 0; i < rows.length; i++) {
            rows[i].style.display = 'none';
        }

        // Hiển thị các hàng cho trang hiện tại
        for (let i = start; i < end && i < totalRecords; i++) {
            rows[i].style.display = '';
        }

        // Cập nhật thông tin phân trang
        const showingCount = Math.min(itemsPerPage, totalRecords - start);
        currentRowsSpan.textContent = showingCount;
        totalRowsSpan.textContent = totalRecords;
    }

    // Hàm tạo các nút phân trang
    function createPagination() {
        const pageCount = Math.ceil(totalRecords / itemsPerPage);
        // Xóa các nút số trang cũ, giữ lại Previous và Next
        const existingPages = paginationControls.querySelectorAll('.page-item:not(.prev-page):not(.next-page)');
        existingPages.forEach(page => page.remove());

        // Cập nhật trạng thái nút Previous
        const prevButton = document.getElementById('databaseTable-prev');
        prevButton.className = 'page-item prev-page' + (currentPage === 1 ? ' disabled' : '');
        prevButton.querySelector('a').addEventListener('click', (e) => {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                displayRows(currentPage);
                createPagination();
            }
        });

        // Thêm các nút số trang trước nút Next
        const nextLi = paginationControls.querySelector('.next-page');
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
            paginationControls.insertBefore(li, nextLi);
        }

        // Cập nhật trạng thái nút Next
        const nextButton = document.getElementById('databaseTable-next');
        nextButton.className = 'page-item next-page' + (currentPage === pageCount ? ' disabled' : '');
        nextButton.querySelector('a').addEventListener('click', (e) => {
            e.preventDefault();
            if (currentPage < pageCount) {
                currentPage++;
                displayRows(currentPage);
                createPagination();
            }
        });
    }

    // Khởi tạo phân trang
    if (totalRecords > 0) {
        displayRows(currentPage);
        createPagination();
    }
});