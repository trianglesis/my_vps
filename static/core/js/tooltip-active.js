// $(document).ready(function () {
//     $('[data-toggle="tooltip"]').tooltip();
// });
// $(document).ready(function () {
//     $('[data-toggle="popover"]').popover();
// });
// $(document).ready(function () {
//     $('[data-toggle="hover"]').popover({
//         trigger: 'hover'
//     });
// });


// //https://getbootstrap.com/docs/5.0/components/popovers/
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})
