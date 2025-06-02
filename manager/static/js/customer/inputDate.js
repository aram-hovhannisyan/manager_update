// const inputDates = document.querySelectorAll('#inputDate');
// // console.log(inputDate.getAttribute('class'));
// const today = new Date();
// const formattedDate = today.toISOString().split('T')[0];
// inputDates.forEach(input => {
//     input.value = formattedDate
// })
function getNextWorkingDay(date) {
  const dayOfWeek = date.getDay();

  if (dayOfWeek === 5) { // Friday
    date.setDate(date.getDate() + 3); // Move to Monday
  } else if (dayOfWeek === 6) { // Saturday
    date.setDate(date.getDate() + 2); // Move to Monday
  } else {
    date.setDate(date.getDate() + 1); // Move to next day
  }

  return date;
}

const inputDates = document.querySelectorAll('#inputDate');
const today = new Date();
const nextWorkingDay = getNextWorkingDay(today);

const year = nextWorkingDay.getFullYear();
const month = String(nextWorkingDay.getMonth() + 1).padStart(2, '0');
const day = String(nextWorkingDay.getDate()).padStart(2, '0');

const formattedDate = `${year}-${month}-${day}`;
// const formattedDate = `2024-09-02`;

inputDates.forEach(input => {
  input.value = formattedDate;
});