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


function start()
{
    connect()
    let form = document.getElementById("add-form");
    form.addEventListener("submit", e => {e.preventDefault(); upload_data(form);});
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
        guest_first_name.placeholder = "Imię jest wymagane";
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
        guest_last_name.placeholder = "Nazwisko jest wymagane";
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