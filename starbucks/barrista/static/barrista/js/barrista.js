
var barrista = {};

barrista.OrderGui = function(order_div)
{
    this.orders_div = order_div;
}

barrista.OrderGui.prototype.show = function()
{
    this.orders_div.empty();
    this.load_orders();
}

barrista.OrderGui.prototype.load_orders = function()
{
    var self = this;
    network.get("/orders", function(data){
        self.orders_loaded(data);
    });
}

barrista.OrderGui.prototype.orders_loaded = function(data)
{
    for (var o in data)
    {
        var order = data[o];
        this.orders_div.append($("<div>", {"class": "order", "text": order.product_id}));
    }
}

function init()
{
    console.log("Init");
    var orders_div = $("#orders");
    var gui = new barrista.OrderGui(orders_div)
    gui.show();
}

$(document).ready(init)
