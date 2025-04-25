export default () => ({
    open: false,

    init() {
        //console.log('dropdown loading...');
    },

    toggle() {
        this.open = ! this.open
    }
})
