import Alpine from 'alpinejs';

Alpine.directive('uppercase', el => {
    el.textContent = el.textContent.toUpperCase()
})
