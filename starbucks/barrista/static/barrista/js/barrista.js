
var barrista = {};

barrista.OrderGui = function(order_div)
{
    this.orders_div = order_div;
}

barrista.OrderGui.prototype.show = function()
{
    this.orders_div.empty();
    this.load_products();
}

barrista.OrderGui.prototype.load_products = function()
{
    var self = this;
    network.get("/products", function(data){
        self.products_loaded(data);
        self.load_orders();
    });
}

barrista.OrderGui.prototype.products_loaded = function(data)
{
    this.products = data;
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
        this.orders_div.append(
            $("<div>", {"class": "order", "text": this.products[order.product_id] + " for " + order.customer_name})
        );
    }
}

function init()
{
    console.log("Init");
    gui = new barrista.OrderGui($("#orders"))
    gui.show();
}

$(document).ready(init)
