import Alpine from 'alpinejs'

document.addEventListener('alpine:init', () => {
    Alpine.data('dropdown', () => ({
        open: false,

        init() {
            console.log('dropdown loading...');
        },

        toggle() {
            this.open = ! this.open
        }
    }))
})
