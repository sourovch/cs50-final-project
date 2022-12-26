const checkboxes = document.querySelectorAll('.form-check-input');

checkboxes.forEach((checkboxe) => {
  checkboxe.addEventListener('change', () => {
    const todoId = checkboxe.dataset.id;

    fetch(`/todos/change/${todoId}`)
      .then((res) => {
        if (res.status !== 200) {
          checkboxe.checked = checkboxe.checked ? false : true;
        }
      })
      .catch(() => {
        checkboxe.checked = checkboxe.checked ? false : true;
      });
  });
});
