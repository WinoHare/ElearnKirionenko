const showButtons = document.querySelectorAll('.table-button');
const closeButtons = document.querySelectorAll('.close')

for (let button of showButtons) {
    button.addEventListener('click', () => {
        let stat = button.classList[1];
        document.querySelector(`.stats-form.${stat}`).classList.remove('hidden')

    });
}

for (let button of closeButtons) {
    button.addEventListener('click', () => {
        let stat = button.classList[1];
        document.querySelector(`.stats-form.${stat}`).classList.add('hidden')
    });
}

