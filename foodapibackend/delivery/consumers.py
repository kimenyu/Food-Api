import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DeliveryTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.delivery_group_name = f"delivery_{self.order_id}"

        await self.channel_layer.group_add(
            self.delivery_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.delivery_group_name,
            self.channel_name
        )

    async def send_delivery_update(self, event):
        await self.send(text_data=json.dumps(event))
