import '@/css/tailwind.css'
import '@/scss/main.scss';
import lab from './lab';

import Alpine from 'alpinejs'

// Utils
import './utils/uppercase';

// Components
// import dropdown from './components/dropdown';
// Alpine.data('dropdown', dropdown)

// Inlines!?
import './components/dropdown';

Alpine.magic('now', () => {
    return (new Date).toLocaleTimeString()
})


window.addEventListener('DOMContentLoaded', lab());
window.Alpine = Alpine
Alpine.start()
