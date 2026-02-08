


const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});


const mobileBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');

if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
}


const carouselTrack = document.querySelector('.carousel-track');
const carouselPrev = document.querySelector('.carousel-prev');
const carouselNext = document.querySelector('.carousel-next');
const carouselDots = document.querySelectorAll('.carousel-dots .dot');
const projectCards = document.querySelectorAll('.carousel-track .project-card-link');

let currentIndex = 0;
const totalProjects = projectCards.length;

function updateCarousel() {
    
    const cardWidth = 440;
    const gap = 32; 
    const offset = currentIndex * (cardWidth + gap);

    
    carouselTrack.style.transform = `translateX(-${offset}px)`;

    
    projectCards.forEach((card, index) => {
        if (index === currentIndex) {
            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    });

    
    carouselDots.forEach((dot, index) => {
        if (index === currentIndex) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}


if (carouselNext) {
    carouselNext.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalProjects;
        updateCarousel();
    });
}


if (carouselPrev) {
    carouselPrev.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalProjects) % totalProjects;
        updateCarousel();
    });
}


carouselDots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentIndex = index;
        updateCarousel();
    });
});


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
            
            currentIndex = (currentIndex + 1) % totalProjects;
            updateCarousel();
        }
        if (touchEndX > touchStartX + swipeThreshold) {
            
            currentIndex = (currentIndex - 1 + totalProjects) % totalProjects;
            updateCarousel();
        }
    }
}


if (projectCards.length > 0) {
    updateCarousel();
}


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


window.addEventListener('scroll', checkScroll);
window.addEventListener('load', checkScroll);


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


const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');


function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);


let mouse = {
    x: null,
    y: null,
    radius: 150 
};

window.addEventListener('mousemove', (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
});


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

        
        const colors = ['#FF6B35', '#FF8555', '#FF9F70'];
        this.color = colors[Math.floor(Math.random() * colors.length)];
    }

    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();

        
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
    }

    update() {
        
        this.x += this.speedX;
        this.y += this.speedY;

        
        if (mouse.x != null && mouse.y != null) {
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < mouse.radius) {
                let force = (mouse.radius - distance) / mouse.radius;
                let directionX = dx / distance;
                let directionY = dy / distance;

                
                this.x -= directionX * force * 3;
                this.y -= directionY * force * 3;
            }
        }

        
        this.x += (this.baseX - this.x) * 0.02;
        this.y += (this.baseY - this.y) * 0.02;

        
        if (this.x < 0) this.x = canvas.width;
        if (this.x > canvas.width) this.x = 0;
        if (this.y < 0) this.y = canvas.height;
        if (this.y > canvas.height) this.y = 0;

        this.draw();
    }
}


let particlesArray = [];
const numberOfParticles = 80;

function init() {
    particlesArray = [];
    for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
    }
}
init();


function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
    }

    requestAnimationFrame(animate);
}
animate();


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


const metricNumbers = document.querySelectorAll('.metric-number');
let countersAnimated = false;

function animateCounters() {
    if (countersAnimated) return;

    metricNumbers.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; 
        const increment = target / (duration / 16); 
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
