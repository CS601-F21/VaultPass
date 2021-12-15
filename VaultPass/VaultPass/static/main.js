const wrapper = document.querySelector(".wrapper");

function displayModel(id){
    const model = document.getElementById(id);
    wrapper.style.display = "flex";
    model.style.display = "flex";
    console.info(model);

    const close = document.getElementById("close");
    close.addEventListener("click", ()=>{
        wrapper.style.display = "none";
        model.style.display = "none";
    })
}

const copy = document.querySelectorAll(".copy");
copy.forEach(c => {
    c.onclick = () => {
        let element = c.previousElementSibling;
        navigator.clipboard.writeText(element.value);
    }
})