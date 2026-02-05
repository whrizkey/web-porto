/* Main Application Script */

// Change navbar when scrolling
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu
const mobileBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');

if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
}

// Carousel Functionality
const carouselTrack = document.querySelector('.carousel-track');
const carouselPrev = document.querySelector('.carousel-prev');
const carouselNext = document.querySelector('.carousel-next');
const carouselDots = document.querySelectorAll('.carousel-dots .dot');
const projectCards = document.querySelectorAll('.carousel-track .project-card-link');

let currentIndex = 0;
const totalProjects = projectCards.length;

function updateCarousel() {
    // Calculate offset
    const cardWidth = 440;
    const gap = 32; // 2rem
    const offset = currentIndex * (cardWidth + gap);

    // Move carousel
    carouselTrack.style.transform = `translateX(-${offset}px)`;

    // Update active card
    projectCards.forEach((card, index) => {
        if (index === currentIndex) {
            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    });

    // Update dots
    carouselDots.forEach((dot, index) => {
        if (index === currentIndex) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

// Next button
if (carouselNext) {
    carouselNext.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalProjects;
        updateCarousel();
    });
}

// Previous button
if (carouselPrev) {
    carouselPrev.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalProjects) % totalProjects;
        updateCarousel();
    });
}

// Dots navigation
carouselDots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentIndex = index;
        updateCarousel();
    });
});

// Touch/Swipe support for mobile
let touchStartX = 0;
let touchEndX = 0;

if (carouselTrack) {
    carouselTrack.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    carouselTrack.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        if (touchEndX < touchStartX - swipeThreshold) {
            // Swipe left - next
            currentIndex = (currentIndex + 1) % totalProjects;
            updateCarousel();
        }
        if (touchEndX > touchStartX + swipeThreshold) {
            // Swipe right - previous
            currentIndex = (currentIndex - 1 + totalProjects) % totalProjects;
            updateCarousel();
        }
    }
}

// Initialize carousel on load
if (projectCards.length > 0) {
    updateCarousel();
}
