let pageNumbers = document.getElementById("page-number-selector");
let uri = window.location.pathname;

// get total pages from backend and populate
function totalPages(){
    let link = "";
    if(uri.includes("items")){
        link = "/billing/api/get-items";
    } else if(uri.includes("bills")){
        link = "/billing/api/view-bills";
    }
    fetch(link)
        .then(response => response.json())
        .then(data => {
            let length = data.length;
            let totalPages = data[length - 1];
            for(let i = 1; i <= totalPages; i++){
                let option = document.createElement("option");
                option.value = i;
                option.text = i;
                pageNumbers.appendChild(option);
            }
        });
}
totalPages();

pageNumbers.addEventListener('change', function(){
    if(uri.includes("items")){
        items(pageNumbers.value);
    } else if(uri.includes("bills")){
        bills(pageNumbers.value);
    }
});

function previousPage(){
    if(pageNumbers.value > 1){
        if(uri.includes("items")){
            items(+pageNumbers.value - 1);
        } else if(uri.includes("bills")){
            bills(+pageNumbers.value - 1);
        }
        pageNumbers.value = parseInt(pageNumbers.value) - 1;
    }
}

function nextPage(){
    if(pageNumbers.value < pageNumbers.options.length){
        if(uri.includes("items")){
            items(+pageNumbers.value + 1);
        } else if(uri.includes("bills")){
            bills(+pageNumbers.value + 1);
        }
        pageNumbers.value = parseInt(pageNumbers.value) + 1;
    }
}