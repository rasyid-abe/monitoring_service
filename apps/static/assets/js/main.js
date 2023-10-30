class Main 
{
    init()
    {
        this.hideSidebar()
    }

    hideSidebar()
    {
        $(document).ready(function(){
            $("body").addClass("sidebar-collapse");
        });
    }
}

// new Main().init()