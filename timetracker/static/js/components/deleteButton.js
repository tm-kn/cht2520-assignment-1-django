const confirmDeletion = ev => {
    if (!window.confirm('Do you want to delete this item?')) {
        ev.preventDefault();
    }
}


export default () => {
    document.querySelectorAll('.js-delete-button').forEach(v => {
        v.addEventListener('click', confirmDeletion);
    });
};
