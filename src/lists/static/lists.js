console.log("lists.js loading");

const initialize = (inputSelector, errorSelector) => {
    console.log("initialize called");
    const textInput = document.querySelector(inputSelector);
    textInput.oninput = () => {
        const errorMsg = document.querySelector(errorSelector);
        errorMsg.style.display = "none";
    };
}
