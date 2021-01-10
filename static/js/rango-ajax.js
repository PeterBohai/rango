$(document).ready(function() {
    $('#like_btn').click(function() {
        let categoryId = $(this).attr('data-categoryid');

        const q_data = {
            'category_id': categoryId
        }
        console.log(q_data);
        $.get('/rango/like_category/', q_data, function(data) {
            $('#like_count').html(data);
            $('#like_btn').hide();
        })
    })

    $('#search-input').keyup(function() {
        let query = $(this).val();
        $.get('/rango/suggest/', {'suggestion': query}, function(data) {
            $('#categories-listing').html(data)
        })
    })

    $('.rango-page-add').click(function() {
        let categoryid = $(this).attr('data-categoryid');
        let title = $(this).attr('data-title');
        let url = $(this).attr('data-url');
        let clickedButton = $(this);

        let querystring_data = {
            'category_id': categoryid,
            'title': title,
            'url': url
        }
        $.get('/rango/search_add_page/', querystring_data, function(data) {
            $('#page-listing').html(data);
            clickedButton.hide();
        })
    })
})