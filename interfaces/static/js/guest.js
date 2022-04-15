window.onload = start;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function start()
{
    let form = document.getElementById("add-form");
    form.addEventListener("submit", e => {e.preventDefault(); upload_data(form);});
}

async function upload_data(form)
{
    const guest_full_name = form.querySelector("[name='guest_full_name']");
    const lastname = form.querySelector("[name='lastname']");
    const keeper_full_name = form.querySelector("[name='keeper_full_name']");
    const company = form.querySelector("[name='company']");
    let output
    if(!validate(guest_full_name, lastname, keeper_full_name, company)) return false;

    const endpoint = "/api/guest_entries";
    const formData = new FormData();
    formData.append("guest_full_name", guest_full_name.value);
    // formData.append("lastname", lastname.value);
    formData.append("keeper_full_name", keeper_full_name.value);
    formData.append("company", company.value);
    console.log(formData);
    const response = await fetch(endpoint,
         {
            method: "post",
            body: formData,
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
        }
        ).catch(console.error);
    const data = await response.json()
    if (response.ok){
        $( "#output" ).css({"color":"green"})
        output = "Pomyślnie zarejestrowano wizytę. Poczekaj na wydanie identyfikatora..."
        $( "#output" ).text(output);
    }
    else{
        $( "#output" ).css({"color":"red"})
        if (response.status == 403){
            $( "#output" ).text(`403 Nieautoryzowany - spróbuj się ponownie zalogować do interfejsu gościa.`);
        }
        $( "#output" ).text(`Wystąpił nieznany błąd. Skontaktuj się z administratorami.`);
    }
    setTimeout(() => {
        guest_full_name.value = '',
        keeper_full_name.value = '',
        lastname.value = '',
        company.value = ''
        $( "#output" ).text('');
    }, 5000)
}

function validate(guest_full_name, lastname, keeper_full_name, company)
{
    let ok = true;
    if(guest_full_name.value == "")
    {
        guest_full_name.placeholder = "Imię jest wymagane";
        guest_full_name.className = "invaild";
        ok = false;
    }
    else
    {
        guest_full_name.placeholder = "Imię";
        guest_full_name.className = "";
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
    if(keeper_full_name.value == "")
    {
        keeper_full_name.placeholder = "Opiekun jest wymagany";
        keeper_full_name.className = "invaild";
        ok = false;
    }
    else
    {
        keeper_full_name.placeholder = "Opiekun";
        keeper_full_name.className = "";
    }
    if(company.value == "")
    {
        company.placeholder = "Frima jest wymagana";
        company.className = "invaild";
        ok = false;
    }
    else
    {
        company.placeholder = "Firma";
        company.className = "";
    }
    if(!ok) return false;
    return true;
}