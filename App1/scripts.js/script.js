// Navigation and Interactive Elements
document.addEventListener('DOMContentLoaded', function() {
    // Active Navigation Highlighting
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active-nav');
        }
    });

    // Pest Search Functionality
    const searchInput = document.getElementById('pest-search');
    
    if (searchInput) {
        const pestCards = document.querySelectorAll('.pest-card');
        const noResultsMessage = document.querySelector('.no-pests-found');

        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            let visibleCardsCount = 0;

            pestCards.forEach(card => {
                // Extract text from different elements
                const pestName = card.querySelector('h3').textContent.toLowerCase();
                const scientificName = card.querySelector('.pest-scientific-name').textContent.toLowerCase();
                const damagePreview = card.querySelector('.pest-damage-preview').textContent.toLowerCase();
                
                // Check if search term matches any of the text fields
                const isMatch = 
                    pestName.includes(searchTerm) || 
                    scientificName.includes(searchTerm) || 
                    damagePreview.includes(searchTerm);
                
                if (isMatch) {
                    card.style.display = 'block';
                    visibleCardsCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Toggle visibility of no results message
            if (noResultsMessage) {
                noResultsMessage.style.display = visibleCardsCount === 0 ? 'block' : 'none';
            }
        });
    }

    // Lazy Loading for Images
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.dataset.src || image.src;
                    image.classList.add('loaded');
                    observer.unobserve(image);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });

        lazyImages.forEach(image => imageObserver.observe(image));
    }

    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Theme Toggle (Optional)
    const themeToggleButton = document.getElementById('theme-toggle');
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', 
                document.body.classList.contains('dark-mode') ? 'dark' : 'light'
            );
        });
    }

    // Check and Apply Saved Theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
});

// Additional Utility Functions
function debounce(func, delay) {
    let debounceTimer;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(context, args), delay);
    }
}