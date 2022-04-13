window.onload = start;

function start()
{
    console.log("działa");
    test = {
        "id": 456,
        "firstname": "Mateusz",
        "lastname": "Ogniewski",
        "keeper": "Arkadiusz Szydlik",
        "brand": "VIGO photonics",
        "card_id": 34
    };
    document.getElementById("awaiting").appendChild(new_active_entry(test));
}

function refresh()
{
    load_awaitings();
    load_active();
}

async function load_awaitings()
{
    let endpoint = "load_possible_guests.py"
    response = await fetch(endpoint).catch(console.error);
    response = await response.json();

    let awaitings = document.getElementById("awaitings");
    awaitings.innerHTML = "";
    response.forEach(entry => {
        awaitings.appendChild(new_awaiting_entry(entry));
    });
}

async function load_active()
{
    let endpoint = "load_active_guests.py"
    response = await fetch(endpoint).catch(console.error);
    response = await response.json();

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
    info.innerHTML = "Imię: "+data["firstname"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Opiekun: "+data["keeper"];
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Nazwisko: "+data["lastname"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Firma: "+data["brand"];
    infos.appendChild(info);

    entry.appendChild(infos);

    let interactions = document.createElement("div");
    interactions.className = "interactions col-12 col-xxl-6";

    let span = document.createElement("span");
    span.innerHTML = "Numer karty: ";
    interactions.appendChild(span);

    let input = document.createElement("input");
    input.type = "number";
    input.value = data["card_id"];
    input.placeholder = "id";
    interactions.appendChild(input);

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
    info.innerHTML = "Imię: "+data["firstname"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Opiekun: "+data["keeper"];
    infos.appendChild(info);

    let clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Nazwisko: "+data["lastname"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Firma: "+data["brand"];
    infos.appendChild(info);

    clearboth = document.createElement("div");
    clearboth.style = "clear: both;";
    infos.appendChild(clearboth);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Numer karty: "+data["card_id"];
    infos.appendChild(info);

    info = document.createElement("div");
    info.className = "info";
    info.innerHTML = "Data wejścia: "+data["enter_date"];
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
    let endpoint = "add_guest.py";
    let formData = new FormData();
    formData.append("accept", accept);
    formData.append("id", id);
    formData.append("card_id", $("[name="+id+"] input").value);
    response = await fetch(endpoint, {method:"post", body: formData}).catch(console.error);
    $("#output").html(response.json());
}

async function release(id)
{
    let endpoint = "release_card.py";
    let formData = new FormData();
    formData.append("id", id);
    response = await fetch(endpoint, {method:"post", body: formData}).catch(console.error);
    $("#output").html(response.json());
}