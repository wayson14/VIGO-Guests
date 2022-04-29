window.onload = start;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var avalible_cards = [];


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
                if (data.message === 'Reload event'){
                    refresh()
                }
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

String.prototype.htmlEntities = function()
{
    return this.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function start()
{
    connect();
    refresh();
    switch_to_ang();
}


function refresh()
{
    load_awaitings();
    load_active();
}

var guest_first_name_string = "";
var guest_last_name_string = "";
var keeper_full_name_string = "";
var company_string = "";
var card_string = "";
var enter_datetime_string = "";
var accept_button_string = "";
var decline_button_string = "";
var release_button_string = "";
var error_unauthorized_string = "";
var error_unknown_string = "";
var operation_successful_string = "";


function switch_to_pl()
{
    document.title = "Rejestracja gości";
    $("header span").html("REJESTRACJA GOŚCI");
    $("#topbar a").html("Wyloguj")
    $("#awaiting-title").html("Oczekujący na przydzielenie karty:")
    $("#active-title").html("Lista przydzielonych kart:")
    $("#language span").html("Język: ")
    guest_first_name_string = "Imię: ";
    guest_last_name_string = "Nazwisko: ";
    keeper_full_name_string = "Opiekun: ";
    company_string = "Firma: ";
    card_string = "Numer karty: ";
    enter_datetime_string = "Data wejścia: ";
    accept_button_string = "ZATWIERDŹ";
    decline_button_string = "ODRZUĆ";
    release_button_string = "ZWOLNIJ";
    error_unauthorized_string = "403 Nieautoryzowany - spróbuj się ponownie zalogować do interfejsu recepcji.";
    error_unknown_string = "Wystąpił nieznany błąd. Skontaktuj się z administratorami.";
    operation_successful_string = "Operacja wykonana pomyślnie";
}

function switch_to_ang()
{
    document.title = "Guest registration";
    $("header span").html("GUEST REGISTRATION");
    $("#topbar a").html("Log out")
    $("#awaiting-title").html("Guests awaiting for card assignment:")
    $("#active-title").html("Currently present guests:")
    $("#language span").html("Language: ")
    guest_first_name_string = "First name: ";
    guest_last_name_string = "Last name: ";
    keeper_full_name_string = "Keeper: ";
    company_string = "Company: ";
    card_string = "Card id: ";
    enter_datetime_string = "Enter date: ";
    accept_button_string = "ACCEPT";
    decline_button_string = "DECLINE";
    release_button_string = "RELEASE";
    error_unauthorized_string = "403 Unauthorized - try to re-log to reception interface.";
    error_unknown_string = "Unknown error occured. Please conntact administration.";
    operation_successful_string = "Operation executed successfuly";
}

async function load_awaitings()
{
    let endpoint = "/api/free_cards";
    let response = await get(endpoint, true);
    let initial_text = "";
    if(response == "")
    {
        initial_text = "<span style='color: red; font-weight: bold;'>Brak dostępnych kart do wydania.<br/>Dodaj więcej kart lub zwolnij te nieużywane.</span>";
        avalible_cards = [];
    }

    else avalible_cards = response;

    endpoint = "/api/no_cards_guests";
    response = await get(endpoint, true);

    let awaitings = document.getElementById("awaiting");
    awaitings.innerHTML = initial_text;
    response.forEach(entry => {
        awaitings.appendChild(new_awaiting_entry(entry));
    });
}

async function load_active()
{
    let endpoint = "/api/active_guest_entries"
    response = await get(endpoint, true);

    let active = document.getElementById("active");
    active.innerHTML = "";
    response.forEach(entry => {
        active.appendChild(new_active_entry(entry));
    });
}

function new_awaiting_entry(data)
{
    let entry = document.createElement("div");
    entry.className = "entry awaiting";
    entry.id = "entry-"+data["id"];

    let infos = document.createElement("div");
    infos.className = "infos col-12 col-xxl-6";

    let info = document.createElement("div");
    info.className = "info";
    info.innerHTML = guest_first_name_string+data["guest_first_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = keeper_full_name_string+data["keeper_full_name"].htmlEntities();
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = guest_last_name_string+data["guest_last_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = company_string+data["company"].htmlEntities();
    infos.appendChild(info);

    entry.appendChild(infos);

    let interactions = document.createElement("div");
    interactions.className = "interactions col-12 col-xxl-6";

    let span = document.createElement("span");
    span.innerHTML = card_string;
    interactions.appendChild(span);

    let div = document.createElement("div");
    let select = document.createElement("select");
    avalible_cards.filter(card => card.id !== -1).sort((a, b) => {        return a - b
    }).forEach(card => {
        let option = document.createElement("option");
        option.innerHTML = card.id;
        option.value = card.id;
        select.appendChild(option);
    });
    interactions.appendChild(select);

    let button = document.createElement("button");
    button.addEventListener("click", function(){accept(data["id"]);});
    button.innerHTML = accept_button_string;
    interactions.appendChild(button);

    button = document.createElement("button");
    button.addEventListener("click", function(){decline(data["id"]);});
    button.innerHTML = decline_button_string;
    interactions.appendChild(button);

    entry.appendChild(interactions);

    return entry;
}

function new_active_entry(data)
{
    let entry = document.createElement("div");
    entry.className = "entry active";
    entry.id = "entry-"+data["id"];

    let infos = document.createElement("div");
    infos.className = "infos col-12 col-lg-8";

    let info = document.createElement("div");
    info.className = "info";
    info.innerHTML = guest_first_name_string+data["guest_first_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = keeper_full_name_string+data["keeper_full_name"].htmlEntities();
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = guest_last_name_string+data["guest_last_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = company_string+data["company"].htmlEntities();
    infos.appendChild(info);

    clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = card_string+data["card"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = enter_datetime_string+data["enter_datetime"];
    infos.appendChild(info);

    entry.appendChild(infos);

    let interactions = document.createElement("div");
    interactions.className = "interactions col-12 col-lg-4";

    let button = document.createElement("button");
    button.addEventListener("click", function(){release(data["id"]);});
    button.innerHTML = release_button_string;
    interactions.appendChild(button);

    entry.appendChild(interactions);

    return entry;
}

async function accept(id)
{
    let endpoint = "/api/guest_entries/"+id+"/give_card/"+document.querySelector("#entry-"+id+" select").value;
    document.getElementById("awaiting").removeChild(document.querySelector("#entry-"+id));
    response = await get(endpoint);
    refresh();
}

async function decline(id)
{
    let endpoint = "/api/guest_entries/"+id+"/discard_entry";
    document.getElementById("awaiting").removeChild(document.querySelector("#entry-"+id));
    response = await del(endpoint);
}

async function release(id)
{
    let endpoint = "/api/guest_entries/"+id+"/close_entry";
    document.getElementById("active").removeChild(document.querySelector("#entry-"+id));
    response = await get(endpoint);
    refresh();
}

async function get(endpoint, quiet=false)
{
    const response = await fetch(endpoint,
        {
           method: "get",
           headers: {'X-CSRFToken': csrftoken},
           mode: 'same-origin',
       }
       ).catch(console.error);
    if(!quiet)
    {
        if (response.ok){
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
            $("#output").text('');
        }, 5000);
    }
    if(response.ok)
    {
        return await response.json();
    }
   else return "";
}

async function del(endpoint, quiet=false)
{
    const response = await fetch(endpoint,
        {
           method: "delete",
           headers: {'X-CSRFToken': csrftoken},
           mode: 'same-origin',
       }
       ).catch(console.error);
    if(!quiet)
    {
        if (response.ok){
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
            $("#output").text('');
        }, 5000);
    }
    if(response.ok)
    {
        return await response.json();
    }
   else return "";
}