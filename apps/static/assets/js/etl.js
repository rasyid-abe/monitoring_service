class Etl 
{
    init()
    {

        this.initializeDataTable();
        this.etlDataButton();
        this.etlDataPostgresButton();
        this.getETLPerformance();

    }

    initializeDataTable()
    {
        $("#example1").DataTable({
            "responsive": true,
            "autoWidth": false,
            "pageLength": 50,
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

    getAirflowData()
    {
      let url = window.location.origin;
      url += '/apis/airflow/taks?type=1'

        $.get(url, function(data, status)
        {
          console.log(data);
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
        for(let i = 1; i<parseInt($('#etl_data_length').text())+1; i++)
        {
          $("#btn-detail-data-"+i).click(function()
          {
            let url = window.location.origin;
            let type = $(this).val(); 
            url += '/apis/etl/histories?type=' + $(this).val() + '&database=datamart'
            
            $.get(url, function(data, status)
            {
              let table = $("#example3").DataTable();
              table.clear().draw();
    
              data['data'].forEach((item, index) => 
              {
                table.row.add([index+1, item['id'], that.timeStampConversion(item['actdate']), 
                that.timeStampConversion(item['ts_current']), item['num_row'], item['time_process'], 
                that.timeStampConversion(item['ts_end']), item['params']])
    
                .draw()
                .node();
              });
    
              $('#etl-name-title').html(type)
            });
          });
        }
    }

    etlDataPostgresButton()
    {
        let that = this;
        for(let i = 1; i<parseInt($('#etl_data_postgres_length').text())+1; i++)
        {
          $("#btn-detail-data-postgres-"+i).click(function()
          {
            let url = window.location.origin;
            let type = $(this).val(); 
            url += '/apis/etl/histories?type=' + encodeURIComponent($(this).val()) + '&database=datamart_postgres'
            
            $.get(url, function(data, status)
            {
              let table = $("#example3").DataTable();
              table.clear().draw();
    
              data['data'].forEach((item, index) => 
              {
                table.row.add([index+1, item['id'], that.timeStampConversion(item['actdate']), 
                that.timeStampConversion(item['ts_current']), item['num_row'], item['time_process'], 
                that.timeStampConversion(item['ts_end']), item['params']])
    
                .draw()
                .node();
              });
    
              $('#etl-name-title').html(type)
            });
          });
        }
    }

    getETLPerformance()
    {
      let url = window.location.origin;
      url += '/apis/etl/histories?database=datamart_postgres&purpose=1'
      
      $.get(url, function(data, status)
      {
        let table = $("#example4").DataTable();
        table.clear().draw();

        data['data'].forEach((item, index) => 
        {
          table.row.add([index+1, item[0], item[1]['performance'], item[1]['execution_time'], item[1]['estimation_time'], item[1]['estimation_time_day'] ])
          .draw()
          .node();
        });
      });
    }

    

    
}

new Etl().init()