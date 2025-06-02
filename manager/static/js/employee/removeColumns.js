function handleRemoveButtonClick(supplierId) {
  let counter = 0;
  const table = document.getElementById(supplierId);
  const supTot = table.querySelectorAll('.supTotal');
  const headings = table.querySelectorAll('thead tr th');
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');
  const delChilds = [];

  for (let i = 0; i < headings.length - 1; i++) {
    headings[i].setAttribute('colspan', '1');
  }

  rows.forEach((row) => {
    const cols = row.querySelectorAll('td');
    cols.forEach((col, index) => {
      if (index % 2 == 0 && index !== 0) {
        delChilds.push({ col, row });
      }
    });
  });

  counter++;
  if (counter % 2) {
    delChilds.forEach((value) => {
      const delCol = value.col;
      delCol.style.display = 'none';
    });
  } else {
    headings.forEach((heading, index) => {
      if (index !== 0) {
        heading.setAttribute('colspan', '2');
      }
    });
    delChilds.forEach((value) => {
      const delCol = value.col;
      delCol.style.display = 'table-cell';
    });
  }

  supTot.forEach((el) => (el.style.display = counter % 2 ? 'block' : 'none'));
  removeAndSumColumns(supplierId)
}

function addIndexIfNotExists(index, arr) {
  if (!arr.includes(index)) {
    arr.push(index);
  }
}

function removeAndSumColumns(supID) {
  const table = document.getElementById(supID);
  const tbody = table.querySelector('tbody');
  const rows = tbody.querySelectorAll('tr');
  const lastRow = supID !== '129' ? tbody.lastElementChild : tbody.lastElementChild.previousSibling;
  const indicesToRemove = [];
  const removeList = [];

  rows.forEach((row) => {
    let ohanRow = row.querySelector('td[name="Օհան"]');
    let tdElements = row.querySelectorAll('td[name="Գ.ավագ"], td[name="Գ.4-րդ"], td[name="Արա"]');
    let headers = table.querySelectorAll('th[name="Գ.ավագ"], th[name="Գ.4-րդ"], th[name="Արա"]');

    let sum = Array.from(tdElements).reduce((accumulator, currentElement) => {
      let cellValue = parseFloat(currentElement.textContent.trim());
      if (!isNaN(cellValue)) {
        return accumulator + cellValue;
      }
      return accumulator;
    }, 0);

    tdElements.forEach((el) => {
      let index = Array.prototype.indexOf.call(row.cells, el);
      addIndexIfNotExists(index, indicesToRemove);
      el.style.display = 'none';
    });

    indicesToRemove.forEach((index) => {
      const cellToRemove = lastRow.cells[index];
      if (cellToRemove) {
        addIndexIfNotExists(cellToRemove, removeList);
      }
    });

    headers.forEach((el) => {
      el.style.display = 'none';
    });

    if (ohanRow) {
      ohanRow.textContent = parseInt(ohanRow?.textContent.trim() || 0) + sum;
    }

    let needAddingIndex = Array.prototype.indexOf.call(row.cells, ohanRow);
    let elementToAdd = lastRow.cells[needAddingIndex];
    let changeSum = 0;

    if (elementToAdd) {
      changeSum = parseInt(elementToAdd.textContent.trim() || 0);
    }

    removeList.forEach((el) => {
      let s = parseInt(el.textContent.trim() || 0);
      changeSum += s;
      el.style.display = 'none';
    });

    if (elementToAdd) {
      elementToAdd.textContent = changeSum;
    }
  });

  rows.forEach((row) => {
    let kamoRow = row.querySelector('td[name="Կամո"]');
    let tdElements = row.querySelectorAll('td[name="Գանձակ"], td[name="Սարուխան"]');
    let headers = table.querySelectorAll('th[name="Գանձակ"], th[name="Սարուխան"]');

    let sum = Array.from(tdElements).reduce((accumulator, currentElement) => {
      let cellValue = parseFloat(currentElement.textContent.trim());
      if (!isNaN(cellValue)) {
        return accumulator + cellValue;
      }
      return accumulator;
    }, 0);

    tdElements.forEach((el) => {
      let index = Array.prototype.indexOf.call(row.cells, el);
      addIndexIfNotExists(index, indicesToRemove);
      el.style.display = 'none';
    });

    indicesToRemove.forEach((index) => {
      const cellToRemove = lastRow.cells[index];
      if (cellToRemove) {
        addIndexIfNotExists(cellToRemove, removeList);
      }
    });

    headers.forEach((el) => {
      el.style.display = 'none';
    });

    if (kamoRow) {
      kamoRow.textContent = parseInt(kamoRow?.textContent.trim() || 0) + sum;
    }

    let needAddingIndex = Array.prototype.indexOf.call(row.cells, kamoRow);
    let elementToAdd = lastRow.cells[needAddingIndex];
    let changeSum = 0;

    if (elementToAdd) {
      changeSum = parseInt(elementToAdd.textContent.trim() || 0);
    }

    removeList.forEach((el) => {
      let s = parseInt(el.textContent.trim() || 0);
      changeSum += s;
      el.style.display = 'none';
    });

    if (elementToAdd) {
      elementToAdd.textContent = changeSum;
    }
  });
}
