
migrate = {};

migrate.migration_complete = function(data)
{
    alert("Migration complete");
}

migrate.perform_migration = function()
{
    if (confirm("This will migrate the dbase, are you sure?"))
        network.post("/migrate", {"migrate": "yes"}, network.migration_complete);
}


function init()
{
    $("#migrate").click(migrate.perform_migration);
}

$(document).ready(init)
