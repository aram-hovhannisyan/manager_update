function formatDateTime(value) {
    if (!value) {
        return;
    }

    const date = new Date(value);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Note: January is 0!
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    const formatted_date = `${day}.${month}.${year} ${hours}:${minutes}`;
    return formatted_date;
}

document.addEventListener('DOMContentLoaded', function () {
    const supplier_id = document.querySelector('#supplier_id').textContent
    const page = document.querySelector('#supplier_id').getAttribute('page')
    fetch('/api/get_ordereed_tables/' + supplier_id + '/' + page + '/')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Process data and generate HTML tables
            data.Tables.forEach(table => {
                const tableElement = document.createElement('table');
                tableElement.setAttribute('supId', table.table);
                tableElement.id = data.supplier.id
                // Create table header
                const thead = document.createElement('thead');
                const headerRow = document.createElement('tr');
                const headerCell = document.createElement('th');
                headerCell.textContent = 'Ապրանք';
                headerRow.appendChild(headerCell);



                data.Columns.forEach(column => {
                    if (column.parentTable === table.table) {
                        const headerCell = document.createElement('th');
                        headerCell.setAttribute('name', column.customerofTable);
                        headerCell.textContent = column.customerofTable;
                        headerRow.appendChild(headerCell);
                    }
                });
                const totalHeader = document.createElement('th');
                totalHeader.textContent = 'Ընդհանուր';
                totalHeader.setAttribute('colspan', 2);
                headerRow.appendChild(totalHeader);
                thead.appendChild(headerRow);
                tableElement.appendChild(thead);

                // Create table body
                const tbody = document.createElement('tbody');
                let table_total = 0
                data.Products.forEach(product => {
                    const row = document.createElement('tr');

                    const productCell = document.createElement('td');
                    productCell.setAttribute('id', 'product');
                    productCell.setAttribute('supPrice', product.supPrice);

                    productCell.style.display = "block";
                    productCell.style.whiteSpace = "pre-line";
                    productCell.textContent = product.productName.split(" ").join("\n");

                    row.appendChild(productCell);
                    let pr_counter = 0
                    data.Columns.forEach((column) => {
                        for (const rowItem of data.TableRows) {
                            if (
                                column.parentTable === table.table &&
                                rowItem.parentColumn === column.column &&
                                rowItem.productName === product.productName
                            ) {
                                const cell = document.createElement('td');
                                cell.setAttribute('name', column.customerofTable);
                                cell.setAttribute('key', rowItem.getId);
                                cell.setAttribute('custId', column.parentTable);
                                cell.textContent = rowItem.productCount;
                                row.appendChild(cell);
                                pr_counter += parseInt(rowItem.productCount)
                                break;
                            }
                        }
                        const rowIndex = data.TableRows.findIndex(item => (
                            item.parentColumn === column.column &&
                            item.productName === product.productName
                        ));

                        // if (rowIndex !== -1) {
                        //     data.TableRows.splice(rowIndex, 1);
                        // }
                    })

                    const tot = document.createElement('td');
                    const count = document.createElement('td');

                    tot.textContent = pr_counter * product.supPrice;
                    table_total += pr_counter * product.supPrice
                    count.textContent = pr_counter;
                    row.appendChild(count);
                    row.appendChild(tot);
                    // pr_counter += parseInt(rowItem.productCount)
                    tbody.appendChild(row);

                });
                // Add row with totals
                const totalRow = document.createElement('tr');
                const totalCell = document.createElement('td');
                totalCell.setAttribute('colspan', '2'); // edited
                totalCell.textContent = formatDateTime(table.date);
                totalRow.appendChild(totalCell);

                const totalTotalCell = document.createElement('td');
                totalTotalCell.setAttribute('id', 'total-total');
                totalTotalCell.setAttribute('colspan', data.Columns.length);

                totalTotalCell.style.textAlign = 'end';
                totalTotalCell.style.fontSize = '22px';
                totalTotalCell.textContent = table_total
                totalRow.appendChild(totalTotalCell);

                tbody.appendChild(totalRow);

                tableElement.appendChild(tbody);
                const br2 = document.createElement('br');
                const br3 = document.createElement('br');
                const br4 = document.createElement('br');
                // Append table to the document body or a specific element in your HTML
                const changeDiv = document.createElement('div');
                changeDiv.classList.add('change');
                const excelButton = document.createElement('button');
                excelButton.classList.add(`export-Button${data.supplier.id}`);
                excelButton.id = 'changeSend';
                excelButton.textContent = 'Excel';
                excelButton.addEventListener('click', (event) => {
                    const table = document.getElementById(data.supplier.id);
                    const today = new Date().toISOString().split('T')[0];
                    const fileName = prompt("Enter the file name", `table_${today}.xlsx`);
                    if (fileName) {
                        exportToExcel(table, fileName);
                        window.location.reload();
                    }
                });
                processTable(tableElement)
                changeDiv.appendChild(excelButton);
                document.body.appendChild(changeDiv)
                removeAndSumColumns(tableElement)
                document.body.appendChild(tableElement);

                document.body.appendChild(br2)
                document.body.appendChild(br3)
                document.body.appendChild(br4)
            })
            document.body.append(createPaginationElement(data.pagination))

        })
})

function createPaginationElement(Tables) {
    const paginationDiv = document.createElement('div');
    paginationDiv.classList.add('pagination');

    const stepLinksSpan = document.createElement('span');
    stepLinksSpan.classList.add('step-links');

    if (Tables.hasPrevious) {
        const firstLink = document.createElement('a');
        firstLink.href = '?page=1';
        firstLink.textContent = '« first';
        stepLinksSpan.appendChild(firstLink);

        const prevLink = document.createElement('a');
        prevLink.href = `?page=${Tables.previousPageNumber}`;
        prevLink.textContent = '‹ prev';
        stepLinksSpan.appendChild(prevLink);
    }

    const currentPageSpan = document.createElement('span');
    currentPageSpan.classList.add('current-page');
    currentPageSpan.textContent = `Page ${Tables.currentPageNumber} of ${Tables.totalPages}.`;

    stepLinksSpan.appendChild(currentPageSpan);

    if (Tables.hasNext) {
        const nextLink = document.createElement('a');
        nextLink.href = `?page=${Tables.nextPageNumber}`;
        nextLink.textContent = 'next ›';
        stepLinksSpan.appendChild(nextLink);

        const lastLink = document.createElement('a');
        lastLink.href = `?page=${Tables.totalPages}`;
        lastLink.textContent = 'last »';
        stepLinksSpan.appendChild(lastLink);
    }

    paginationDiv.appendChild(stepLinksSpan);
    console.log(paginationDiv);
    return paginationDiv;
}
