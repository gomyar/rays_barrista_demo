rays_barrista_demo
==================

Small demo app

So I reckoned I'd go with the Get a Cup of Coffee demo that's so popular at the moment.
It's a cut down version (didn't add optional toppings for example).

So anyway this demo starts out as a sqlite-backed django app which allows a barrista to add orders for customers,
and lets them select when each order is done.

The point of the demo is mainly to show off a python version of the Container pattern, which is popular in javaland.

Turns out it's really easy to put together a simple and effective Container using the json module and a couple of encoding/decoding hooks.

I like this pattern for non-rel backends as it allows embedding and complex domains very easily. It's quick to extend and can put together any
object structure you like. The control over how your domain is loaded/saved is encapsulated in this one class.

As you can see in this example, the container is used for communicating with both the old relational backend (django models)
and the new mongo backend simultaneously.

The assumption is that you can have both dbases on the go, but it'll only be writing to Mongo.

The /migrate url is used when you feel like migrating the data wholesale.
