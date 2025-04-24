// patches_management.js

document.addEventListener('DOMContentLoaded', function () {
    const tbody = document.getElementById('patches-tbody');
    const rows = tbody.getElementsByTagName('tr');
    const totalPatches = rows.length;
    const itemsPerPage = 10; // Số bản ghi mỗi trang
    let currentPage = 1;

    const paginationInfo = document.getElementById('pagination-info');
    const totalPatchesSpan = document.getElementById('total-patches');
    const paginationControls = document.getElementById('pagination-controls');

    // Hiển thị tổng số bản ghi
    totalPatchesSpan.textContent = totalPatches;

    // Hàm hiển thị các hàng cho trang hiện tại
    function displayRows(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        // Ẩn tất cả các hàng
        for (let i = 0; i < rows.length; i++) {
            rows[i].style.display = 'none';
        }

        // Hiển thị các hàng cho trang hiện tại
        for (let i = start; i < end && i < totalPatches; i++) {
            rows[i].style.display = '';
        }

        // Cập nhật thông tin phân trang
        const showingCount = Math.min(itemsPerPage, totalPatches - start);
        paginationInfo.textContent = showingCount;
    }

    // Hàm tạo các nút phân trang
    function createPagination() {
        const pageCount = Math.ceil(totalPatches / itemsPerPage);
        paginationControls.innerHTML = ''; // Xóa các nút cũ

        // Nút Previous
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

        // Các nút số trang
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

        // Nút Next
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

    // Khởi tạo phân trang
    if (totalPatches > 0) {
        displayRows(currentPage);
        createPagination();
    }
});