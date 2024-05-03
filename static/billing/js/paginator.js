let pageNumbers = document.getElementsById("page-number-selector");

// get total pages from backend and populate
function pageNumbers(){
    fetch('/billing/api/get-items/?total_pages=true')
        .then(response => response.json())
        .then(data => {
            let totalPages = data.total_pages;
            for(let i = 1; i <= totalPages; i++){
                let option = document.createElement("option");
                option.value = i;
                option.text = i;
                pageNumbers.appendChild(option);
            }
        });
}
pageNumbers();

function previousPage(){
    var page = parseInt(document.getElementById("page").value);
    if(page > 1){
        document.getElementById("page").value = page - 1;
        document.getElementById("form").submit();
    }
}

function nextPage(){
    let page = parseInt(document.getElementById("page").value);

}