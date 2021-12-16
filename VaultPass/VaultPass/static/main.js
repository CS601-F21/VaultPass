const wrapper = document.querySelector(".wrapper");

function displayModel(id){
    const model = document.getElementById(id);
    const container = document.querySelector(".container")
    wrapper.style.display = "flex";
    model.style.display = "flex";
    container.style.display = "none";
    

    const close = document.getElementById("close");
    close.addEventListener("click", ()=>{
        wrapper.style.display = "none";
        model.style.display = "none";
        document.querySelector("header").style.display = "unset";
        container.style.display = "grid"
    })
    document.querySelector("header").style.display = "none";
}

const copy = document.querySelectorAll(".copy");
copy.forEach(c => {
    c.onclick = () => {
        let element = c.previousElementSibling;
        navigator.clipboard.writeText(element.value);
    }
})