$(document).ready(function() {
    var table = $('#statustable').DataTable({
        searchPanes: {
            columns: [4, 3],
            layout: 'columns-1',
            orderable: false,
            controls: false,
            hideCount: false,
        },
        language: {
            searchPanes: {
                title: {
                    _: '',
                    0: '',
                    1: ''
                }
            }
        },
        pageLength: 25,
        lengthMenu: [ 25, 50, 75, 100 ]
    });
    table.searchPanes.container().appendTo('#filters');
    table.searchPanes.resizePanes();
});