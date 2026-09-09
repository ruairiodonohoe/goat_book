console.log("lists.js loading");

const initialize = (inputSelector) => {
    console.log("initialize called");
    const textInput = document.querySelector(inputSelector);
    textInput.oninput = () => {
        textInput.classList.remove("is-invalid")
    };
}