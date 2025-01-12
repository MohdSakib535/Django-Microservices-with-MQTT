from django.http import JsonResponse
from .models import Order, Product
from .mqtt_publisher import MqttPublisher



def publish_order(order_id, product_id, quantity):
    """Helper function to publish the order to MQTT."""
    mqtt_publisher = MqttPublisher(topic="orders")
    mqtt_publisher.connect()
    
    # Create the message payload
    message = {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
    }
    
    mqtt_publisher.publish(message)
    mqtt_publisher.disconnect()





def place_order(request):
    """API endpoint to place an order."""
    product_id = request.GET.get("product_id")
    quantity = int(request.GET.get("quantity"))

    try:
        product = Product.objects.get(id=product_id)
        if product.stock < quantity:
            return JsonResponse({"error": "Not enough stock"}, status=400)

        order = Order.objects.create(product=product, quantity=quantity)
        product.stock -= quantity  # Reduce stock
        product.save()

        # Publish order to MQTT
        publish_order(order.id, product.id, quantity)

        return JsonResponse({"status": "Order placed", "order_id": order.id})

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product

@csrf_exempt
def update_inventory(request):
    """API endpoint for Inventory Service to update stock."""
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        try:
            product = Product.objects.get(id=product_id)
            product.stock -= quantity  # Reduce stock
            product.save()
            return JsonResponse({"status": "Inventory updated"})

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)
