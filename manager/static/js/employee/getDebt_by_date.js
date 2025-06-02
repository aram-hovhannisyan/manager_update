document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.date-cell').forEach(function(cell) {
        cell.addEventListener('click', function() {
            var date = cell.dataset.date;
            showDebtsForDate(date);
            // console.log(date);
        });
    });

    function showDebtsForDate(date) {
        fetch(`/debts_by_date/${date}/`)
            .then(response => response.json())
            .then( (data) => {
                // console.log(data, 'response');
                const debtDetails = document.querySelector('#parentTot');
                // console.log(debtDetails);
                const tbody = document.querySelector('#debtDetails_body')
                tbody.innerHTML = '';
                console.log(tbody);
                const childDiv = document.querySelector('#debtDetails')
                let art = 0
                let ayl = 0
                data.forEach(function(debt) {
                    art += debt[1] || 0
                    ayl += debt[2] || 0
                    let row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${debt[0]}</td>
                        <td>${debt[1]}</td>
                        <td>${debt[2]}</td>
                        <td>${debt[1] + debt[2]}</td>
                    `;
                    tbody.appendChild(row);
                    const screenWidth = window.innerWidth;
                    const close = document.querySelector('#x')

                    close.addEventListener('click', function(){
                        debtDetails.style.display = "none";
                    })
                if (screenWidth <= 600) {
                    debtDetails.style.fontSize = '13px';
                    debtDetails.style.display = 'block';
                    debtDetails.style.bottom = '1540px';
                    childDiv.style.width = '300px'
                    close.style.left = '287px'

                } else {
                    debtDetails.style.width = '100%';
                    debtDetails.style.fontSize = '1em';
                    debtDetails.style.display = 'block';
                    debtDetails.style.bottom = '1750px';
                    childDiv.style.width = '1000px'
                    close.style.left = '875px'

                }
                })
                let r = document.createElement('tr');
                r.innerHTML = `
                    <td>Ընդհանուր</td>
                    <td>${art}</td>
                    <td>${ayl}</td>
                    <td>${art + ayl}</td>
                `;
                tbody.appendChild(r);
            })
            }});