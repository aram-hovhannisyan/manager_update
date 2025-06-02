const paymanatform = document.querySelector('.paymant')
    const payButton = document.querySelector('.paymantButton')
    payButton.addEventListener('click', ()=>{
        if(paymanatform.style.display === 'none'){
            payButton.innerHTML = 'Փակել'
            payButton.style.textAlign = 'center'
            paymanatform.style.display = 'block'
        }else if(paymanatform.style.display === 'block'){
            payButton.innerHTML = 'Կատարել Վճարում'
            paymanatform.style.display = 'none'
        }
        // console.log(paymanatform.style.display)
    })
    const options = document.querySelectorAll('.WeekOption');
    const today = new Date();
    function parseDate(dateString) {
        const parts = dateString.split('.');
        // Note: months are 0-based in JavaScript Date objects
        const date = new Date(parts[2], parts[1] - 1, parts[0]);
        return date;
    }
    options.forEach((option) => {
        let optionDate = new Date(parseDate(option.value));
        // Calculate the difference in days between today and the option date
        const timeDifference = today.getTime() - optionDate.getTime();
        const dayDifference = timeDifference / (1000 * 3600 * 24);
        // If the option date is within the last 7 days, select it
        if (dayDifference >= 0 && dayDifference <= 7) {
            // option.setAttribute('selected', true)
            option.selected = true
        }
});