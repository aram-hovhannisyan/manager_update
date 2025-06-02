document.addEventListener('DOMContentLoaded', function() {
    let allTables = document.querySelectorAll('table');
    allTables.forEach((table) => {
        let tbody = table.querySelector('tbody');
        let rows = tbody.querySelectorAll('tr');
        let totalSum = 0;
        let total = table.querySelector('thead tr').lastChild
        // tbody.lastChild.removeChild(tbody.lastChild.querySelector('.totalcolumn-row'))
        total.setAttribute('colspan', 2)
        rows.forEach((row) => {
            let product = row.querySelector("#product") || null;
            let totalCell = row.querySelector(".totalcolumn-row") || null;
            let newCell = document.createElement("td");
            if(product && totalCell){
                newCell.textContent = parseInt(product.getAttribute('supPrice')) * parseInt(totalCell.textContent.trim())
                newCell.id = 'new_Cell'
                row.appendChild(newCell);
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    let allTables = document.querySelectorAll('table');
    allTables.forEach((table) => {
        const newCells = table.querySelectorAll('#new_Cell')
        let tbody = table.querySelector('tbody');
        let lastRow = tbody.lastChild.previousSibling
        let rem = lastRow.querySelector('.totalcolumn-row')
        lastRow.removeChild(rem)
            
        let sum = 0
        newCells.forEach((cell)=>{
            if(parseInt(cell.textContent.trim())){
                sum += parseInt(cell.textContent.trim())
            }
        })
        table.querySelector('#total-total').textContent = sum
        table.querySelector('#total-total').style.color = 'red'
        console.log(tbody.firstChild.nextSibling.childNodes.length);
        table.querySelector('#total-total').setAttribute('colspan', tbody.firstChild.nextSibling.childNodes.length)
    })
});