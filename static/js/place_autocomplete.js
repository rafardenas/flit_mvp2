
const origen = document.getElementById("id_origen");
const options = {
    componentRestrictions: { country: "mx" },
    fields: ["address_components", "geometry", "icon", "name"],
};
const autocomplete = new google.maps.places.Autocomplete(origen, options);
autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
});

const destino = document.getElementById("id_destino");
const options2 = {
    componentRestrictions: { country: "mx" },
    fields: ["address_components", "geometry", "icon", "name"],
};
const autocomplete2 = new google.maps.places.Autocomplete(destino, options2);
autocomplete2.addListener("place_changed", () => {
    const place2 = autocomplete.getPlace();
});