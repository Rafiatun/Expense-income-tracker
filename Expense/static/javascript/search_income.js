const searchfieldincome=document.querySelector("#searchfieldincome");
const tabeloutput2=document.querySelector(".table-output2");
const apptable2=document.querySelector(".app-table2")
const pagination2=document.querySelector(".pagination-container")
const tbody2=document.querySelector(".table-body2")

tabeloutput2.style.display= "none";


searchfieldincome.addEventListener("keyup",(e)=>{
    const searchvalue=e.target.value;
    if (searchvalue.trim().length >0) 
    {
        pagination2.style.display="none";
        tbody2.innerHTML=" "
   
        fetch("/search_income",{
            body: JSON.stringify({ searchText:searchvalue }),
            method: "POST",
    
        })
        .then((res) => res.json())
        .then( data=> {
            console.log("data",data)
            apptable2.style.display="none";
            tabeloutput2.style.display="block";

            if (data.length==0){

                tabeloutput2.innerHTML="No results found"

            }else {
                data.forEach((item) => {

                    tbody2.innerHTML += `
                    <tr>
                    <td>${item.amount}</td>
                    <td>${item.source }</td>
                    <td>${item.description }</td>
                    <td>${item.date }</td>
                    </tr>
                    `
                    
                });
            
            }
            
        });

    } else {
        tabeloutput2.style.display="none"
        apptable2.style.display="block";
        pagination2.style.display="block"

    }
});



