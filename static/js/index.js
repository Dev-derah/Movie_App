const slides = document.querySelectorAll(".discover-container");
const movies = document.querySelectorAll(".movie-card");

function addId(params) {
    for (let index = 0; index < slides.length; index++) {
        const element = slides[index];
        element.setAttribute("id", "slide" + [index]);
    }
}
addId();