$(document).ready(function() {
    $('#about-btn').click(function() {
        let msgStr = $('#msg').html();
        msgStr = msgStr + ' OH, fancy!';
        $('#msg').html(msgStr);
    });
    $('#about-btn').removeClass('btn-primary').addClass('btn-success');

    $('p').hover(
        function() {
            $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'black');
        }
    );
})