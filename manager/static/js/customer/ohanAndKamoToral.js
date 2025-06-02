const manins = document.querySelectorAll('.mainItems')
const others = document.querySelectorAll('.otherItmes')

const cellForMain = document.querySelector('.mainTotal')
const cellForOther = document.querySelector('.otherTotal')

manins.forEach((td)=>{
    let sum =  parseInt(td.textContent.trim()) || 0
    cellForMain.textContent = parseInt(cellForMain.textContent.trim()) + sum
});

others.forEach((td)=>{
    let sum =  parseInt(td.textContent.trim()) || 0
    cellForOther.textContent = parseInt(cellForOther.textContent.trim()) + sum
});


const total = cellForOther.nextSibling.nextSibling
total.textContent = parseInt(cellForMain.textContent.trim()) + parseInt(cellForOther.textContent.trim())