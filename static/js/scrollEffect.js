document.addEventListener("DOMContentLoaded", function () {
    const fadeInElements = document.querySelectorAll(".fade-in");

    if (fadeInElements.length === 0) {
        console.log("Элементы с классом .fade-in не найдены");
    } else {
        console.log("Элементы с классом .fade-in найдены");
    }

    function checkVisibility() {
        fadeInElements.forEach((item) => {
            const rect = item.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            if (rect.top < windowHeight * 0.85 && rect.bottom > 0) {
                item.classList.add("show");
            } else {
                item.classList.remove("show");
            }
        });
    }

    window.addEventListener("scroll", checkVisibility);
    checkVisibility();
});


// document.addEventListener("DOMContentLoaded", function () {
//     let fadeElements = document.querySelectorAll(".fade-in");
//
//     function checkPosition() {
//         fadeElements.forEach(el => {
//             let position = el.getBoundingClientRect().top;
//             if (position < window.innerHeight - 50) {
//                 el.classList.add("show");
//             }
//         });
//     }
//
//     window.addEventListener("scroll", checkPosition);
//     checkPosition(); // Чтобы сразу применилось при загрузке
// });

