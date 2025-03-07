document.querySelector('form').addEventListener('submit', function (event) {
    if (event.target.tagName === 'form') {
        var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        loadingModal.show();
    }
});