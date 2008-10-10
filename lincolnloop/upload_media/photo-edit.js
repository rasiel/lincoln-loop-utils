$(function(){
	$('.default').attr('name','_continue');
	var saved = $('.messagelist');
	if (saved.length) {
		//this needs to wait until the form submission is complete
		//opener.location.reload();
		window.close();
	}
	
    //check if this is a callback from Snipshot
    var url_split = document.location.href.split('?snipshot_file=');
    if (url_split.length > 1) {
        window.resizeTo(800,520);
        var arg_split = url_split[1].split('&');
        var request = {};
        request.photo = unescape(arg_split[0]);
        request.url = url_split[0];
        request.title = $('#id_title').val();
        request.description = $('#id_description').val();
        $('body').empty();
        $.get('/admin/upload/download/', request, function(data){
            document.location.href = '../'+data+'/?_popup=1';
        });
    }
    else {
        $('#id_upload').after(' <a href="#" id="photo-edit">Edit this photo</a>');
        $('#photo-edit').hide();
    }
    var ext = '';
    //check if the upload field contains an image path or PDF
    $('#id_upload').change(function(){
        var image_ext = ['.jpg', '.jpeg', '.gif', '.png', '.pdf'];
        var found = false;
        for (var i=0; i<image_ext.length; i++) {
            if ($(this).val().toLowerCase().lastIndexOf(image_ext[i]) > 0) {
                found = true;
                ext = image_ext[i].replace('.','');
                break;
            }
        }
        if (found == true)
            $('#photo-edit').show();
        else
            $('#photo-edit').hide();
    });
    //edit form to post to snipshot and submit
    $('a#photo-edit').click(function(){
        $(this).after('<input type="hidden" name="snipshot_input" value="upload"/>');
        $(this).after('<input type="hidden" name="snipshot_callback" value="'+document.location.href+'"/>');
        $(this).after('<input type="hidden" name="snipshot_output" value="snipshot_file"/>');
        $(this).after('<input type="hidden" name="snipshot_callback_agent" value="user"/>');
        $(this).parents('form').attr('action', 'http://services.snipshot.com/');
        $(this).parents('form').submit();
        return false;
    });
});
