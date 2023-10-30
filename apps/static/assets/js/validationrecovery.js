class ValidationRecovery 
{
    
    init()
    {
        var CURRENT_VALIDITY = '';
        var CURRENT_RECOVERY = '';
        var IS_READONLY = this.getReadonlyStatus();

        this.initializeDataTable();
        this.initializeModalButton();
        this.initializeDatePicker();
        this.executeValidityDatePicker();
        this.executeRecoveryDatePicker();
        
        if(IS_READONLY != 1)
        {
          this.fillNifiGroupList();
          this.schedulerSave();
        }
      }
      
    getReadonlyStatus()
    {
      let status = 1;
      if(document.getElementById('scheduler-table').rows[0].cells.length == 6)
      {
        status = 0;
      }

      return status;
    }

    fillNifiGroupList()
    {
        let filter = '?data_type=Nifi_Group';
        let url = window.location.origin;
        let that = this;
        url += '/apis/validity-and-recovery' + filter;
        that.displayLoading("scheduler");
        $.get(url, function(data, status)
        {
            data = data['data']
            that.schedulerTable(data['etl'], data['recovery'])
        });
    }

    initializeDataTable()
    {
        $("#example1").DataTable({
            "responsive": true,
            "autoWidth": false,
          });
          $("#example2").DataTable({
            "responsive": true,
            "autoWidth": false,
          });
          $("#example3").DataTable({
            "responsive": true,
            "autoWidth": false,
            columnDefs: [{
              "defaultContent": "-",
              "targets": "_all"
            }]      
          });
          $("#example4").DataTable({
            "responsive": true,
            "autoWidth": false,
            columnDefs: [{
              "defaultContent": "-",
              "targets": "_all"
            }]
        });
    }

    initializeModalButton()
    {
        let that = this;

        // recovery
        for(let i = 1; i<parseInt($('#recovery_length').text())+1; i++)
        {
            $("#btn-detail-data-recovery-"+i).click(function()
            {
                that.CURRENT_RECOVERY = $(this).val();
                let start_time = moment($('#recovery_range').data('daterangepicker').startDate).format('YYYY-MM-DD');
                let end_time = moment($('#recovery_range').data('daterangepicker').endDate).format('YYYY-MM-DD');
                
                that.getRecoveryData($(this).val(), start_time, end_time)
            });
        }

        // validity
        for(let i = 1; i<parseInt($('#validity_length').text())+1; i++)
        {
            $("#btn-detail-data-validity-"+i).click(function()
            {
                that.CURRENT_VALIDITY = $(this).val();
                let start_time = moment($('#validity_range').data('daterangepicker').startDate).format('YYYY-MM-DD');
                let end_time = moment($('#validity_range').data('daterangepicker').endDate).format('YYYY-MM-DD');

                that.getValidityData($(this).val(), start_time, end_time)
            });
        }
    }

    initializeDatePicker()
    {
        var start = moment().subtract(0, 'days');
        var end = moment();

        function cb(start, end) {
            $('#validity_range span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
            $('#recovery_range span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }

        $('#validity_range').daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, cb);
        cb(start, end);

        $('#recovery_range').daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, cb);
        cb(start, end);
    }

    getValidityData(name, start_time, end_time)
    {
        let that = this;
        that.displayLoading("validity");
        let url = window.location.origin;
        let filter = '?data_type=Validity&type=' + name + '&start_time=' + start_time + '&end_time=' + end_time;  
        url += '/apis/validity-and-recovery' + filter
        
        $.get(url, function(data, status)
        {
            let table = $("#example3").DataTable();
            table.clear().draw();

            data['data'].forEach((item, index) => 
            {
                table.row.add([index+1, item['id_user'], item['id_cabang'], 
                    item['is_recovery'] == 1 ? "Done" : "Waiting", item['total']])
                .draw()
                .node();
            });

            $('#validity-name-title').html(name)
            that.hideLoading("validity");
        });
    }

    getRecoveryData(name, start_time, end_time)
    {
        let that = this; 
        that.displayLoading("recovery");
        let url = window.location.origin;
        let filter = '?data_type=Recovery&type=' + name + '&start_time=' + start_time + '&end_time=' + end_time; 
        url += '/apis/validity-and-recovery' + filter;
        
        $.get(url, function(data, status)
        {
            let table = $("#example4").DataTable();
            table.clear().draw();

            data['data'].forEach((item, index) => 
            {
                table.row.add([index+1, item['id_user'], item['id_cabang'], item['total'], item['rows']])
                .draw()
                .node();
            });

            $('#recovery-name-title').html(name)
            that.hideLoading("recovery");
        });
    }

    executeValidityDatePicker()
    {
        let that = this;
        $('#validity_range').on('apply.daterangepicker', function(ev, picker) {
            let start_time = picker.startDate.format('YYYY-MM-DD');
            let end_time = picker.endDate.format('YYYY-MM-DD');
            
            that.getValidityData(that.CURRENT_VALIDITY, start_time, end_time)
        });
    }

    executeRecoveryDatePicker()
    {
        let that = this;
        $('#recovery_range').on('apply.daterangepicker', function(ev, picker) {
            let start_time = picker.startDate.format('YYYY-MM-DD');
            let end_time = picker.endDate.format('YYYY-MM-DD');
            that.getRecoveryData(that.CURRENT_RECOVERY, start_time, end_time)
        });
    }

    timeStampConversion(timeStamp)
    {
        let date = timeStamp.split('T');
        date = date[0].split('-')
        
        let result = date[2] + '/' + date[1] + '/' + date[0]

        return result;
    }

    timeStampConversion2(timeStamp)
    {
        let date = timeStamp.split(' ');
        let time = date[1].split('.')[0]
        date = date[0].split('-')
        
        let result = date[2] + '/' + date[1] + '/' + date[0]
        result += ' ' + time

        return result;
    }

    timeStampConversion3(timeStamp)
    {
        let date = timeStamp.split('T');
        let time = date[1].replace('Z', '')
        date = date[0].split('-')
        
        let result = date[2] + '/' + date[1] + '/' + date[0]
        result += ' ' + time

        return result;
    }

    hideLoading(name)
    {
        let loader = document.querySelector("#" + name + "_loading");
        loader.classList.remove("display");
          
    }
    
    displayLoading(name)
    {
        let loader = document.querySelector("#" + name + "_loading");
        loader.classList.add("display");

        // to stop loading after some time
        setTimeout(() => {
            loader.classList.remove("display");
        }, 15000);
    }


    editSaveButton(state)
    {
      let btn = document.getElementById('btn-scheduler-save');

      if(state == 'disable')
      {
        btn.disabled = true;
      }else
      {
        btn.disabled = false;
      }
    }

    schedulerSave()
    {
        let that = this;
        $("#btn-scheduler-save").click(function() {
            let table = $('#scheduler-table');
            let data = [];
            table = table.find('tr');
            let table_length = table.length;
            
            table.each(function(i, el) 
            {
              let $tds = $(this).find('td');
              if($tds.length == 6)
              {
                let row = []
                $tds.each(function (i2, el){
                  if(i2 <= 4)
                  {
                      row.push($(this).text());
                  }
                });
                data.push(row)
              }
              
            });
             
            let url = window.location.origin;
            url += '/apis/validity-and-recovery'
            data = 
            {
                data : data
            }

            $.ajax({
                url: url,
                headers : { "X-CSRFToken": that.getCookie("csrftoken")},
                type : 'post',
                data : data,
                success: function(data)
                {
                    var Toast = Swal.mixin({
                        toast: true,
                        position: 'top-end',
                        showConfirmButton: false,
                        timer: 3000
                    });

                    if(data['status'] == 200)
                    {
                        Toast.fire({
                        icon: 'success',
                        title: data['message']
                        });
                    }else
                    {
                        Toast.fire({
                            icon: 'error',
                            title: data['message']
                        });
                    }
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert(textStatus, errorThrown);
                }
            });

        });
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    schedulerTable(etl, recovery)
    {
        let that = this; 
        $('[data-toggle="tooltip"]').tooltip();
        var actions = $("#scheduler-table td:last-child").html();
        // Append table with add row form on add new button click
        $(".add-new").click(function() {
          $(this).attr("disabled", "disabled");
          var index = $("#scheduler-table tbody tr:last-child").index();
          var row =
            "<tr>" +
            '<td><div class="autocomplete"><input id="newInput-' + index + 1 + '" type="text" class="form-control" name="nifi-name" placeholder="ETL Name"></div></td>' +
            '<td><div class="autocomplete"><input id="newInput-' + index + 2 + '" type="text" class="form-control" name="nifi-name" placeholder="Recovery Name"></div></td>' +
            '<td><input type="time" class="form-control" name="start"></td>' +
            '<td><input type="time" class="form-control" name="end"></td>' +
            '<td><select class="form-control"><option value="Yes">Yes</option><option value="No">No</option></select> </td>' +
            "<td>" + actions + "</td>" +
            "</tr>";
          $("#scheduler-table").append(row);
          
          $("#scheduler-table tbody tr")
            .eq(index + 1)
            .find(".add, .edit")
            .toggle();
        
         that.autocomplete(document.getElementById('newInput-' + index + 1), etl);
         that.autocomplete(document.getElementById('newInput-' + index + 2), recovery);

        });
        // Add row on add button click
        $(document).on("click", ".add", function() {
          that.editSaveButton('activate')
          var empty = false;
          var input = $(this)
            .parents("tr")
            .find('input[type="text"]');
          var input2 = $(this)
            .parents("tr")
            .find('input[type="time"]');
          var input3 = $(this)
            .parents("tr")
            .find('select');

          input.each(function() {
            if (!$(this).val()) {
              $(this).addClass("error");
              empty = true;
            } else {
              $(this).removeClass("error");
            }
            });
          input2.each(function() {
                if (!$(this).val()) {
                  $(this).addClass("error");
                  empty = true;
                } else {
                  $(this).removeClass("error");
                }
            });
          input3.each(function() {
              if (!$(this).val()) {
                $(this).addClass("error");
                empty = true;
              } else {
                $(this).removeClass("error");
              }
          });
          $(this)
            .parents("tr")
            .find(".error")
            .first()
            .focus();
          if (!empty) {
            input.each(function() {
              $(this)
                .parent("div")
                .html($(this).val());
            });
            input2.each(function() {
                $(this)
                  .parent("td")
                  .html($(this).val());
              });
            input3.each(function() {
                $(this)
                  .parent("td")
                  .html($(this).val());
              });
            $(this)
              .parents("tr")
              .find(".add, .edit")
              .toggle();
            $(".add-new").removeAttr("disabled");
          }
        });
        // Edit row on edit button click
        $(document).on("click", ".edit", function() {
          that.editSaveButton('disable')
          $(this)
            .parents("tr")
            .find("td:not(:last-child)")
            .each(function(number) {
                let html_value = '<input id="" type="time" class="form-control" name="start" value="' ;
                let random_number = Math.floor(Math.random() * 1000);
                html_value += $(this).text() + '">'
                if(number == 0)
                {
                    let container = '<div class="autocomplete">INPUT</div>'
                    html_value = html_value.replace('id=""', 'id="editInput-' + random_number + '"');
                    html_value = html_value.replace('time', 'text')
                    html_value = container.replace("INPUT", html_value);
                }

                if(number == 1)
                {
                    let container = '<div class="autocomplete">INPUT</div>'
                    html_value = html_value.replace('id=""', 'id="editInput-' + random_number + 1 + '"');
                    html_value = html_value.replace('time', 'text')
                    html_value = container.replace("INPUT", html_value);
                }
                
                if(number == 3)
                {
                    html_value = html_value.replace("start", "end");
                }

                if(number == 4)
                {
                  html_value = '<select class="form-control"><option value="Yes" selected>Yes</option><option value="No">No</option></select>'
                  
                  if ($(this).text() == 'No')
                  {
                    html_value = html_value.replace('selected', '');
                    html_value = html_value.replace('value="No"', 'value="No" selected');
                  }

                }
                
                $(this).html(html_value)

                if(number == 0)
                {
                    that.autocomplete(document.getElementById('editInput-' + random_number), etl);
                }

                if(number == 1)
                {
                    that.autocomplete(document.getElementById('editInput-' + random_number + 1), recovery);
                }
                
            });
          $(this)
            .parents("tr")
            .find(".add, .edit")
            .toggle();
          $(".add-new").attr("disabled", "disabled");
        });
        // Delete row on delete button click
        $(document).on("click", ".delete", function() {
          $(this)
            .parents("tr")
            .remove();
          $(".add-new").removeAttr("disabled");
        });
        that.hideLoading("scheduler");
    }

    autocomplete(inp, arr) {
        /*the autocomplete function takes two arguments,
        the text field element and an array of possible autocompleted values:*/
        var currentFocus;
        /*execute a function when someone writes in the text field:*/
        inp.addEventListener("input", function(e) {
            var a, b, i, val = this.value;
            /*close any already open lists of autocompleted values*/
            closeAllLists();
            if (!val) { return false;}
            currentFocus = -1;
            /*create a DIV element that will contain the items (values):*/
            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            /*append the DIV element as a child of the autocomplete container:*/
            this.parentNode.appendChild(a);
            /*for each item in the array...*/
            for (i = 0; i < arr.length; i++) {
              /*check if the item starts with the same letters as the text field value:*/
              if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                    b.addEventListener("click", function(e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
              }
            }
        });
        /*execute a function presses a key on the keyboard:*/
        inp.addEventListener("keydown", function(e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
              /*If the arrow DOWN key is pressed,
              increase the currentFocus variable:*/
              currentFocus++;
              /*and and make the current item more visible:*/
              addActive(x);
            } else if (e.keyCode == 38) { //up
              /*If the arrow UP key is pressed,
              decrease the currentFocus variable:*/
              currentFocus--;
              /*and and make the current item more visible:*/
              addActive(x);
            } else if (e.keyCode == 13) {
              /*If the ENTER key is pressed, prevent the form from being submitted,*/
              e.preventDefault();
              if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
              }
            }
        });
        function addActive(x) {
          /*a function to classify an item as "active":*/
          if (!x) return false;
          /*start by removing the "active" class on all items:*/
          removeActive(x);
          if (currentFocus >= x.length) currentFocus = 0;
          if (currentFocus < 0) currentFocus = (x.length - 1);
          /*add class "autocomplete-active":*/
          x[currentFocus].classList.add("autocomplete-active");
        }
        function removeActive(x) {
          /*a function to remove the "active" class from all autocomplete items:*/
          for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
          }
        }
        function closeAllLists(elmnt) {
          /*close all autocomplete lists in the document,
          except the one passed as an argument:*/
          var x = document.getElementsByClassName("autocomplete-items");
          for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
            x[i].parentNode.removeChild(x[i]);
          }
        }
      }
      /*execute a function when someone clicks in the document:*/
      document.addEventListener("click", function (e) {
          closeAllLists(e.target);
      });
      }

}

new ValidationRecovery().init()