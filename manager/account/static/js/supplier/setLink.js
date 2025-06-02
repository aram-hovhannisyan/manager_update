const allChangeItems = document.querySelectorAll('p');
const keys = [];
const allTds = document.querySelectorAll('td');
const linkElements = [];

allChangeItems.forEach((item) => {
    const key = item.getAttribute('key');
    if (key) {
        keys.push(key);
    }
});

allTds.forEach((td) => {
    const key = td.getAttribute('key');
    if (keys.includes(key)) {
        console.log(td)
        td.style.color = 'red';
        const link = document.createElement('a');
        link.href = `/account/endorse/${td.getAttribute('custId')}/`;
        td.addEventListener('click', function() {
            window.location.href = link.href; // Redirect to the link
        });
    }
});