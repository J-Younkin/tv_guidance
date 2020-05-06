$('.ajax_form').submit(function(e){
    e.preventDefault()
})
$('#ajax_search').keyup(function(){
    console.log('Sending Ajax request to /shows/all/find')
    console.log('Submitting the following data', $(this).parent().serialize())
    $.ajax({
    url: '/shows/all/find', /* Where should this go? */
    method: 'post', /* Which HTTP verb? */
    data: $(this).parent().serialize(), /* Any data to send along? */
    success: function(serverResponse) { /* What code should we run when the server responds? */
        $('#show_table').html(serverResponse)
    }
    })
});