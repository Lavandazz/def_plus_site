    // Карусель работников Swiper.js
document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".swiper", {
        loop: true,
        centeredSlides: true, // Центрирует слайды
        slidesPerView: 1, // Показывать один слайд полностью
        spaceBetween: 10, // Расстояние между слайдами
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        effect: "coverflow",
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2.5,
            slideShadows: false,
        },
    });
});