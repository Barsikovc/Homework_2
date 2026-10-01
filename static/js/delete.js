// Подтверждение удаления книги
document.addEventListener('DOMContentLoaded', function () {
    const deleteForms = document.querySelectorAll('form.delete-form');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!confirm('Вы уверены, что хотите удалить эту книгу?')) {
                event.preventDefault();
            }
        });
    });
});
