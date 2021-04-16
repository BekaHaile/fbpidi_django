$(document).ready(function () {
    var date = new Date();
    var current_year = new Date().getFullYear()-8

    $(".summernote").summernote();

    // Investment Capital Form
    $("#inv_capital_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        console.log(formData);
        $.ajax({
            url: "/admin/create_investment_capital/"+project_id+"/",
            headers: { "X-CSRFToken": my_token },
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    // $("#inv_capital_form_modal").modal("hide");
                    $("#success_invcap").html(result['message']);
                    $("#errors_invcap").empty();
                } else {
                    $("#errors_invcap").html(result['message']);
                    $("#success_invcap").empty();
                }
            },
            error: function (error) {
                $("#errors_invcap").html(error['statusText']);
                $("#success_invcap").empty();
            }
        });
    });

 
    $("#employee_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_employees-project/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#success_employee").html(result['message']);
                    $("#errors_employee").empty();
                    // $("#employees_form_modal").modal("hide");
                } else {
                    $("#errors_employee").html(result['message']);
                    $("#success_employee").empty();
                }
            },
            error: function (error) {
                $("#errors_employee").html(error['statusText']);
                $("#success_employee").empty();
            }
        });

    });
    $("#jobcreated_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_jobs_created-project/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#success_jobs").html(result['message']);
                    $("#errors_jobs").empty();
                    // $("#createdjob_form_modal").modal("hide");
                } else {
                    $("#errors_jobs").html(result['message']);
                    $("#success_jobs").empty();
                }
            },
            error: function (error) {
                $("#errors_jobs").html(error['statusText']);
                $("#success_jobs").empty();
            }
        });

    });
    $("#education_stat_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_education_status-project/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result);
                if (result['error'] == false) {
                    $("#success_education").html(result['message']);
                    $("#errors_education").empty();
                    // $("#education_status_form_modal").modal("hide");
                } else {
                    $("#errors_education").html(result['message']);
                    $("#success_education").empty();
                }
            },
            error: function (error) {
                $("#errors_education").html(error['statusText']);
                $("#success_education").empty();
            }
        });

    });
    $("#land_aquistion_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/craete_land-aqsn/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result);
                if (result['error'] == false) {
                    $("#success_aqsn").html(result['message']);
                    $("#errors_aqsn").empty();
                    // $("#education_status_form_modal").modal("hide");
                } else {
                    $("#errors_aqsn").html(result['message']);
                    $("#success_aqsn").empty();
                }
            },
            error: function (error) {
                $("#errors_aqsn").html(error['statusText']);
                $("#success_aqsn").empty();
            }
        });

    });
    
    $("#usage_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/craete_land-usage/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result);
                if (result['error'] == false) {
                    $("#success_usage").html(result['message']);
                    $("#errors_usage").empty();
                    // $("#education_status_form_modal").modal("hide");
                } else {
                    $("#errors_usage").html(result['message']);
                    $("#success_usage").empty();
                }
            },
            error: function (error) {
                $("#errors_usage").html(error['statusText']);
                $("#success_usage").empty();
            }
        });

    });
    $("#status_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_project_state/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result);
                if (result['error'] == false) {
                    $("#success_status").html(result['message']);
                    $("#errors_status").empty();
                    // $("#education_status_form_modal").modal("hide");
                } else {
                    $("#errors_status").html(result['message']);
                    $("#success_status").empty();
                }
            },
            error: function (error) {
                $("#errors_status").html(error['statusText']);
                $("#success_status").empty();
            }
        });

    });
    $("#company_address_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_project_address/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['error'] == false) {
                    $("#errors_span").empty();
                    $("#success_span").html(result['message']);
                    // $("#address_form_modal").modal("hide");
                } else {
                    $("#errors_span").html(result['message']);
                    $("#success_span").empty();
                }
            },
            error: function (error) {
                $("#errors_span").html(error['statusText']);
                $("#success_span").empty();
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
                    $("#errors_span").empty();
                    $("#success_span").html(result['message']);
                    // $("#address_form_modal").modal("hide");
                } else {
                    $("#errors_span").html(result['message']);
                    $("#success_span").empty();
                }
            },
            error: function (error) {
                $("#errors_span").html(error['statusText']);
                $("#success_span").empty();
            }
        });

    });

    $("#product_form").submit(function (e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        $.ajax({
            url: "/admin/create_product_quantity/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result);
                if (result['error'] == false) {
                    $("#success_product").html(result['message']);
                    $("#errors_product").empty();
                    // $("#education_status_form_modal").modal("hide");
                } else {
                    $("#errors_product").html(result['message']);
                    $("#success_product").empty();
                }
            },
            error: function (error) {
                $("#errors_product").html(error['statusText']);
                $("#success_product").empty();
            }
        });

    });
    // 
   
    $("#id_employment_type").change(function(){
        var emp_typ = $(this).val();
        $.ajax({
            url: "/admin/check_project_year_data/employee/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data:{
                'emp_type':emp_typ,
            },
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_employee").prop("disabled",false);
                    $("#errors_employee").empty();
                } else {
                    $("#errors_employee").html(emp_typ+" "+result['message']);
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
    
    $("#id_job_type").change(function(){
        var job_type = $(this).val();
        $.ajax({
            url: "/admin/check_project_year_data/jobs_created/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data:{'job_type':job_type},
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_jobs").prop("disabled",false);
                    $("#errors_jobs").empty();
                } else {
                    $("#errors_jobs").html(job_type+" "+result['message']);
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
 
    $("#id_education_type").change(function(){
        var year = $("#id_year_edu").val();
        var edu_type = $(this).val();
        var quarter_edu = $("#id_quarter_edu").val();
        $.ajax({
            url: "/admin/check_project_year_data/education/"+project_id+"/",
            type: "POST",
            headers: { "X-CSRFToken": my_token },
            data:{'edu_type':edu_type},
            success: function (result) {
                if (result['error'] == false) {
                    $("#submit_education").prop("disabled",false);
                    $("#errors_education").empty();
                } else {
                    $("#errors_education").html(edu_type+" "+result['message']);
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
    $("#update_project_form").click(function(){
        $("#submit_update").submit();
    });
 
});

