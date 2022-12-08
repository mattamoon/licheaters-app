function spin() {
const element = document.getElementById("loader");

if (element.className == "spinner-grow spinner-grow-sm loader"){
    element.className = "spinner-border spinner-border-sm";
    } else {
    element.className = "spinner-grow spinner-grow-sm loader";
    }
}
