class ETLCaller 
{
    init()
    {
      this.initializeDataTable();
      this.changeIsRunning();
      this.changeEndpoint();
    }

    initializeDataTable()
    {
      $("#example1").DataTable({
          "responsive": true,
          "autoWidth": false,
          "pageLength": 100,
          columnDefs: [{
          "defaultContent": "-",
          "targets": "_all"
          }]
      });
  }

  changeIsRunning()
  {
    for(let i = 1; i<parseInt($('#etl_length').text())+1; i++)
    {
      $("#etl-"+i).change(function ()
      {
        let currentState = $(this).prop('checked');

        let status = 0;
        if (currentState)
        {
          status = 1;
        }

        let url = window.location.origin;
        url += '/apis/etl-caller?purpose=is_active&id=' + $(this).val() + '&status=' + status;
        
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

  changeEndpoint()
  {
    for(let i = 1; i<parseInt($('#etl_length').text())+1; i++)
    {
      $("#btn-edit-"+i).click(function ()
      {
        let id = $(this).val(); 
        let endpoint = $('#endpoint-'+i).text()
        let name = 'Edit Endpoint - ' + $('#etl-name-'+i).text()
        $('#etl-title').html(name);
        $('#etl_name').val($('#etl-name-'+i).text());
        $('#endpoint').val(endpoint);
        $('#id').val(id);
      });
    }
  }

  



}

new ETLCaller().init()