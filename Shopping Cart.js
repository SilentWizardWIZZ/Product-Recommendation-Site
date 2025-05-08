document.addEventListener('DOMContentLoaded', function() {
    // Cart functionality
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    const addToWishlistButtons = document.querySelectorAll('.btn-add-to-wishlist');
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    
    // Initialize cart and wishlist from localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    
    // Add to Cart
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            
            // Add product to cart
            const productExists = cart.some(item => item.id === productId);
            
            if (productExists) {
                // Update quantity
                cart = cart.map(item => {
                    if (item.id === productId) {
                        return {...item, quantity: item.quantity + 1};
                    }
                    return item;
                });
            } else {
                // Add new product
                cart.push({
                    id: productId,
                    name: productName,
                    quantity: 1
                });
            }
            
            // Save cart to localStorage
            localStorage.setItem('cart', JSON.stringify(cart));
            
            // Show alert
            if (alertPlaceholder) {
                const alert = document.createElement('div');
                alert.className = 'alert alert-success alert-dismissible fade show';
                alert.innerHTML = `
                    ${productName} has been added to your cart!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                alertPlaceholder.appendChild(alert);
                
                // Remove alert after 3 seconds
                setTimeout(() => {
                    alert.remove();
                }, 3000);
            }
        });
    });
    
    // Add to Wishlist
    addToWishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            
            // Check if product already exists in the wishlist
            const productExists = wishlist.some(item => item.id === productId);
            
            if (!productExists) {
                // Add to wishlist
                wishlist.push({
                    id: productId,
                    name: productName
                });
                
                // Save wishlist to localStorage
                localStorage.setItem('wishlist', JSON.stringify(wishlist));
                
                // Show alert
                if (alertPlaceholder) {
                    const alert = document.createElement('div');
                    alert.className = 'alert alert-info alert-dismissible fade show';
                    alert.innerHTML = `
                        ${productName} has been added to your wishlist!
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    `;
                    alertPlaceholder.appendChild(alert);
                    
                    // Remove alert after 3 seconds
                    setTimeout(() => {
                        alert.remove();
                    }, 3000);
                }
            } else {
                // Show alert that product is already in wishlist
                if (alertPlaceholder) {
                    const alert = document.createElement('div');
                    alert.className = 'alert alert-warning alert-dismissible fade show';
                    alert.innerHTML = `
                        ${productName} is already in your wishlist!
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    `;
                    alertPlaceholder.appendChild(alert);
                    
                    // Remove alert after 3 seconds
                    setTimeout(() => {
                        alert.remove();
                    }, 3000);
                }
            }
        });
    });
});