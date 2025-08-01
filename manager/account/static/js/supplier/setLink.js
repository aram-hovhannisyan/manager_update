
function processTable(table) {
    console.log('process', table);
    const allChangeItems = document.querySelectorAll(".changes");
    console.log(allChangeItems);
    const keys = [];
    const allTds = table.querySelectorAll('td');
    const linkElements = [];
    const ohan_Users = ['Գ.4-րդ', 'Գ.ավագ', 'Արա'];
    const kamo_Users = ['Գանձակ', 'Սարուխան'];

    allChangeItems.forEach((item) => {
        let key = item.getAttribute('change_key');
        console.log(key);
        if (key) {
            keys.push(key);
        }
    });

    allTds.forEach((td) => {
        let key = td.getAttribute('key');
        if (keys.includes(key)) {
            setTimeout(() => {
                td.style.color = 'white';
            }, 2100);
            const link = document.createElement('a');
            td.style.backgroundColor = '#ff3333';
            link.href = `/account/supplier_endorse/${td.getAttribute('custId')}/`;
            td.addEventListener('click', function() {
                window.location.href = link.href; // Redirect to the link
            });

            let parentName = td.getAttribute('name');
            let par = td.parentElement.querySelector(`[name="${parentName}"]`);

            if (ohan_Users.includes(parentName) || kamo_Users.includes(parentName)) {
                par.style.backgroundColor = '#ff3333';
                par.addEventListener('click', function() {
                    window.location.href = link.href; // Redirect to the link
                });
            }
        }
    });
}