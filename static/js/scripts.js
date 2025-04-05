document.addEventListener("DOMContentLoaded", function() {
    // Анимация для главной страницы (если есть соответствующие элементы)
    if (document.querySelector('.fade-in-item-left')) {
        const leftItems = document.querySelectorAll('.fade-in-item-left');
        leftItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('visible');
            }, 300 * (index + 1));
        });

      // Анимация для ВСЕХ hero-container
        const heroContainers = document.querySelectorAll('.fade-in-delay');
        heroContainers.forEach((container, index) => {
            setTimeout(() => {
                container.classList.add('visible');
            }, 800 + 100 * index); // Задержка: 0.8s + 0.3s для каждого следующего
        });

        const rightItems = document.querySelectorAll('.fade-in-item-right');
        rightItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('visible');
            }, 1000 + 300 * index);
        });
    }

    // Скролл-эффект для других страниц
    const fadeInElements = document.querySelectorAll(".fade-in");
    if (fadeInElements.length > 0) {
        function checkVisibility() {
            fadeInElements.forEach((item) => {
                const rect = item.getBoundingClientRect();
                if (rect.top < window.innerHeight * 0.85 && rect.bottom > 0) {
                    item.classList.add("show");
                } else {
                    item.classList.remove("show");
                }
            });
        }
        window.addEventListener("scroll", checkVisibility);
        checkVisibility();
    }
});

// document.addEventListener("DOMContentLoaded", function() {
//     // Анимация первой строки
//     const leftItems = document.querySelectorAll('.fade-in-item-left');
//     leftItems.forEach((item, index) => {
//         setTimeout(() => {
//             item.classList.add('visible');
//         }, 300 * (index + 1));
//     });
//
//     // Анимация hero-container (появляется после первого stats-container)
//     setTimeout(() => {
//         const heroContainer = document.querySelector('.fade-in-delay');
//         if (heroContainer) {
//             heroContainer.classList.add('visible');
//         }
//     }, 800); // Запускаем через 1200ms после начала
//
//     // Анимация второй строки (начинается после первой)
//     const rightItems = document.querySelectorAll('.fade-in-item-right');
//     rightItems.forEach((item, index) => {
//         setTimeout(() => {
//             item.classList.add('visible');
//         }, 1000 + 300 * index); // 900ms = задержка после первой строки
//     });
// });