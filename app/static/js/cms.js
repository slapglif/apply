$(document).ready(function() {

    setupActionButtons();

    $('div.actions_layer a').click(function(){
        $(this).parent().fadeOut('fast');
        $('a.actions_button .selected').removeClass('selected');
        $(this).closest('.member_list').removeAttr('style');
    });

    $('body').click(function(){
       $('div.actions_layer').fadeOut('fast');
       $('a.actions_button').removeClass('selected');
       $('.member_list').removeAttr('style');
    });

    $('.trigger_search').click(function(){
        $(this).closest('form').submit();
        return false;
    });

    $(document).on('click','.trigger_ajax', function(){
        var $this = $(this);
        var memberId = $this.parents('.member_list').prop('id');
        var collapced = $this.parents('.member_list').find('.member_expand').hasClass('expanded');
        $.get($(this).attr('href'), function(data){
            var divs = $(data).filter(function(){ return $(this).is('div.view_list_detail'); });
            $this.parents('.member_list').replaceWith($(divs).find('#'+memberId));
            tabsAndSortable();
            if (!collapced) {
                $('#'+memberId).find('.talent-header, .member-tabs').hide();
                $('#'+memberId).find('.member_expand').removeClass('expanded');
            }
        });
        return false;
    });

    $(document).on('click','.trigger_edit_listmember', function(){
        $.ajax({
            type : 'POST',
            url : $(this).attr('href'),
            success: function(data){
                $('.modal_form, #fade_layer').fadeIn('fast',function(){
                    $('#modal_form_content').html(data);
                });
                tabsAndSortable();
            }
        });

        return false;
    });

    $(document).on('click', '.trigger-budgetting', function(e){
        $(this).parents('td').find('> a, form').toggleClass('hidden');
        e.preventDefault();
        return false;
    });

});


function setupActionButtons(){

    $(document).on('click', 'a.actions_button', function(){

        $(this).closest('.member_list').css('z-index', 500);

        $('div.actions_layer').fadeOut('fast');
        $(this).toggleClass('selected');
        $('a.actions_button').not(this).removeClass('selected');

        if( $(this).hasClass('selected') ){
            $(this).parent('.actions_container').children('div.actions_layer').fadeIn('fast');
        }
        return false;

    });
}