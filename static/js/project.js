// Detect Touch
function isTouchSupported() {
    var msTouchEnabled = window.navigator.msMaxTouchPoints;
    var generalTouchEnabled = "ontouchstart" in document.createElement("div");

    if (msTouchEnabled || generalTouchEnabled) {
        return true;
    }
    return false;
}

window.addEventListener('DOMContentLoaded', function() {
    $(document).ready(function() {

    // Initial Values
    var countrySelect = $('select[name="country"]').val();
    var stateVal = $('#id_state').val();
    var cityVal = $('#id_line4').val();
    var stateInitialSet = false;
    var cityInitialSet = false;

    function updateSelects(){
        // Tutti gli input select di wagtail form
        $(".state_select, .city_select, select[name='country']").select2({
          width: 'resolve'
        });
        // Initial value
        if(typeof(countrySelect) !== 'undefined'){
            if(countrySelect.length > 0){
                getStates(countrySelect);
            }
        }
    }

    $(document).on('select2:open', () => {
        document.querySelector('.select2-search__field').focus();
    });

    // Append fake select and hide input text
    $('#id_state').parent().prepend('<select class="form-control state_select" required><option></option></select>');
    $('#id_state').hide();
    $('#id_line4').parent().prepend('<select class="form-control city_select" required><option></option></select>');
    $('#id_line4').hide();

    // Country event
    $('select[name="country"]').on('change', function(){
        if($(this).val().length > 0){
            getStates($(this).val());
        }
        // Clean state / city
        $('#id_state').val('');
        $('#id_line4').val('');
        $(".state_select, .state_select~.select2, .city_select, .city_select~.select2").show().prop('required',true).val('');
    });

    // State event
    $('.state_select').on('change', function() {
        if($(this).val().length > 0){
            getCities($(this).val());
        }
        $('#id_state').val($(this).val());
        // Clean city
        $('#id_line4').val('');
    });

    // City event
    $('.city_select').on('change', function() {
        $('#id_line4').val($(this).val());
    });
    
    // Funzione che ritorna tutti stati
    var getStates = function(value){
        $.ajax({
            type: "POST",
            url: "/get_states/",
            data: {
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
              value: value,
            },
        })
        .done(function (data) {
            if(data.error == 1){
                alert(msg);
            }else{
                if(data.content.length > 0){
                    $('#id_state, #id_line4').hide();
                    $(".state_select, .state_select~.select2, .city_select, .city_select~.select2").show().prop('required',true);
                    // Clean select state
                    $(".state_select").find('option').remove();
                    $(".state_select").append('<option value="">---------</option>').val('');
                    // Clean select cities
                    $(".city_select").find('option').remove();
                    $(".city_select").append('<option value="">---------</option>').val('');
                    // Add options to select
                    for (let index = 0; index < data.content.length; index++) {
                        const element = data.content[index];
                        var o = new Option(element.name, element.name);
                        /// jquerify the DOM object 'o' so we can use the html method
                        $(o).html(element.name);
                        $(".state_select").append(o);
                    }
                    // Initial Value
                    if(stateVal.length > 0 && !stateInitialSet){
                        $(".state_select").val(stateVal);
                        $("#id_state").val(stateVal);
                        getCities(stateVal);
                        stateInitialSet=true;
                    }
                }else{
                    // Se è vuoto devo dare la possibilità all'utente di scrivere a mano
                    $('#id_state, #id_line4').show();
                    $(".state_select, .state_select~.select2, .city_select, .city_select~.select2").hide().removeAttr('required');
                }
            }
        })
        .fail(function () {
            alert("Spiacenti, si è verificato un errore. Per favore riprova più tardi");
        });
    }

    // Funzione che ritorna tutte le città
    var getCities = function(value){
        $.ajax({
            type: "POST",
            url: "/get_cities/",
            data: {
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
              value: value,
            },
          })
        .done(function (data) {
            if(data.error == 1){
                alert(msg);
            }else{
                if(data.content.length > 0){
                    $(".city_select, .city_select~.select2").show().prop('required',true);
                    $('#id_line4').hide();
                    // Clean select
                    $(".city_select").find('option').remove();
                    $(".city_select").append('<option value="">---------</option>').val('');
                    // Add options to select
                    for (let index = 0; index < data.content.length; index++) {
                        const element = data.content[index];
                        var o = new Option(element.name, element.name);
                        /// jquerify the DOM object 'o' so we can use the html method
                        $(o).html(element.name);
                        $(".city_select").append(o);
                    }
                    // Initial Value
                    if(cityVal.length > 0 && !cityInitialSet){
                        $(".city_select").val(cityVal);
                        $("#id_line4").val(cityVal);
                        cityInitialSet=true;
                    }
                }else{
                    // Se è vuoto devo dare la possibilità all'utente di scrivere a mano
                    $('#id_line4').show();
                    $(".city_select, .city_select~.select2").hide().removeAttr('required');
                }
            }
        })
        .fail(function () {
            alert("Spiacenti, si è verificato un errore. Per favore riprova più tardi");
        });
    }

    // get video resoluction
    var isHighDefEnabled = !isTouchSupported() && window.innerWidth > 720;
    var vids = document.getElementsByTagName('video'); 
    
    for( var i = 0; i < vids.length; i++ ){ 
        var source = vids[i].querySelector("source");
        var videoHigh = source.getAttribute('data-video-high');
        var videoLow = source.getAttribute('data-video-low');
        if(videoHigh != undefined && isHighDefEnabled){
            source.setAttribute("src", videoHigh);
        }else if(videoLow != undefined){
            source.setAttribute("src", videoLow);
        }
        vids[i].load();
        vids[i].play();
    }

    if(self.webView != undefined){
        self.webView.mediaPlaybackRequiresUserAction = NO;
    }

    if ($(".video-popup").length) {
        $(".video-popup").magnificPopup({
          type: "iframe",
          mainClass: "mfp-fade",
          removalDelay: 160,
          preloader: true,
    
          fixedContentPos: false
        });
    }
    
    // run
    updateSelects();

    });





    //menu  
    $('[data-toggle="offcanvas"]').on('click', function () {
        $('.offcanvas-collapse').toggleClass('open')
    })
    
    $('#menu .nav-link').on('click', function(){
        $('.offcanvas-collapse').toggleClass('open')
    })

    $('.close-menu').on('click', function(){
        $('.offcanvas-collapse').toggleClass('open')
    })


    
    var $hamburger = $(".hamburger");
  $hamburger.on("click", function(e) {
    $hamburger.toggleClass("is-active");
    // Do something else, like open/close menu
  });



     /* per risolvere il bug del flash su Chrome scrollando in su, è necessario aggiungere position fixed al container */
  /* non posso usare il detect del sistema operativo perché su iPad non funziona */
  function isTouchDevice() {
    return (('ontouchstart' in window) ||
       (navigator.maxTouchPoints > 0) ||
       (navigator.msMaxTouchPoints > 0));
  }

  if (isTouchDevice()){
    $('.bg-parallax').css('background-attachment', 'scroll');
}
    

});


