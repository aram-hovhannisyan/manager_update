
// function getNextWorkingDay(date) {
//     const dayOfWeek = date.getDay();

//     if (dayOfWeek === 5) { // Friday
//         date.setDate(date.getDate() + 3); // Move to Monday
//     } else if (dayOfWeek === 6) { // Saturday
//         date.setDate(date.getDate() + 2); // Move to Monday
//     } else {
//         date.setDate(date.getDate() + 1); // Move to next day
//     }

//     return date;
// }
// function formatDateFromString(dateString) {
//     const [day, month, year] = dateString.split('.');
//     const formattedDate = new Date(`${year}-${month}-${day}`);

//     const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
//     return formattedDate
// }

// const workingDay = getNextWorkingDay(new Date())
// function isEqual(date) {
//     return (
//         date.getDate() === workingDay.getDate() &&
//         date.getMonth() === workingDay.getMonth() &&
//         date.getFullYear() === workingDay.getFullYear()
//     );
// }
// function red_or_green(th) {

//     const dateString = th.getAttribute('date');
//     if (dateString && dateString !== 'None') {
//         const date = formatDateFromString(dateString);
//         if (isEqual(date)) {
//             th.style.backgroundColor = '#639551';
//         } else {
//             th.style.backgroundColor = '#A27575';
//         }
//     } else {
//         th.style.backgroundColor = '#525551';
//     }
// }

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

function red_or_green(th){
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

}



// Function to add total row at the end of each table
let totObj = {}

function addTotalRow(table) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');

    // Get the number of columns to sum
    const numColumns = rows[0].querySelectorAll('td').length - 1;

    // Create a new row
    const totalRow = document.createElement('tr');
    totalRow.classList.add('total-row');

    // Add the "Total" label to the first column
    const totalLabel = document.createElement('td');
    totalLabel.textContent = 'Ընդհանուր';
    totalRow.appendChild(totalLabel);

    // Sum the values in each column and add them to the row
    for (let i = 0; i < numColumns; i++) {
        let sum = 0;
        for (let j = 0; j < rows.length; j++) {
            const cell = rows[j].querySelectorAll('td')[i + 1];
            try{
            if (cell.textContent.trim() === '') {
                cell.textContent = '0';
            }
            sum += Number(cell.textContent);
            }
            catch{}
        }
        const totalCell = document.createElement('td');
        totalCell.textContent = sum;
        totalCell.classList.add('total-cell')
        totalRow.appendChild(totalCell);
    }

    // Add the row to the table
    tbody.appendChild(totalRow);
}

// Function to add total column to each table
function addTotalColumn(table) {
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');

    // Create a new header cell for the total column
    const totalHeader = document.querySelector('.total-column');
    let lastSupCellSum = 0

    // Sum the product counts for each row and add the total to a new cell in each row
    for (let i = 0; i < rows.length; i++) {

        const cells = rows[i].querySelectorAll('td');
        const supCells = rows[i].querySelectorAll('th')
        let supTotal = 0
        for (let s = 0; s < supCells.length; s++) {
            supTotal += parseInt(supCells[s].textContent, 10)
            rows[i].removeChild(supCells[s])
        }

        // const sumCells = rows[i].querySelectorAll('td');
        let total = 0;
        let totalSum = 0;
        for (let j = 1; j < cells.length; j += 2) {
            total += parseInt(cells[j].textContent, 10);
            totalSum += parseInt(cells[j + 1].textContent, 10);
        }
        const totalCell = document.createElement('td');
        const totalSumCell = document.createElement('td');
        const supTotalCell = document.createElement('td')

        supTotalCell.classList.add('supTotal')

        totalCell.classList.add('totalcolumn-count');
        totalSumCell.classList.add('totalcolumn-row');

        if (!totalSum) {
            totalSumCell.textContent = '0';
        } else {
            totalSumCell.textContent = totalSum;
        }
        if (!total) {
            totalCell.textContent = '0';
        } else {
            totalCell.textContent = total;
        }
        if (!supTotal) {
            supTotalCell.textContent = '0';
        } else {
            supTotalCell.textContent = supTotal;
        }
        lastSupCellSum += supTotal
        if (i == rows.length - 1) {
            supTotalCell.textContent = lastSupCellSum
            let attr = table.getAttribute('name')
            totObj[attr] = totalSum
        }

        supTotalCell.style.display = 'none'
        supTotalCell.style.color = 'red'
        rows[i].appendChild(totalCell);
        rows[i].appendChild(totalSumCell);
        rows[i].appendChild(supTotalCell)

    }
}
// const tables = document.querySelectorAll('.big-table');

// tables.forEach((table)=>{
//   if(table.getAttribute('name') === 'Կիրովական'){
//     let theBody = table.querySelector('tbody')
//     let theRows = theBody.querySelector('tr')
//     let newRow = document.createElement('tr')
//     let lenRow = theRows.querySelectorAll('td').length //
//     let newCell = document.createElement('td') //
//     newCell.textContent = Summary //
//     newCell.setAttribute('colspan', lenRow) //
//     newCell.style.textAlign = 'end'
//     newCell.style.borderTop = '1px solid black'
//     newRow.appendChild(newCell) //
//     theBody.appendChild(newRow) //
//   }
// })
function addSupTotal(row) {
    // console.log(row);
    let product = row.firstChild
    // console.log(product);
    let countCell = row.querySelector(".totalcolumn-count")
    let supTotal = row.querySelector(".supTotal")
    supTotal.textContent = parseInt(countCell.textContent.trim()) * parseInt(product.getAttribute('supPrice'))
}
// Function to export table content to Excel and trigger download
function exportToExcel(table, fileName) {
    const tds = table.querySelectorAll('td')
    tds.forEach((td) => {
        if (parseInt(td.textContent.trim()) === 0) {
            td.innerText = ''
        }
    })
    const rows = table.querySelectorAll('tbody tr');
    const headerRow = table.querySelector('thead tr')
    const headers = table.querySelectorAll("thead tr th")
    headers.forEach((header) => {
        if (header.style.display === 'none') {
            headerRow.removeChild(header)
        }
    })

    rows.forEach(row => {
        for (const el of row.children) {
            // console.log(el);
            if (el.style.display === 'none') {
                // console.log(el);
                row.removeChild(el)
            }
        }
    }
    )
    rows.forEach(row => {
        for (const el of row.children) {
            // console.log(el);
            if (el.style.display === 'none') {
                // console.log(el);
                row.removeChild(el)
            }
        }
    }
    )
    rows.forEach(row => {
        for (const el of row.children) {
            // console.log(el);
            if (el.style.display === 'none') {
                // console.log(el);
                row.removeChild(el)
            }
        }
    }
    )



    const wb = XLSX.utils.table_to_book(table);
    const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const blob = new Blob([wbout], { type: "application/octet-stream" });

    // Check if the browser supports the download attribute
    if (typeof navigator.msSaveBlob !== "undefined") {
        // For IE and Edge browsers
        navigator.msSaveBlob(blob, fileName);
    } else {
        // For other browsers
        const link = document.createElement("a");
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", fileName);
            link.style.visibility = "hidden";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }
    }
}

function addTotal_cell(table){
    let totalcell = table.lastChild.lastChild.lastChild

    totalcell.textContent = 0
    // console.log(totalcell);
    let cells = table.querySelectorAll('tbody .supTotal')
    let sum = 0
    cells.forEach((cell)=> {
        // console.log(cell.textContent);
        sum += parseInt(cell.textContent)
    })
    totalcell.textContent = sum

}


document.addEventListener('DOMContentLoaded', function () {
    // Function to make an AJAX request to fetch data from the backend
    function fetchDataFromBackend(callback) {
        const url = '/api/other_items/';
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);

        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 400) {
                const data = JSON.parse(xhr.responseText);
                callback(data);
            } else {
                console.error('Error fetching data from the backend');
            }
        };

        xhr.onerror = function () {
            console.error('Error fetching data from the backend');
        };

        xhr.send();
    }
    function format_date(value) {
        if (!value) {
            return value;
        }
        const date = new Date(value);
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();
        return `${day}.${month}.${year}`;
    }
    function createTableHeadingDiv(supplier) {
        const br1 = document.createElement('br');
        const tableHeadingDiv = document.createElement('div');
        tableHeadingDiv.classList.add('table-heading-div');

        const h1 = document.createElement('h1');
        h1.style.width = 'auto';
        h1.textContent = supplier.username;



        const changeDiv = document.createElement('div');
        changeDiv.classList.add('change');

        const removeButton = document.createElement('button');
        removeButton.classList.add(`remove-Button${supplier.id}`);
        removeButton.id = 'changeSend';
        removeButton.textContent = 'Փոխել';
        removeButton.addEventListener('click', function () {
            handleRemoveButtonClick(supplier.id);
        });

        const excelButton = document.createElement('button');
        excelButton.classList.add(`export-Button${supplier.id}`);
        excelButton.id = 'changeSend';
        excelButton.textContent = 'Excel';
        excelButton.addEventListener('click', (event) => {
            const table = document.getElementById(supplier.id);
            const today = new Date().toISOString().split('T')[0];
            const fileName = prompt("Enter the file name", `table_${today}.xlsx`);
            if (fileName) {
                exportToExcel(table, fileName);
                window.location.reload();
            }
        });
        const sendButton = document.createElement('button');
        sendButton.addEventListener('click', function () {
            sendOrder(supplier.id, supplier.username);
        });
        sendButton.id = 'changeSend';
        sendButton.textContent = 'Ուղարկել';

        changeDiv.appendChild(removeButton);
        changeDiv.appendChild(excelButton);
        changeDiv.appendChild(sendButton);

        tableHeadingDiv.appendChild(h1);
        tableHeadingDiv.appendChild(br1);
        tableHeadingDiv.appendChild(changeDiv);

        return tableHeadingDiv;
    }

    function generateTableBody(Products, BigTables, TableRows, supplier) {
        const tbody = document.createElement('tbody');
        const cellsToRemove = [];

        for (let i = 0; i < Products.length; i++) {
            const product = Products[i];
            if (product.supplier === supplier.username) {
                const tr = document.createElement('tr');

                const tdProductName = document.createElement('td');
                tdProductName.textContent = product.productName;
                tdProductName.setAttribute('supPrice', product.supPrice);
                tr.appendChild(tdProductName);

                for (let j = 0; j < BigTables.length; j++) {
                    const bigtable = BigTables[j];
                    if (bigtable.supplier_id === supplier.id) {
                        for (let k = 0; k < TableRows.length; k++) {
                            const row = TableRows[k];
                            if (row.supplier_id === supplier.id) {
                                if (
                                    row.porductName === product.productName &&
                                    row.table === bigtable.table
                                ) {

                                    const tdProductCount = document.createElement('td');
                                    tdProductCount.setAttribute('name', row.user);
                                    tdProductCount.textContent = row.productCount;
                                    tr.appendChild(tdProductCount);

                                    const tdTotalPrice = document.createElement('td');
                                    tdTotalPrice.textContent = row.totalPrice;
                                    tr.appendChild(tdTotalPrice);

                                    cellsToRemove.push(k); // Remember to remove this cell after rendering
                                    break; // Found the matching row, no need to continue looping
                                }
                            }
                        }
                    }
                    tbody.appendChild(tr);
                }
            }
        }


        // Remove cells from TableRows
        cellsToRemove.sort((a, b) => b - a); // Sort in reverse order to avoid index conflicts
        for (const index of cellsToRemove) {
            TableRows.splice(index, 1);
        }

        return tbody;
    }


    function createBigTable(supplier, BigTables, data) {

        const table = document.createElement('table');
        table.classList.add('big-table');
        table.setAttribute('name', supplier.username);
        table.setAttribute('id', supplier.id);

        const thead = document.createElement('thead');

        const tr = document.createElement('tr');

        const thProduct = document.createElement('th');
        thProduct.textContent = 'Ապրանք';

        tr.appendChild(thProduct);

        for (let i = 0; i < BigTables.length; i++) {
            const bigtable = BigTables[i];
            // console.log(bigtable);
            if (bigtable.supplier_id === supplier.id) {
                const thUser = document.createElement('th');
                thUser.setAttribute('colspan', '2');
                thUser.classList.add('colspan2');
                thUser.setAttribute('date', format_date(bigtable.modifiedDate));
                thUser.setAttribute('name', bigtable.user);
                thUser.textContent = bigtable.user;
                red_or_green(thUser)
                tr.appendChild(thUser);

            }
        }

        const thTotal = document.createElement('th');
        thTotal.classList.add('total-column');
        thTotal.setAttribute('colspan', '2');
        thTotal.textContent = 'Ընդհանուր';

        tr.appendChild(thTotal);

        thead.appendChild(tr);
        table.appendChild(thead);
        const Products = data.Products
        const TableRows = data.TableRows
        console.log(supplier);

        table.appendChild(generateTableBody(Products, BigTables, TableRows, supplier))
        addTotalRow(table);
        addTotalColumn(table);
        rows = table.querySelectorAll('tbody tr')
        rows.forEach((row) => {
            addSupTotal(row)

        })
        addTotal_cell(table)
        return table;
    }
    // Function to render the table for a specific supplier
    function renderTable(data) {
        const suppliers = data.Suppliers
        const BigTables = data.BigTables
        console.log(data)
        console.log(suppliers);
        for (const supplier of suppliers) {
            const br2 = document.createElement('br');
            const br3 = document.createElement('br');
            const br4 = document.createElement('br');
            const br5 = document.createElement('br');
            const br6 = document.createElement('br');
            const br7 = document.createElement('br');
            document.body.appendChild(createTableHeadingDiv(supplier))
            document.body.appendChild(br5)
            document.body.appendChild(br6)
            document.body.appendChild(br7)
            document.body.appendChild(createBigTable(supplier, BigTables, data))
            document.body.appendChild(br2)
            document.body.appendChild(br3)
            document.body.appendChild(br4)

        }

        console.log(data);

    }

    fetchDataFromBackend(function (data) {
        renderTable(data); // Render table for supplier with ID 1

    });
});



