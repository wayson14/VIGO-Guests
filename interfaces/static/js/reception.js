window.onload = start;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

function start()
{
    console.log("działa");
    test = {
        "id": 456,
        "guest_first_name": "Mateusz",
        "guest_last_name": "Ogniewski",
        "keeper_full_name": "Arkadiusz Szydlik",
        "company": "VIGO photonics",
        "card": 34,
        "cards": [1,2,3,4,5,6,7,8,9,45,34]
    };
    $("#awaiting").html(new_awaiting_entry(test));
    //refresh();
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
    let endpoint = "/api/"
    response = await get(endpoint, new FormData());
    if(response == "") return

    let awaitings = document.getElementById("awaitings");
    awaitings.innerHTML = "";
    response.forEach(entry => {
        awaitings.appendChild(new_awaiting_entry(entry));
    });
}

async function load_active()
{
    let endpoint = "/api/"
    response = await get(endpoint, new FormData());
    if(response == "") return

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
    entry.name = data["id"];

    let infos = document.createElement("div");
    infos.className = "infos col-12 col-xxl-6";

    let info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Imię: "+data["guest_first_name"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Opiekun: "+data["keeper_full_name"];
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Nazwisko: "+data["guest_last_name"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Firma: "+data["company"];
    infos.appendChild(info);

    entry.appendChild(infos);

    let interactions = document.createElement("div");
    interactions.className = "interactions col-12 col-xxl-6";

    let span = document.createElement("span");
    span.innerHTML = "Numer karty: ";
    interactions.appendChild(span);

    let select = document.createElement("select");
    data["cards"].forEach(card => {
        let option = document.createElement("option");
        option.innerHTML = card;
        select.appendChild(option);
    });
    select.value = data["card"];
    interactions.appendChild(select);

    let button = document.createElement("button");
    button.addEventListener("click", function(){accept(data["id"], true);});
    button.innerHTML = "ZATWIERDŹ";
    interactions.appendChild(button);

    button = document.createElement("button");
    button.addEventListener("click", function(){accept(data["id"], false);});
    button.innerHTML = "ODRZUĆ";
    interactions.appendChild(button);

    entry.appendChild(interactions);

    return entry;
}

function new_active_entry(data)
{
    let entry = document.createElement("div");
    entry.className = "entry active";
    entry.name = data["id"];

    let infos = document.createElement("div");
    infos.className = "infos col-12 col-lg-8";

    let info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Imię: "+data["guest_first_name"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Opiekun: "+data["keeper_full_name"];
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Nazwisko: "+data["guest_last_name"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Firma: "+data["company"];
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

async function accept(id, accept)
{
    const endpoint = "/api/";
    let formData = new FormData();
    formData.append("accept", accept);
    formData.append("id", id);
    formData.append("card_id", $("[name="+id+"] select").value);
    response = await get(endpoint, formData)
    $("#output").html(response.json());
    refresh();
}

async function release(id)
{
    const endpoint = "/api/";
    let formData = new FormData();
    formData.append("id", id);
    response = await get(endpoint, formData)
    $("#output").html(response.json());
    refresh();
}

async function get(endpoint, formData)
{
    const response = await fetch(endpoint,
        {
           method: "post",
           body: formData,
           headers: {'X-CSRFToken': csrftoken},
           mode: 'same-origin',
       }
       ).catch(console.error);
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
   if(response.ok) return await response.json();
   return "";
}