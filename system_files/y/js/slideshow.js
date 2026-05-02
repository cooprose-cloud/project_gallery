
// Photos at an Exposition - Slideshow Script

class Slideshow {
    constructor(containerId, config = {}) {
        this.container = document.getElementById(containerId);
        this.slides = this.container.querySelectorAll('.slideshow-slide');
        this.currentSlide = 0;
        this.interval = (config.interval_seconds || 5) * 1000;
        this.showCaptions = config.show_captions !== false;
        this.timer = null;
        
        // Hide captions if configured
        if (!this.showCaptions) {
            this.container.querySelectorAll('.slide-caption').forEach(caption => {
                caption.style.display = 'none';
            });
        }
    }
    
    start() {
        this.showSlide(0);
        this.timer = setInterval(() => this.nextSlide(), this.interval);
    }
    
    showSlide(index) {
        this.slides.forEach(slide => slide.classList.remove('active'));
        this.slides[index].classList.add('active');
        this.currentSlide = index;
    }
    
    nextSlide() {
        const next = (this.currentSlide + 1) % this.slides.length;
        this.showSlide(next);
    }
    
    stop() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}

// Configuration injected from JSON config file
const slideshowConfig = {"interval_seconds": 5, "show_captions": true};

// Initialize slideshow when page loads
document.addEventListener('DOMContentLoaded', function() {
    const slideshow = new Slideshow('slideshow', slideshowConfig);
    slideshow.start();
});
