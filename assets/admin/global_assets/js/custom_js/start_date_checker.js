// inorder to use this js file you have set the name of start date as start_date, name of end date field to end_date and the id of 
// the submit button to submit_btn
// finally add the following div element just where you want your alert to be shown

// <div id='alart' style="display:none;" class="alert alert-danger"  role="alert"> 
//  <p id="alart_message" >   </p>
// </div>
    $("input[name = 'start_date']").change(function () {check_date_input()})
	$("input[name = 'end_date']").change(function () {check_date_input()})

  
function set_alert_message(text)
{  
        alert_box = document. getElementById("alart_message")
        alert_box.innerHTML = text;
        alert_box.style['display'] = 'block';
        $("input [type = 'submit']").attr("disabled",  true);
		$("button[type = 'submit']").attr("disabled", true);
}
	
function check_date_input()
	{		
      
        var start_date = new Date($("input[name = 'start_date']").val()); 
        var end_date = new Date($("input[name = 'end_date']").val()); 
        str_today = new Date().toDateString()
        // new Date() is changed to DateString, inorder to cut of the timezone from the date, as the date from start date and end date is just the date field without time zone
        today = new Date(str_today)
        if(start_date < today){
            document. getElementById("alart").style.display = "block"; //show
            set_alert_message("start date must be greater than or equal to today!!")	
        }
        else if (start_date > end_date) {
            document. getElementById("alart").style.display = "block"; //show
            set_alert_message("End date must be greater than or equal to start date!!")
        }
        else{
            document. getElementById("alart").style.display = "none"; //hide.
            $("input[type = 'submit']").attr("disabled",  false);
			$("button[type = 'submit']").attr("disabled", false);
            }
	}