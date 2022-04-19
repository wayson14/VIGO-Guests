window.onload = start;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var avalible_cards = [];

String.prototype.htmlEntities = function()
{
    return this.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function start()
{
    console.log("działa");
    refresh();
}

function auto_refresh()
{
    refresh();
    setTimeout(() => {
        auto_refresh();
    }, 3000);
}

function refresh()
{
    load_awaitings();
    load_active();
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
    info.innerHTML = "Imię: "+data["guest_first_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Opiekun: "+data["keeper_full_name"].htmlEntities();
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Nazwisko: "+data["guest_last_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Firma: "+data["company"].htmlEntities();
    infos.appendChild(info);

    entry.appendChild(infos);

    let interactions = document.createElement("div");
    interactions.className = "interactions col-12 col-xxl-6";

    let span = document.createElement("span");
    span.innerHTML = "Numer karty: ";
    interactions.appendChild(span);

    let div = document.createElement("div");
    let select = document.createElement("select");
    avalible_cards.forEach(card => {
        let option = document.createElement("option");
        option.innerHTML = card.id;
        option.value = card.id;
        select.appendChild(option);
    });
    interactions.appendChild(select);

    let button = document.createElement("button");
    button.addEventListener("click", function(){accept(data["id"]);});
    button.innerHTML = "ZATWIERDŹ";
    interactions.appendChild(button);

    button = document.createElement("button");
    button.addEventListener("click", function(){decline(data["id"]);});
    button.innerHTML = "ODRZUĆ";
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
    info.innerHTML = "Imię: "+data["guest_first_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Opiekun: "+data["keeper_full_name"].htmlEntities();
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Nazwisko: "+data["guest_last_name"].htmlEntities();
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Firma: "+data["company"].htmlEntities();
    infos.appendChild(info);

    clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Numer karty: "+data["card"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Data wejścia: "+data["enter_datetime"];
    infos.appendChild(info);

    entry.appendChild(infos);

    let interactions = document.createElement("div");
    interactions.className = "interactions col-12 col-lg-4";

    let button = document.createElement("button");
    button.addEventListener("click", function(){release(data["id"]);});
    button.innerHTML = "ZWOLNIJ";
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
            output = "Operacja wykonana pomyślnie"
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
            output = "Operacja wykonana pomyślnie"
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
            $("#output").text('');
        }, 5000);
    }
    if(response.ok)
    {
        return await response.json();
    }
   else return "";
}