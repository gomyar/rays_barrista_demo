
var barrista = {};

barrista.orders_div = null;
barrista.customer_orders_div = null;
barrista.order_form = null;

barrista.products = {};
barrista.orders = [];

barrista.show = function()
{
    barrista.orders_div.empty();
    barrista.customer_orders_div = $("<div>", {"id": "customer_orders"});
    barrista.order_form = $("<div>", {"id": "order_form"});
    barrista.orders_div.append(
        $("<div>", {"id": "leftcolumn"}).append(
            barrista.customer_orders_div
        ),
        $("<div>", {"id": "rightcolumn"}).append(
            barrista.order_form
        )
    );
    barrista.load_products();
}

barrista.load_products = function()
{
    network.get("/products", function(data){
        barrista.products_loaded(data);
        barrista.load_orders();
        barrista.show_order_form();
    });
}

barrista.products_loaded = function(data)
{
    barrista.products = data;
}

barrista.load_orders = function()
{
    network.get("/orders", function(data){
        barrista.orders_loaded(data);
    });
}

barrista.orders_loaded = function(data)
{
    for (var o in data)
    {
        var order = data[o];
        barrista.customer_orders_div.append(
            $("<div>", {"class": "order", "id": "order_" + order.order_id}).append(
                $("<div>", {"class": "product", "text": this.products[order.product_id]}),
                $("<div>", {"class": "for", "text": "for"}),
                $("<div>", {"class": "customer", "text": order.customer_name}),
                $("<button>", {"class": "order_served", "text": "Served"}).bind("click", {"order_id": order.order_id}, (function(e){
                    barrista.send_order_made(e.data.order_id);
                }))
            )
        );
    }
}

barrista.reload_orders = function()
{
    barrista.customer_orders_div.empty();
    barrista.load_orders()
}

barrista.send_order_made = function(order_id)
{
    network.post("/orders/" + order_id, {"action": "made"}, barrista.reload_orders);
}

barrista.show_order_form = function()
{
    barrista.order_form.append(
        $("<div>", {"id": "order_form"}).append(
            $("<div>", {"class": "field"}).append(
                $("<div>", {"class": "name", "text": "Product"}),
                barrista.build_products_select()
            ),
            $("<div>", {"class": "field"}).append(
                $("<div>", {"class": "name", "text": "Customer"}),
                $("<input>", {"class": "customer"})
            ),
            $("<div>", {"class": "field"}).append(
                $("<button>", {"class": "submit_order", "text": "Submit"}).click(barrista.submit_order)
            )
        )
    );
}

barrista.submit_order = function()
{
    var product_id = $("#order_form .products").find(":selected").val();
    var customer_name = $("#order_form .customer").val();
    console.log("Adding order: " + product_id + " " + customer_name);
    network.post("/orders", {"product_id": product_id, "customer_name": customer_name}, barrista.reload_orders);
}

barrista.build_products_select = function()
{
    var products_select = $("<select>", {"class": "products"});
    for (var product_id in barrista.products)
    {
        var product_name = barrista.products[product_id];
        products_select.append(
            $("<option>", {"class": "product", "value": product_id, "text": product_name})
        );
    }
    return products_select;
}

function init()
{
    console.log("Init");
    barrista.orders_div = $("#main");
    barrista.show();
}

$(document).ready(init)
