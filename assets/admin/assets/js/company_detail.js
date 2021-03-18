$(document).ready(function () {
    $(".summernote").summernote();

    // 
    $("#expn_yes").click(function(){
        $("#div_expn").css('display','block');
    });
    $("#expn_no").click(function(){
        $("#div_expn").css('display','none');
    });
    $("#lab_yes").click(function(){
        $("#div_lab").css('display','block');
    });
    $("#lab_no").click(function(){
        $("#div_lab").css('display','none');
    });
    $("#outsrc_yes").click(function(){
        $("#div_outsrc").css('display','block');
    });
    $("#outsrc_no").click(function(){
        $("#div_outsrc").css('display','none');
    });
    $("#rsrch_yes").click(function(){
        $("#div_rsrch").css('display','block');
    });
    $("#rsrch_no").click(function(){
        $("#div_rsrch").css('display','none');
    });
    $("#product_yes").click(function(){
        $("#div_product").css('display','block');
    });
    $("#product_no").click(function(){
        $("#div_product").css('display','none');
    });
    $("#wastetrt_yes").click(function(){
        $("#div_waste_trtmt").css('display','block');
    });
    $("#wastetrt_no").click(function(){
        $("#div_waste_trtmt").css('display','none');
    });
    $("#ce_yes").click(function(){
        $("#div_ce").css('display','block');
    });
    $("#ce_no").click(function(){
        $("#div_ce").css('display','none');
    });
    $("#env_complaint_yes").click(function(){
        $("#div_env_complaint").css('display','block');
    });
    $("#env_complaint_no").click(function(){
        $("#div_env_complaint").css('display','none');
    });
    $("#linkage_yes").click(function(){
        $("#div_linkage").css('display','block');
    });
    $("#linkage_no").click(function(){
        $("#div_linkage").css('display','none');
    });


    // Investment Capital Form
    $("#inv_capital_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        console.log(formData);
        $.ajax({
            url: "/admin/create_investment_capital/"+company_id+"/",
            headers: { "X-CSRFToken": my_token },
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#inv_capital_form_modal").modal("hide");
                    $("#errors").html(result['message']);
                } else {
                    $("#errors").html(result['message']);
                }
            },
            error: function (error) {

            }
        });
    });

    $("#certificate_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_company_certificates/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#errors_certificate").html(result['message']);
                } else {
                    $("#errors_certificate").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#employee_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_employees/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#errors_employee").html(result['message']);
                    // $("#employees_form_modal").modal("hide");
                } else {
                    $("#errors_employee").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#jobcreated_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_jobs_created/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#errors_jobs").html(result['message']);
                    // $("#createdjob_form_modal").modal("hide");
                } else {
                    $("#errors_jobs").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#education_stat_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_education_status/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result);
                if (result['error'] == false) {
                    $("#errors_education").html(result['message']);
                    // $("#education_status_form_modal").modal("hide");
                } else {
                    $("#errors_education").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#femaleposn_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_femalein_posn/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#femaleposn_form_modal").modal("hide");
                    $("#errors_femaleposn").html(result['message']);
                } else {
                    $("#errors_femaleposn").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#srcamnt_input_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_srcamnt_inputs/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#srcamnt_input_form_modal").modal("hide");
                    $("#errors_input").html(result['message']);
                } else {
                    $("#errors_input").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#destination_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_market_destination/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#destination_form_modal").modal("hide");
                    $("#errors_destination").html(result['message']);
                } else {
                    $("#errors_destination").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#target_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_market_target/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#target_form_modal").modal("hide");
                    $("#errors_target").html(result['message']);
                } else {
                    $("#errors_target").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#power_consumption_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_power_consumption/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#power_consumption_form_modal").modal("hide");
                    $("#errors_powerc").html(result['message']);
                } else {
                    $("#errors_powerc").html(result['message']);

                }
            },
            error: function (error) {

            }
        });

    });
    $("#company_address_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_company_address/"+company_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#error_span").html(result['message']);
                    // $("#address_form_modal").modal("hide");
                } else {
                    $("#error_span").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#address_form_update").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/update_company_address/"+address_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#error_span").html(result['message']);
                    // $("#address_form_modal").modal("hide");
                } else {
                    $("#error_span").html(result['message']);
                }
            },
            error: function (error) {

            }
        });

    });
    $("#submit_update").click(function(){
        $("#update_company_info").submit();
    });
     
    $("#id_year_inv").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/investment/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_inv_capital").prop("disabled",false);
                    $("#errors").empty();
                } else {
                    $("#errors").html(result['message']);
                    $("#submit_inv_capital").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors").html(error['statusText']);
            }
        });
    });
    $("#id_year_emp").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/employee/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_employee").prop("disabled",false);
                    $("#errors_employee").empty();
                } else {
                    $("#errors_employee").html(result['message']);
                    $("#submit_employee").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_employee").html(error['statusText']);
                $("#submit_employee").prop("disabled",true);
            }
        });
    });
    $("#id_year_job").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/jobs_created/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_jobs").prop("disabled",false);
                    $("#errors_jobs").empty();
                } else {
                    $("#errors_jobs").html(result['message']);
                    $("#submit_jobs").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_jobs").html(error['statusText']);
                $("#submit_jobs").prop("disabled",true);
            }
        });
    });
    $("#id_year_edu").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/education/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_education").prop("disabled",false);
                    $("#errors_education").empty();
                } else {
                    $("#errors_education").html(result['message']);
                    $("#submit_education").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        $("#id_"+field).val(result['data']['fields'][field]);
                        // $("select[id='id_"+field+"']").val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_education").html(error['statusText']);
                $("#submit_education").prop("disabled",true);
            }
        });
    });

    $("#id_year_fem").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/female_emp/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_femaleposn").prop("disabled",false);
                    $("#errors_femaleposn").empty();
                } else {
                    $("#errors_femaleposn").html(result['message']);
                    $("#submit_femaleposn").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_femaleposn").html(error['statusText']);
                $("#submit_femaleposn").prop("disabled",true);
            }
        });
    });
    // 
    $("#id_year_src").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/src_amnt/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_input_srcamnt").prop("disabled",false);
                    $("#errors_input").empty();
                } else {
                    $("#errors_input").html(result['message']);
                    $("#submit_input_srcamnt").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_input").html(error['statusText']);
                $("#submit_input_srcamnt").prop("disabled",true);
            }
        });
    });
     // 
     $("#id_day").change(function(){
        var day = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/power_consumption/"+company_id+"/"+day+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_powerconsumed").prop("disabled",false);
                    $("#errors_powerc").empty();
                } else {
                    $("#errors_powerc").html(result['message']);
                    $("#submit_powerconsumed").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_powerc").html(error['statusText']);
                $("#submit_powerconsumed").prop("disabled",true);
            }
        });
    });
     // 
     $("#id_year_destn").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/destination/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_destination").prop("disabled",false);
                    $("#errors_destination").empty();
                } else {
                    $("#errors_destination").html(result['message']);
                    $("#submit_destination").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_destination").html(error['statusText']);
                $("#submit_destination").prop("disabled",true);
            }
        });
    });
     // 
     $("#id_year_target").change(function(){
        var year = $(this).val();

        $.ajax({
            url: "/admin/check_company_year_data/target/"+company_id+"/"+year+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_target").prop("disabled",false);
                    $("#errors_target").empty();
                } else {
                    $("#errors_target").html(result['message']);
                    $("#submit_target").prop("disabled",true);
                    for(var field in result['data']['fields']){
                        
                        $("#id_"+field).val(result['data']['fields'][field]);
                    }
                }
            },
            error: function (error) {
                $("#errors_target").html(error['statusText']);
                $("#submit_target").prop("disabled",true);
            }
        });
    });
});