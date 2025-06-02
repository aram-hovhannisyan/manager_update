let allWhite_tds = document.querySelectorAll('td')
let buuuts = document.querySelectorAll('#changeSend')

let x = () => {
allWhite_tds.forEach((td)=>{
    if(td.style.color === 'white' && parseInt(td.textContent.trim()) !== 0){
        td.style.color = 'rgb(20, 20, 20)';
    }
})}
buuuts.forEach((but)=>{
    but.addEventListener('click', x)
})
