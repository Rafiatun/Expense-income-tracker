const searchfield=document.querySelector("#searchfield");
const tabeloutput=document.querySelector(".table-output");
const apptable=document.querySelector(".app-table")
const pagination=document.querySelector(".pagination-container")
const tbody=document.querySelector(".table-body")

tabeloutput.style.display= "none";


searchfield.addEventListener("keyup",(e)=>{
    const searchvalue=e.target.value;
    if (searchvalue.trim().length >0) 
    {
        pagination.style.display="none";
        tbody.innerHTML=" "
   
        fetch("/search_expense",{
            body: JSON.stringify({ searchText:searchvalue }),
            method: "POST",
    
        })
        .then((res) => res.json())
        .then( data=> {
            console.log("data",data)
            apptable.style.display="none";
            tabeloutput.style.display="block";

            if (data.length==0){

                tabeloutput.innerHTML="No results found"

            }else {
                data.forEach((item) => {

                    tbody.innerHTML += `
                    <tr>
                    <td>${item.amount}</td>
                    <td>${item.category }</td>
                    <td>${item.description }</td>
                    <td>${item.date }</td>
                    </tr>
                    `
                    
                });
            
            }
            
        });

    } else {
        tabeloutput.style.display="none"
        apptable.style.display="block";
        pagination.style.display="block"

    }
});



