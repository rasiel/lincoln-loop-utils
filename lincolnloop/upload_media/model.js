if (typeof TinyMCE_Engine=='function') {
    tinyMCE.init({
       theme : 'django',
       theme_django_toolbar_location : 'top',
       theme_django_buttons1 : 'bold, italic, separator, bullist, numlist, outdent, indent, separator, justifyleft, justifycenter, justifyright, separator, link, unlink, separator, pastetext, pasteword, selectall, separator, code',
       theme_django_buttons2 : '',
       theme_django_buttons3 : '',
       plugins : 'inlinepopups, paste',
       button_tile_map : true,
       fix_list_elements : true,
   	   gecko_spellcheck : true,
   	   verify_html : true,
	   convert_urls : false,
   	   dialog_type : "modal",
   	   height : '300',
       mode : 'none' 
    });
}
function toggleEditorMode(sEditorID) {
    try {
        if(tinyMCEmode) {
            tinyMCE.removeMCEControl(tinyMCE.getEditorId(sEditorID));
            tinyMCEmode = false;
        } else {
            tinyMCE.addMCEControl(document.getElementById('pagecontent'), sEditorID);
            tinyMCEmode = true;
        }
    } catch(e) {
        //error handling
    }
}
$(function(){
    $('textarea').each(function(){
        //exclude common plain text fields
        if (!this.id.match('map') && !this.id.match('excerpt') && !this.id.match('teaser') && !this.id.match('comment')) {
            $(this).after('<iframe frameborder="0" style="border:none; width:755px; height:210px;" src="/admin/upload/?textarea='+this.id+'"></iframe>');
            if (typeof TinyMCE_Engine=='function') {
				var tinyMCEmode = true;
                tinyMCE.execCommand("mceAddControl", true, this.id); 
			}
        }
    });
});
