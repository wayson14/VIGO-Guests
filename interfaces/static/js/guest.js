window.onload = start;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


function connect() {
    socket = new WebSocket("wss://" + window.location.host + "/ws/socket_connection/");

    socket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    socket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "socket_message":
                // chatLog.value += data.message + "\n";
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        // chatLog.scrollTop = chatLog.scrollHeight;
    };

    socket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        socket.close();
    }
}

var guest_first_name_wrong_string = "";
var guest_last_name_wrong_string = "";
var keeper_full_name_wrong_string = "";
var company_wrong_string = "";
var error_unauthorized_string = "";
var error_unknown_string = "";
var operation_successful_string = "";

function start()
{
    switch_to_ang();
    connect()
    let form = document.getElementById("add-form");
    form.addEventListener("submit", e => {e.preventDefault(); upload_data(form);});
}

function switch_to_pl()
{
    document.title = "Rejestracja gości";
    $("header span").html("REJESTRACJA GOŚCI");
    $(".container h1").html("Witamy w VIGO Photonics!")
    $(".container h2").html("Proszę podaj swoje dane:")
    $("#language span").html("Język: ")
    document.querySelector("[name='guest_first_name']").placeholder = "Imię";
    document.querySelector("[name='guest_last_name']").placeholder = "Nazwisko";
    document.querySelector("[name='keeper_full_name']").placeholder = "Opiekun";
    document.querySelector("[name='company']").placeholder = "Firma";
    document.querySelector("[name='submit']").value = "ZATWIERDŹ";
    guest_first_name_wrong_string = "Imię jest wymagane";
    guest_last_name_wrong_string = "Nazwisko jest wymagane";
    keeper_full_name_wrong_string = "Opiekun jest wymagany";
    company_wrong_string = "Firma jest wymagana";
    error_unauthorized_string = "403 Nieautoryzowany - spróbuj się ponownie zalogować do interfejsu gościa.";
    error_unknown_string = "Wystąpił nieznany błąd. Skontaktuj się z administratorami.";
    operation_successful_string = "Pomyślnie zarejestrowano wizytę. Poczekaj na wydanie identyfikatora...";
}

function switch_to_ang()
{
    document.title = "Guest registration";
    $("header span").html("GUEST REGISTRATION");
    $(".container h1").html("Welcome to VIGO Photonics")
    $(".container h2").html("Please enter your data:")
    $("#active-title").html("Currently present guests:")
    $("#language span").html("Language: ")
    document.querySelector("[name='guest_first_name']").placeholder = "First name";
    document.querySelector("[name='guest_last_name']").placeholder = "Last name";
    document.querySelector("[name='keeper_full_name']").placeholder = "Keeper";
    document.querySelector("[name='company']").placeholder = "Company";
    document.querySelector("[name='submit']").value = "ACCEPT";
    guest_first_name_wrong_string = "First name is required";
    guest_last_name_wrong_string = "Last name is required";
    keeper_full_name_wrong_string = "Keeeper is required";
    company_wrong_string = "Company is required";
    error_unauthorized_string = "403 Unauthorized - try to re-log to guest interface.";
    error_unknown_string = "Unknown error occured. Please conntact administration.";
    operation_successful_string = "Visitation registrated successfuly. Please wait to recive your idnetificator...";
}

async function upload_data(form)
{
    const guest_first_name = form.querySelector("[name='guest_first_name']");
    const guest_last_name = form.querySelector("[name='guest_last_name']");
    const keeper_full_name = form.querySelector("[name='keeper_full_name']");
    const company = form.querySelector("[name='company']");
    let output
    if(!validate(guest_first_name, guest_last_name, keeper_full_name, company)) return false;

    const endpoint = "/api/guest_entries";
    const formData = new FormData();
    formData.append("guest_first_name", guest_first_name.value);
    formData.append("guest_last_name", guest_last_name.value);
    formData.append("keeper_full_name", keeper_full_name.value);
    formData.append("company", company.value);
    formData.append("csrfmiddlewaretoken", csrftoken)
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
        socket.send(JSON.stringify({
            "message": "Reload event"
        }))
        $( "#output" ).css({"color":"green"})
        output = operation_successful_string
        $( "#output" ).text(output);
    }
    else{
        $( "#output" ).css({"color":"red"})
        if (response.status == 403){
            $( "#output" ).text(error_unauthorized_string);
        }
        $( "#output" ).text(error_unknown_string);
    }
    setTimeout(() => {
        guest_first_name.value = '',
        guest_last_name.value = '',
        keeper_full_name.value = '',
        company.value = ''
        $( "#output" ).text('');
    }, 3000)
}

function validate(guest_first_name, guest_last_name, keeper_full_name, company)
{
    let ok = true;
    if(guest_first_name.value == "")
    {
        guest_first_name.placeholder = guest_first_name_wrong_string;
        guest_first_name.className = "invaild";
        ok = false;
    }
    else
    {
        guest_first_name.placeholder = "Imię";
        guest_first_name.className = "";
    }
    if(guest_last_name.value == "")
    {
        guest_last_name.placeholder = guest_last_name_wrong_string;
        guest_last_name.className = "invaild";
        ok = false;
    }
    else
    {
        guest_last_name.placeholder = "Nazwisko";
        guest_last_name.className = "";
    }
    if(keeper_full_name.value == "")
    {
        keeper_full_name.placeholder = keeper_full_name_wrong_string;
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
        company.placeholder = company_wrong_string;
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