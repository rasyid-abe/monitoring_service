class CDC 
{
    init()
    {

        this.initializeDataTable();
        this.etlDataButton();
    }

    initializeDataTable()
    {
        $("#example1").DataTable({
            "responsive": true,
            "autoWidth": false,
            "pageLength": 50,
        });
        $("#example3").DataTable({
          "responsive": true,
          "autoWidth": false,
          "pageLength": 10,
      });
    }

    timeStampConversion(timeStamp)
    {
      let date = timeStamp.split('T');
      let time = date[1].replace('Z', '')
      date = date[0].split('-')
      
      let result = date[2] + '/' + date[1] + '/' + date[0]
      result += ' ' + time

      return result;
    }

    etlDataButton()
    {
        let that = this;
        for(let i = 1; i<parseInt($('#data_length').text())+1; i++)
        {
          $("#btn-detail-data-cdc-"+i).click(function()
          {
            let url = window.location.origin;
            let table_name = $(this).val(); 
            url += '/apis/cdc?table_name=' + $(this).val()
            
            $.get(url, function(data, status)
            {
              let table = $("#example3").DataTable();
              table.clear().draw();
    
              data['data'].forEach((item, index) => 
              {
                table.row.add([index+1, item['data_source'], item['data_target'],
                  item['dispute'], item['execution_time'], that.timeStampConversion(item['actdate'])])                
                .draw()
                .node();
              });
    
              $('#cdc-table-name-title').html(table_name)
            });
          });
        }
    }
    
}

new CDC().init()