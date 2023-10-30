class RecoveryPromo 
{
    
    init()
    {
        this.initializeDataTable();
      }
      
    initializeDataTable()
    {
      $("#example1").DataTable({
        "responsive": true,
        "autoWidth": false,
        "pageLength": 20,
      });
    }

}

new RecoveryPromo().init()