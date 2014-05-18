
var barrista = {};

barrista.OrderGui = function(order_div)
{
    this.orders_div = order_div;
}

barrista.OrderGui.prototype.show = function()
{
    this.orders_div.empty();
    this.customer_orders = $("<div>", {"id": "customer_orders"});
    this.order_form = $("<div>", {"id": "order_form"});
    this.orders_div.append(
        $("<div>", {"id": "leftcolumn"}).append(
            this.customer_orders
        ),
        $("<div>", {"id": "rightcolumn"}).append(
            this.order_form
        )
    );
    this.load_products();
}

barrista.OrderGui.prototype.load_products = function()
{
    var self = this;
    network.get("/products", function(data){
        self.products_loaded(data);
        self.load_orders();
        self.show_order_form();
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
    var self = this;
    for (var o in data)
    {
        var order = data[o];
        this.customer_orders.append(
            $("<div>", {"class": "order", "id": "order_" + order.order_id}).append(
                $("<div>", {"class": "product", "text": this.products[order.product_id]}),
                $("<div>", {"class": "for", "text": "for"}),
                $("<div>", {"class": "customer", "text": order.customer_name}),
                $("<button>", {"class": "order_served", "text": "Served"}).bind("click", {"order_id": order.order_id}, (function(e){
                    self.send_order_made(e.data.order_id);
                    $("#order_" + e.data.order_id).remove();
                }))
            )
        );
    }
}

barrista.OrderGui.prototype.send_order_made = function(order_id)
{
    network.post("/orders/" + order_id, {"action": "made"});
}

barrista.OrderGui.prototype.show_order_form = function()
{
    this.order_form.append(
        $("<div>", {"id": "order_form"}).append(
            $("<div>", {"class": "field"}).append(
                $("<div>", {"class": "name", "text": "Product"}),
                this.build_products_select()
            ),
            $("<div>", {"class": "field"}).append(
                $("<div>", {"class": "name", "text": "Customer"}),
                $("<input>", {"class": "customer"})
            ),
            $("<div>", {"class": "field"}).append(
                $("<button>", {"class": "submit_order", "text": "Submit"}).click(this.submit_order)
            )
        )
    );
}

barrista.OrderGui.prototype.submit_order = function()
{
    var product_id = $("#order_form .products").find(":selected").val();
    var customer_name = $("#order_form .customer").val();
    console.log("Adding order: " + product_id + " " + customer_name);
    network.post("/orders", {"product_id": product_id, "customer_name": customer_name});
}

barrista.OrderGui.prototype.build_products_select = function()
{
    var products_select = $("<select>", {"class": "products"});
    for (var product_id in this.products)
    {
        var product_name = this.products[product_id];
        products_select.append(
            $("<option>", {"class": "product", "value": product_id, "text": product_name})
        );
    }
    return products_select;
}

function init()
{
    console.log("Init");
    gui = new barrista.OrderGui($("#main"))
    gui.show();
}

$(document).ready(init)
