$(document).ready(function() {
	$('a[target="_blank"]').click(function(){
        _gaq.push(['_trackEvent', 'Offsite Link', 'Click', $(this).attr('href')]);
        return true;
    });

    /*************************** BEGIN 2013 GOOGLE ANALYTICS // EVENT TRACKING ******************************/

    /**
    *
    * Note: There are several important functions for the event tracking
    * found in other files:
    * 		opportunity.functions.js
    * 		opportunity-backbone.js
    *
    **/

    //Deliverable:
    $('#deliverables_add').on('click', 'div div:not(.group)', function(){
        //_gaq.push(['_trackEvent', 'SOW', 'Add Deliverable', 'Focus']);
        _gaq.push(['_trackEvent', 'Project Choice', 'Click', $(this).html() ]);

    });

    // Company Name
    $('#opportunity_post').on('focus', '#company input[type=text]', function() {
        _gaq.push(['_trackEvent', 'Sign Up – Company', 'Click', 'Company Name']);
    })

    //Company Description
    $('#opportunity_post').on('focus', '#company textarea', function() {
        _gaq.push(['_trackEvent', 'Sign Up – Company', 'Click', 'Company Description']);
    })

        /* Make Company Confidential */
    $('#opportunity_post').on('click', '#company .checkbox input', function() {
         _gaq.push(['_trackEvent', 'Sign Up – Company', 'Click', 'Make Company Confidential']);
    })

    /* Location Specific */
    $('#candidates').on('click', '.location_container .answers .drop', function() {
    	_gaq.push(['_trackEvent', 'Sign Up – Company', 'Click', 'Location Specific']);
    })

    /* Will You Cover Costs?: */
    $('#candidates').on('click', '.input.radio input', function() {
    	checkval = $(this).val()
    	if(checkval == 1) {
    		_gaq.push(['_trackEvent', 'Sign Up – Company', 'Click', 'Travel Expense - Yes']);
    	} else {
    		_gaq.push(['_trackEvent', 'Sign Up – Company', 'Click', 'Travel Expense - No']);
    	}
    })

    // Project Title Click
    $('#opportunity_post').on('focus', '#title input#OpportunityName', function() {
        _gaq.push(['_trackEvent', 'Sign Up – Project Title', 'Click', 'Project Title']);
    });

    //Preview Page Payment/Edit/Draft Buttons
    $('#preview_container').on('click', '.btns_container .btn, .btns_container #btn_save_draft', function() {
    	var whichButton = $(this).attr('id');
    	switch(whichButton) {
    		case 'btn_proceed_payment':
    			button = 'Proceed to Payment';
    			break;
    		case 'btn_edit_post':
    			button = 'Edit Post';
    			break;
    		case 'btn_save_draft':
    			button = 'Save as Draft';
    			break;
    	}
        _gaq.push(['_trackEvent', 'Preview Project Window', 'Click', button ]);
    })

    //Preview Page // side bar edit buttons:
    $('#preview_container').on('click', '.preview-edit', function() {
        _gaq.push(['_trackEvent', 'Preview Project Window', 'Click', 'Edit - Specific' ]);
    })

    //Save Draft ... buttons:
    $('#preview_container').on('click', '#cancel_draft_btn', function() {
        _gaq.push(['_trackEvent', 'Save as Draft Window', 'Click', 'Go Back' ]);
    })

    //Save Draft... email
    $('#preview_container').on('focus', '.data-preview #OpportunityEmail', function() {
        _gaq.push(['_trackEvent', 'Account Sign Up', 'Click', 'Name']);
    })

    //account sign up:

   /* $('#payment_page').on('focus', '.inputs #UserName', function() {
    	_gaq.push(['_trackEvent', 'Account Sign Up', 'Click', 'Name']);
    })

    $('#payment_page').on('focus', '.inputs #UserEmail', function() {
    	_gaq.push(['_trackEvent', 'Account Sign Up', 'Click', 'Email']);
    }) */

    $('#payment_page').on('click', '.payment-submit', function() {
       	_gaq.push(['_trackEvent', 'Account Sign Up', 'Click', 'Submit Project Button']);
    })

    //Challenger SOW Page event tracking specifics
    $('.info-block-alternative').on('click', '#main a.btn', function() {
        _gaq.push(['_trackEvent', 'Challenger Page Start', 'Click', 'Quick Start']);
    })

    //see if we can grab the elements when created...
    //this is sketchy, but I don't want to write into the Pages Controller ...
    //here, we just see if the positive message appears on the challenger page
    //and fire the _gaq if present....
    if( $('.challenger-wrap #modal_content_flash .primary-column h1').html() == 'Thank You!' ) {
        _gaq.push(['_trackEvent', 'Challenger Page Start', 'Click', 'Email Submit Success']);
    }

   $('body.creative_agencies').on('click', '.btn-orange', function() {
        _gaq.push(['_trackEvent', 'Control Page Start', 'Click', 'Get Started']);
   })

    if( $('body.creative_agencies #modal_content_flash .primary-column h1').html() == 'Thank You!' ) {
        _gaq.push(['_trackEvent', 'Control Page Start', 'Click', 'Email Submit Success']);
    }

    $('#wrap').on('click', '#cancel_draft_btn', function() {
        _gaq.push(['_trackEvent', 'Sign Up – Completion', 'Click', 'Go Back']);
    })

    // Opportunities/pitch even tracking
    $('#wrap').on('click', '#opportunities_submit_pitch', function() {
        //_gaq.push(['_trackEvent', 'Pitch Process - Opp Page', 'Click', 'Submit Pitch Button']);
        _gaq.push(['_trackPageview', '/pitch/step1_submit_pitch_button']);
    });

    $("#OpportunityRequestSubmitForm").on("focusout", "#TalentlistMemberPitch", function (event) {
        if($(this).val() != ''){
            //_gaq.push(['_trackEvent', 'Pitch Process - Pitch Page', 'Pitch', 'Talent Pitch']);
            _gaq.push(['_trackPageview', '/pitch/step2_talent_pitch']);
        }
    });

    $("#OpportunityRequestSubmitForm").on("focusout", "#TalentlistMemberLink0Url", function (event) {
        if($(this).val() != ''){
            _gaq.push(['_trackEvent', 'Pitch Process - Pitch Page', 'Link', 'Initial Pitch Link']);
        }
    });

    $("#OpportunityRequestSubmitForm").on("click", "#trigger_talentlist_link", function (event) {
        _gaq.push(['_trackEvent', 'Pitch Process - Pitch Page', 'Link', 'Initial Pitch Link']);
    });

    $("#OpportunityRequestSubmitForm").on("click", ".btn.btn-preview", function (event) {
        //_gaq.push(['_trackEvent', 'Pitch Process - Pitch Page', 'Click', 'Pitch Preview Button']);
        _gaq.push(['_trackPageview', '/pitch/step3_pitch_preview_button']);
    });

    $("#OpportunityRequestSubmitForm").on("click", "#opportunities_pitch_cancel", function (event) {
        _gaq.push(['_trackEvent', 'Pitch Process - Pitch Page', 'Click', 'Pitch Cancelled']);
    });

    $("#OpportunityRequestSubmitForm").on("click", "#opportunities_purchase_credits", function (event) {
        _gaq.push(['_trackEvent', 'Pitch Process - Pitch Modal', 'Click', 'Purchase Credits']);
    });

    $("#OpportunityRequestSubmitForm").on("click", "#opportunities_go_back", function (event) {
        _gaq.push(['_trackEvent', 'Pitch Process - Pitch Modal', 'Click', 'Go Back and Edit']);
    });

    $("#OpportunityRequestSubmitForm").on("click", "#opportunities_submit_payment", function (event) {
        //_gaq.push(['_trackEvent', 'Pitch Process - Pitch Modal', 'Click', 'Submit Payment']);
        _gaq.push(['_trackPageview', '/pitch/step4_submit_pitch_button']);
    });

    /*************************** END GOOGLE ANALYTICS EVENT TRACKING ******************************/

});

