window.onload = start;

function start()
{
    let form = document.getElementById("add-form");
    form.addEventListener("submit", e => {e.preventDefault(); upload_data(form);});
}

async function upload_data(form)
{
    let firstname = form.querySelector("[name='firstname']");
    let lastname = form.querySelector("[name='lastname']");
    let keeper = form.querySelector("[name='keeper']");
    let brand = form.querySelector("[name='brand']");
    
    if(!validate(firstname, lastname, keeper)) return false;

    let endpoint = "add_possible_guest.py";
    let formData = new FormData();
    formData.append("firstname", firstname.value);
    formData.append("lastname", lastname.value);
    formData.append("keeper", keeper.value);
    formData.append("brand", brand.value);
    console.log(formData);
    response = await fetch(endpoint, {method:"post", body: formData}).catch(console.error);
    $("#output").html(response.json());
}

function validate(firstname, lastname, keeper)
{
    let ok = true;
    if(firstname.value == "")
    {
        firstname.placeholder = "Imię jest wymagane";
        firstname.className = "invaild";
        ok = false;
    }
    else
    {
        firstname.placeholder = "Imię";
        firstname.className = "";
    }
    if(lastname.value == "")
    {
        lastname.placeholder = "Nazwisko jest wymagane";
        lastname.className = "invaild";
        ok = false;
    }
    else
    {
        lastname.placeholder = "Nazwisko";
        lastname.className = "";
    }
    if(keeper.value == "")
    {
        keeper.placeholder = "Opiekun jest wymagany";
        keeper.className = "invaild";
        ok = false;
    }
    else
    {
        keeper.placeholder = "Opiekun";
        keeper.className = "";
    }
    if(!ok) return false;
    return true;
}