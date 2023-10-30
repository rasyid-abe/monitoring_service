class EtlStatus 
{
    init()
    {

        this.initializeDataTable();
        this.autoSwitchButton();
        this.switchDatamart();

    }

    initializeDataTable()
    {
        $("#example1").DataTable({
            "responsive": true,
            "autoWidth": false,
            "pageLength": 100,
        });
    }

    autoSwitchButton()
    {
      for(let i = 1; i<parseInt($('#report_list_length').text())+1; i++)
      {
        $("#etl-status-"+i).change(function ()
        {
          let currentState = $(this).prop('checked');
  
          let status = 'False';
          if (currentState)
          {
            status = 'True';
          }
  
          let url = window.location.origin;
          url += '/apis/etl-status?purpose=is_automate&id=' + $(this).val() + '&status=' + status;
          
          $.get(url, function(data, _) 
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
              $(this).prop('checked', !currentState);
            }
          })
  
        });
      }
    }

    switchDatamart()
    {
      for(let i = 1; i<parseInt($('#report_list_length').text())+1; i++)
      {
        $("#report-"+i).change(function ()
        {
          let currentState = $(this).prop('checked');
          if(!confirm("Are you sure you want to change state?"))
          {
            location.reload()
            return false;
          }
  
          let status = 'False';
          if (currentState)
          {
            status = 'True';
          }
  
          let url = window.location.origin;
          url += '/apis/etl-status?purpose=datamart&id=' + $(this).val() + '&status=' + status;
          
          $.get(url, function(data, _) 
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
              $(this).prop('checked', !currentState).change();
            }
          })
  
        });
      }
    }

  

    
}

new EtlStatus().init()