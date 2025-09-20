// Main JavaScript file for AI Artisan Marketplace

// Utility functions
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            notification.style.backgroundColor = '#ffc107';
            notification.style.color = '#333';
            break;
        default:
            notification.style.backgroundColor = '#17a2b8';
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#e1e5e9';
        }
    });
    
    return isValid;
}

// API helper functions
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API call failed:', error);
        return { success: false, message: 'Network error occurred' };
    }
}

// Product interaction tracking
function trackProductView(productId) {
    // This would typically send analytics data
    console.log(`Product ${productId} viewed`);
}

function trackProductInteraction(productId, interactionType) {
    // This would typically send analytics data
    console.log(`Product ${productId} ${interactionType}`);
}

// Search and filter functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach(card => {
            const productName = card.querySelector('h3').textContent.toLowerCase();
            const productDescription = card.querySelector('.product-description').textContent.toLowerCase();
            const productCategory = card.querySelector('.product-category').textContent.toLowerCase();
            
            if (productName.includes(searchTerm) || 
                productDescription.includes(searchTerm) || 
                productCategory.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Category filter functionality
function initializeCategoryFilter() {
    const categorySelect = document.getElementById('categoryFilter');
    if (!categorySelect) return;
    
    categorySelect.addEventListener('change', function(e) {
        const selectedCategory = e.target.value;
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach(card => {
            const productCategory = card.querySelector('.product-category').textContent.toLowerCase();
            
            if (selectedCategory === 'all' || productCategory.includes(selectedCategory)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// AI Story generation with loading state
async function generateAIStory(description, category, callback) {
    const generateBtn = document.querySelector('[onclick*="generateStory"]');
    const originalText = generateBtn.innerHTML;
    
    // Show loading state
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    generateBtn.disabled = true;
    
    try {
        const result = await apiCall('/generate_story', {
            method: 'POST',
            body: JSON.stringify({ description, category })
        });
        
        if (result.success) {
            callback(result.story);
            showNotification('AI story generated successfully!', 'success');
        } else {
            showNotification('Error generating story: ' + result.message, 'error');
        }
    } catch (error) {
        showNotification('An error occurred while generating the story', 'error');
    } finally {
        // Reset button state
        generateBtn.innerHTML = originalText;
        generateBtn.disabled = false;
    }
}

// Product recommendation engine (client-side)
function getRecommendedProducts(userPreferences, allProducts) {
    if (!userPreferences || !allProducts) return allProducts;
    
    const preferences = userPreferences.toLowerCase().split(',').map(p => p.trim());
    const scoredProducts = allProducts.map(product => {
        let score = 0;
        const productText = `${product.name} ${product.description} ${product.category}`.toLowerCase();
        
        preferences.forEach(pref => {
            if (productText.includes(pref)) {
                score += 1;
            }
        });
        
        return { ...product, score };
    });
    
    return scoredProducts
        .sort((a, b) => b.score - a.score)
        .slice(0, 6);
}

// Image upload preview
function initializeImageUpload() {
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    
    if (!imageInput || !imagePreview) return;
    
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    initializeCategoryFilter();
    initializeImageUpload();
    initializeSmoothScrolling();
    
    // Add loading states to all forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
    
    // Add hover effects to product cards
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Export functions for global use
window.showNotification = showNotification;
window.validateForm = validateForm;
window.apiCall = apiCall;
window.trackProductView = trackProductView;
window.trackProductInteraction = trackProductInteraction;
window.generateAIStory = generateAIStory;
window.getRecommendedProducts = getRecommendedProducts;

