const usernamefield=document.querySelector("#usernamefield");
const feedback =document.querySelector(".invalid-feedback");
const emailfield=document.querySelector("#emailfield");
const emailfeedback =document.querySelector(".emailarea");
const usernamesuccessoutput=document.querySelector(".usernamesuccessoutput");
const passtoggole=document.querySelector(".showpasswordtoggle")
const passwordfield=document.querySelector("#passwordfield")
const submit=document.querySelector(".submit-btn")


const handleToggler=(e)=>{

    if(passtoggole.textContent==='Show'){
        passtoggole.textContent="Hide";

        passwordfield.setAttribute("type", "password");

    }else {
        passtoggole.textContent='Show';
        passwordfield.setAttribute("type", "text");

    }
    
}

passtoggole.addEventListener("click",handleToggler)

emailfield.addEventListener("keyup" , (e) => {
    const emailvalue=e.target.value;

    emailfield.classList.remove("is-invalid");
    emailfeedback.style.display="none";

    if (emailvalue.length>0){

        fetch('/validateemail' , {
            body:JSON.stringify({ email:emailvalue }),
            method:"POST",
        })
        .then((res) => res.json())
        .then(data=> 
            {
                console.log("data", data);
                if(data.email_error){
                    emailfield.classList.add("is-invalid");
                    emailfeedback.style.display="block";
                    emailfeedback.innerHTML= `
                     <p> ${data.email_error}</p>
                      `
                    submit.disabled = true;
                }else{
                    submit.removeAttribute("disabled");
                }
    
            });

    }
    
        console.log('emailvalue',emailvalue)
})




usernamefield.addEventListener("keyup", (e) =>{
    const usernameVal=e.target.value;

    usernamefield.classList.remove("is-invalid");
    feedback.style.display="none";
    usernamesuccessoutput.style.display="block";
    usernamesuccessoutput.textContent=`Checking ${usernameVal}`

    if (usernameVal.length>0){
        fetch('/validateusername',{
            body: JSON.stringify({ username:usernameVal }),
            method: "POST",
    
        })
        .then((res) => res.json())
        .then( data=> {
            console.log("data", data);
            usernamesuccessoutput.style.display="none";
            if(data.username_error){
                usernamefield.classList.add("is-invalid");
                feedback.style.display="block";
                feedback.innerHTML= `
                 <p> ${data.username_error}</p>
                  `
                submit.disabled = true;
            }else {
                submit.removeAttribute("disabled");
            }

        });

    }

    
    console.log('usernameVal',usernameVal)
});