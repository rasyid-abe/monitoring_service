class RecoveryHardDelete 
{
    
    init()
    {
        this.initializeDataTable();
        this.showDetail();
      }
      
    initializeDataTable()
    {
      $("#example1").DataTable({
        "responsive": true,
        "autoWidth": false,
        "pageLength": 100,
      });
      $("#example2").DataTable({
        "responsive": true,
        "autoWidth": false,
      });
      $("#example3").DataTable({
        "responsive": true,
        "autoWidth": false,
      });
    }

    showDetail()
    {
      let that = this;

      for(let i = 1; i<parseInt($('#recovery_length').text())+1; i++)
      {
        $("#btn-detail-recovery-"+i).click(function()
          {
            let detail = $(this).val(); 
            detail = detail.replace(/'/g, '"');
            detail = JSON.parse(detail)

            // get table object
            let table = $("#example2").DataTable();
            table.clear().draw();
            
            let i = 1;
            for (let item in detail)
            {
              
              let status = '-'
              let tProcess = '-'
              let nrow = '-'

              if ('status' in detail[item] && detail[item]['status'] == 'success')
              {                
                status = '<button class="btn btn-success">' + detail[item]['status']  + '</button>'
                
                if ('tProcess' in detail[item])
                {
                  tProcess = (detail[item]['tProcess'] / 60000).toFixed(2)
                }

                if ('nrow' in detail[item])
                {
                  nrow = detail[item]['nrow']
                }
              
              }
              else
              {
                status = '<button class="btn btn-danger">' + 'failed'  + '</button>'
              }

              table.row.add([i, item, status, tProcess, nrow])
              .draw()
              .node();
              i += 1;
            }

          });
      }


    }


}

new RecoveryHardDelete().init()