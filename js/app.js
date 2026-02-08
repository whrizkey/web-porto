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

// Scroll Reveal Animations
const revealElements = document.querySelectorAll('.scroll-reveal');

function checkScroll() {
    revealElements.forEach(el => {
        const elementTop = el.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;

        if (elementTop < windowHeight * 0.85) {
            el.classList.add('revealed');
        }
    });
}

// Check on scroll and load
window.addEventListener('scroll', checkScroll);
window.addEventListener('load', checkScroll);

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Interactive Particle System
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Mouse position
let mouse = {
    x: null,
    y: null,
    radius: 150 // Area of effect around mouse
};

window.addEventListener('mousemove', (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
});

// Particle class
class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.baseX = this.x;
        this.baseY = this.y;
        this.density = (Math.random() * 30) + 1;
        this.speedX = (Math.random() - 0.5) * 0.5;
        this.speedY = (Math.random() - 0.5) * 0.5;

        // Color variations (orange theme only)
        const colors = ['#FF6B35', '#FF8555', '#FF9F70'];
        this.color = colors[Math.floor(Math.random() * colors.length)];
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();

        // Add glow effect
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
    }

    update() {
        // Gentle floating motion
        this.x += this.speedX;
        this.y += this.speedY;

        // Mouse interaction - particles get pushed away
        if (mouse.x != null && mouse.y != null) {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < mouse.radius) {
                let force = (mouse.radius - distance) / mouse.radius;
                let directionX = dx / distance;
                let directionY = dy / distance;

                // Push away from mouse
                this.x -= directionX * force * 3;
                this.y -= directionY * force * 3;
            }
        }

        // Slowly return to base position
        this.x += (this.baseX - this.x) * 0.02;
        this.y += (this.baseY - this.y) * 0.02;

        // Wrap around edges
        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;

        this.draw();
    }
}

// Create particles
let particlesArray = [];
const numberOfParticles = 80;

function init() {
    particlesArray = [];
    for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
    }
}
init();

// Animation loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
    }

    requestAnimationFrame(animate);
}
animate();

// Parallax Effect for sections
let parallaxSections = document.querySelectorAll('.about-visual, .project-card');

window.addEventListener('mousemove', (e) => {
    let mouseX = e.clientX / window.innerWidth;
    let mouseY = e.clientY / window.innerHeight;

    parallaxSections.forEach((section, index) => {
        let depth = index % 2 === 0 ? 10 : -10;
        let moveX = (mouseX - 0.5) * depth;
        let moveY = (mouseY - 0.5) * depth;

        section.style.transform = `translate(${moveX}px, ${moveY}px)`;
    });
});

// Animated Data Counters
const metricNumbers = document.querySelectorAll('.metric-number');
let countersAnimated = false;

function animateCounters() {
    if (countersAnimated) return;

    metricNumbers.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };

        updateCounter();
    });

    countersAnimated = true;
}

// Trigger counter animation when metrics section is in view
function checkMetrics() {
    const metricsSection = document.querySelector('.metrics-showcase');
    if (metricsSection) {
        const rect = metricsSection.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        if (rect.top < windowHeight * 0.8) {
            animateCounters();
        }
    }
}

window.addEventListener('scroll', checkMetrics);
window.addEventListener('load', checkMetrics);
