const container = document.querySelector('.input-container')
const vacanciesButton = container.querySelector('.vacancies-button')
const input = container.querySelector('.input-form')
const vacanciesList = document.querySelector('.vacancies-list')
const vacancyTemplate = document.querySelector('#vacancy').content.querySelector('.vacancy')
const vacanciesUrl = 'http://127.0.0.1:8000/vacancies/?day='


const createVacancy = (vacancy) => {
    const vacancyItem = vacancyTemplate.cloneNode(true)
    vacancyItem.querySelector('.vacancy-url').href = vacancy['url']
    vacancyItem.querySelector('.vacancy-title').textContent = vacancy['name']
    vacancyItem.querySelector('.description').textContent = vacancy['description']
    vacancyItem.querySelector('.skills').textContent = vacancy['skills']
    vacancyItem.querySelector('.company').textContent = vacancy['company']
    vacancyItem.querySelector('.salary').textContent = `${vacancy["salary"]} рублей`
    vacancyItem.querySelector('.area-name').textContent = vacancy['area_name']
    vacancyItem.querySelector('.published-at').textContent = vacancy['published_at'].slice(0, 10)
    vacanciesList.appendChild(vacancyItem)
}

const showVacancies = (json) => {

    const vacancies = json['items']
    if (vacancies.length === 0) {
        alert('К сожалению ничего не найдено. Попробуйте ввести друго день')
        vacanciesButton.textContent = "Показать вакансии";
        vacanciesButton.disabled = false;
    } else {
        container.classList.add('hidden')
        vacancies.forEach((vacancy) => createVacancy(vacancy))
    }
}

const errorLoad = () => {
    vacanciesButton.textContent = "Показать вакансии";
    vacanciesButton.disabled = false;
    alert('Не удалось получить данные');
}

vacanciesButton.addEventListener('click', (evt) => {
    fetch(`${vacanciesUrl}${input.value}`)
        .then(response => response.json())
        .then(response => showVacancies(response))
        .catch(() => errorLoad())
    vacanciesButton.textContent = "Загрузка";
    vacanciesButton.disabled = true;
});