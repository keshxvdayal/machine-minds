const slider = document.querySelector('#priceSlider')
const display = document.querySelector('#sliderValue')
const products = document.querySelectorAll('.product')

slider.oninput = function() {
    const sliderValue = parseInt(this.value)
    display.textContent = `\$${sliderValue}`
    
    products.forEach(product => {
        const price = parseInt(product.dataset.price)

        if (sliderValue > parseInt(this.min) && sliderValue < parseInt(this.max)) {
            if (sliderValue >= price) {
                gsap.to(product, {autoAlpha: 1, scale: 1, duration: 0.5})
            } else {
                gsap.to(product, {autoAlpha: 0, scale: 0.8, duration: 0.5})
            }
        } else {
            gsap.to(product, {autoAlpha: 1, scale: 1, duration: 0.5})
        }
    });
};