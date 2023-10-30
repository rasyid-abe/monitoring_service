class Alert 
{
    init()
    {
      this.initializeDataTable();
      this.detailButton();
      this.errorButton();
      this.alertActionButton()
    }

    initializeDataTable()
    {
      $("#example1").DataTable({
          "responsive": true,
          "autoWidth": false,
          columnDefs: [{
          "defaultContent": "-",
          "targets": "_all"
          }]
      });
      $("#example2").DataTable({
        "responsive": true,
        "autoWidth": false,
        "pageLength": 50,
        columnDefs: [{
        "defaultContent": "-",
        "targets": "_all"
        }]  
      });
      $("#example3").DataTable({
        "responsive": true,
        "autoWidth": false,
        columnDefs: [{
        "defaultContent": "-",
        "targets": "_all"
        }]  
      });
  }

  alertActionButton()
  {
    for(let i = 1; i<parseInt($('#alert_length').text())+1; i++)
    {
      $("#alert-action-"+i).change(function ()
      {
        let currentState = $(this).prop('checked');

        let status = 0;
        if (currentState)
        {
          status = 1;
        }

        let url = window.location.origin;
        url += '/apis/alert?purpouse=update-alert&id=' + $(this).val() + '&status=' + status;
        
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


  detailButton()
  {
    let that = this;
    for(let i = 1; i<parseInt($('#alert_length').text())+1; i++)
    {
      $("#btn-detail-"+i).click(function()
      {
        let url = window.location.origin;
        url += '/apis/alert?purpouse=etl&id=' + $(this).val()
        
        $.get(url, function(data, _)
        {
          let table = $("#example2").DataTable();
          table.clear().draw();

          data['data']['alert_detail'].forEach((item, index) => 
          {

            // let status = '<button id="btn-activation-' + i + '-' + index + '" class="btn btn-detail btn-success" value="' + item['id'] +'">Activate</button>'
            let status = '<input type="checkbox" id="toggle-activation-' + i + '-' + index + '" value="' + item['id'] +'" data-toggle="toggle" data-on="Enabled" data-off="Disabled" data-width="100" checked>'
            
            if (item['status'] == 0)
            {
              status = status.replace('checked', '')
            }

            let type_object = item['detail'];
            let type_text = '-';
            // only for ETL detail
            if (type_object != null)
            {
              type_text = type_object['type'] == 0 ? "Execution" : "Data"
              let button_style = type_object['type'] == 0 ? "btn-primary" : "btn-secondary"
              let button_type = '<button id="btn-type-' + i + '-' + index + '" class="btn btn-detail '+ button_style +'" value="' + item['id'] + '">' + type_text + '</button>'
              type_text = button_type
            }

            let row_value = [index+1, item['alert_detail_name'], that.timeStampConversion(item['updated_at']), status, type_text]

            if (table.columns().header().length != 5)
            {
              row_value = [index+1, item['alert_detail_name'], that.timeStampConversion(item['updated_at'])]
            }

            table.row.add(row_value)
            .draw()
            .node();
            
            $('#toggle-activation-' + i + '-' + index).bootstrapToggle()
            $("#toggle-activation-" + i + '-' + index).change(function() 
            {
              let currentState = $(this).prop('checked');
              let status = 0;
              if (currentState)
              {
                status = 1;
              }

              url = window.location.origin;
              url += '/apis/alert?purpouse=update-alert-detail&id=' + $(this).val() + '&status=' + status;
              
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
            })

            $("#btn-type-"+i+'-'+index).click(function() 
            {
              let buttonText = $(this).text();
              let detail = '{"type" : 0}';
              if (buttonText == 'Execution')
              {
                detail = '{"type" : 1}';
              }

              url = window.location.origin;
              url += '/apis/alert?purpouse=update-alert-detail-detail&id=' + $(this).val() + '&detail=' + detail;

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
      
                  let current_name = 'Execution'
                  let current_class = 'btn btn-detail btn-primary'
                  
                  if(detail == '{"type" : 1}')
                  {
                    current_name = 'Data';
                    current_class = current_class.replace('primary', 'secondary');
                  }
      
                  let btn = $('#btn-type-' + i + '-' + index) 
                  btn.text(current_name);
                  btn.prop('class', current_class);
      
                }else
                {
                  Toast.fire({
                    icon: 'error',
                    title: data['message']
                  });
                }
              })
            })



          });

          $('#detail-name').html(data['data']['alert_name'])
        });
      });
    }
  }

  errorButton()
  {
    let that = this;
    for(let i = 1; i<parseInt($('#alert_length').text())+1; i++)
    {
      $("#btn-error-"+i).click(function()
      {
        let url = window.location.origin;
        url += '/apis/alert?purpouse=history&id=' + $(this).val()
        
        $.get(url, function(data, status)
        {
          let table = $("#example3").DataTable();
          table.clear().draw();

          data['data']['alert_detail'].forEach((item, index) => 
          {
            let type = 'Error'
            if(item['type'] == 2)
            {
              type == 'Warning'
            } 

            table.row.add([index+1, item['id_alert_detail__alert_detail_name'], type, item['message'], that.timeStampConversion(item['created_at'])])
            .draw()
            .node();
          });

          $('#error-name').html(data['data']['alert_name'])
        });
      });
    }
  }

  timeStampConversion(timeStamp)
  {
    let date = timeStamp.split('T');
    let time = date[1].replace('Z', '')
    date = date[0].split('-')
    
    let result = date[2] + '/' + date[1] + '/' + date[0]
    result += ' ' + time.split('.')[0]

    return result;
  }


}

new Alert().init()