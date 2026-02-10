/* Main Application Script */

// Change navbar when scrolling (for Project Pages)
const navbar = document.getElementById('navbar');

// Function to check scroll metrics and apply/remove 'scrolled' class
function checkMetrics() {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

if (navbar) {
    window.addEventListener('scroll', checkMetrics);
    window.addEventListener('load', checkMetrics); // Also check on load in case page is refreshed while scrolled
}

// GSAP Entry Animation
window.addEventListener('load', () => {
    // Check if GSAP is loaded
    if (typeof gsap !== 'undefined') {
        const tl = gsap.timeline();

        // 1. Counter 0-100%
        const counterElement = document.querySelector('.loader-counter');

        if (counterElement) {
            let count = { val: 0 };
            tl.to(count, {
                val: 100,
                duration: 1.5,
                ease: "power2.inOut",
                onUpdate: () => {
                    counterElement.textContent = Math.floor(count.val) + "%";
                }
            });

            // 2. Curtain Slide Up
            tl.to('.loader', {
                yPercent: -100,
                duration: 0.8,
                ease: "power4.inOut"
            }, "+=0.2"); // slight pause after 100%
        }

        // 3. Elements Reveal (Staggered)
        // Main Name (slides up from opacity 0, y: 100)
        tl.fromTo('.main-name.hero-reveal',
            { y: 100, opacity: 0 },
            { y: 0, opacity: 1, duration: 1, ease: "power3.out" },
            "-=0.4" // overlap with loader sliding up
        );

        // Top Corners (slide down)
        tl.fromTo('.corner-top-left.hero-reveal, .corner-top-center.hero-reveal, .corner-top-right.hero-reveal',
            { y: -50, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: "power3.out" },
            "-=0.6"
        );

        // Center Carousel (Scale up + Fade)
        tl.fromTo('.horizontal-carousel-wrapper.hero-reveal',
            { scale: 0.9, opacity: 0 },
            { scale: 1, opacity: 1, duration: 1, ease: "power2.out" },
            "-=0.6"
        );

        // Bottom Right Bio (Slide up)
        tl.fromTo('.corner-bottom-right.hero-reveal',
            { y: 50, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" },
            "-=0.8"
        );
    }
});

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

if (canvas) {
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
}

// Parallax Effect for sections
let parallaxSections = document.querySelectorAll('.about-visual, .project-card');

if (parallaxSections.length > 0) {
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
}
