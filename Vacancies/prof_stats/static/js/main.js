const tableForm = document.querySelector('.stats-form')
const showButtons = document.querySelectorAll('.table-button');
const closeButton = document.querySelector('.close')
console.log(closeButton)

for (let button of showButtons) {
    button.addEventListener('click', () => {
        const stat = button.classList[1];
        console.log(stat)
        tableForm.classList.remove('hidden')
        const table = document.querySelector(`.stats-table.${stat}`).cloneNode(true)
        table.classList.remove('hidden')
        tableForm.insertBefore(table, tableForm.firstChild);
    });
}

closeButton.addEventListener('click', () => {
    tableForm.classList.add('hidden')
    const table = tableForm.querySelector(`.stats-table`)
    tableForm.removeChild(table)
});


