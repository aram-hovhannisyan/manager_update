
// Function to export table content to Excel and trigger download
function exportToExcel(table, fileName) {
  const tds = table.querySelectorAll('td')
  tds.forEach((td)=>{
    if(parseInt(td.textContent.trim()) === 0){
      td.innerText = ''
    }
  })
  const rows = table.querySelectorAll('tbody tr');
  const headerRow = table.querySelector('thead tr')
  const headers = table.querySelectorAll("thead tr th")
  headers.forEach((header)=>{
    if(header.style.display === 'none'){
      headerRow.removeChild(header)
    }
  })

  rows.forEach(row => {
    for (const el of row.children) {
      // console.log(el);
        if (el.style.display === 'none'){
          // console.log(el);
          row.removeChild(el)
        }
      }
    }
    )
    rows.forEach(row => {
      for (const el of row.children) {
        // console.log(el);
          if (el.style.display === 'none'){
            // console.log(el);
            row.removeChild(el)
          }
        }
      }
      )
    rows.forEach(row => {
        for (const el of row.children) {
          // console.log(el);
            if (el.style.display === 'none'){
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


