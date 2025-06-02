
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
function formatDateFromString(dateString) {
  const [day, month, year] = dateString.split('.');
  const formattedDate = new Date(`${year}-${month}-${day}`);

  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  return formattedDate
}

const workingDay = getNextWorkingDay(new Date())
function isEqual(date) {
  return (
    date.getDate() === workingDay.getDate() &&
    date.getMonth() === workingDay.getMonth() &&
    date.getFullYear() === workingDay.getFullYear()
  );
}

function isEqueal_to(date1, date2){
    return (
    date1.getDate() === date2.getDate() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getFullYear() === date2.getFullYear()
  );
}

document.addEventListener('DOMContentLoaded', function() {
  const thElements = document.querySelectorAll('th.colspan2');

  thElements.forEach(th => {
    const dateString = th.getAttribute('date');
    if (dateString && dateString !== 'None') {
      const date = formatDateFromString(dateString);
      if (isEqual(date)) {
        th.style.backgroundColor = '#639551';
      } else {
          let today = new Date()
          let isBefore10AM = today.getHours() < 10;
          if(isEqueal_to(today, date) && isBefore10AM){
            th.style.backgroundColor = '#639551';
          }else{
              th.style.backgroundColor = '#A27575';
          }
      }
    } else {
      th.style.backgroundColor = '#525551';
    }
  });
});