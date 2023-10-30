class Recovery 
{
    
    init()
    {
        this.initializeDataTable();
        this.initializeModalButton();
        this.initializeDatePicker();
        this.recoveryProcess();

      }

    initializeModalButton()
    {
        let that = this;

        // recovery
        for(let i = 1; i<parseInt($('#recovery_length').text())+1; i++)
        {
            $("#btn-recovery-"+i).click(function()
            {                
                $('#recovery-name-title').html($('#etl-name-id-'+i).html())
                $('#url_input').val($(this).val())
            });
        }
    }

    initializeDataTable()
    {
      $("#example1").DataTable({
          "responsive": true,
          "autoWidth": false,
          "pageLength": 50,
      });
    }

    initializeDatePicker()
    {
        var start = moment().subtract(0, 'days');
        var end = moment();

        function cb(start, end) {
            $('#recovery_range span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }

        $('#recovery_range').daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            }
        }, cb);
        cb(start, end);
    }

    recoveryProcess()
    {
      let that = this;
      $("#recovery-process").click(function()
      {            
        
        let datePicker = $('#recovery_range').data('daterangepicker')
        let start = datePicker.startDate.format('YYYY-MM-DD')
        let end = datePicker.endDate.format('YYYY-MM-DD')

        if(that.checkingEmailFormat())
        {

          let url = $('#url_input').val() + '?'
          let email = 'email=' + $('#email_input').val()
          let _start = 'start_time=' + start + ' ' + '00:00:00'
          let _end = 'end_time=' + end + ' ' + '23:59:59'
          url += email + '&' + _start + '&' + _end

          window.open(url, "_blank");
        }
      });
    }

    checkingEmailFormat()
    {
      let email_input = $('#email_input').val()
      if (this.validateEmail(email_input))
      {
        $('#email-alert').css('display', 'none')
        return true;
      }else
      {
        $('#email-alert').css('display', 'block')
        return false;
      }
    }

    validateEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }

  }
  
new Recovery().init()