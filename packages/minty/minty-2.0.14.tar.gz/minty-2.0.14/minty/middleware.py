# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import amqpstorm  # type: ignore
import json
from .cqrs import MiddlewareBase


def AmqpPublisherMiddleware(
    publisher_name: str, infrastructure_name: str = "amqp"
):
    """Return  `_AMQPPublisherClass` instantiated given params.

    :param publisher_name: name of publisher to get from config
    :type publisher_name: str
    :param infrastructure_name: name of amqp infrastructure, defaults to "amqp"
    :type infrastructure_name: str, optional
    :return: _AMQPPublisher middleware
    :rtype: _AMQPPublisher
    """

    class _AMQPPublisher(MiddlewareBase):
        """Publish all events in the event service to AMQP exchange."""

        def __call__(self, func):
            func()

            self.channel = self.infrastructure_factory.get_infrastructure(
                context=self.context, infrastructure_name=infrastructure_name
            )
            config = self.infrastructure_factory.get_config(
                context=self.context
            )
            publish_settings = config[infrastructure_name]["publish_settings"]
            exchange = publish_settings["exchange"]

            timer = self.statsd.get_timer("amqp_write_duration")
            counter = self.statsd.get_counter("amqp_write_number")

            for event in self.event_service.event_list:
                properties = {"content_type": "application/json"}
                event_content = json.dumps(
                    {
                        "id": str(event.uuid),
                        "created_date": event.created_date.isoformat(),
                        "correlation_id": str(self.correlation_id),
                        "context": event.context,
                        "domain": event.domain,
                        "user_uuid": str(event.user_uuid),
                        "entity_type": event.entity_type,
                        "entity_id": str(event.entity_id),
                        "event_name": event.event_name,
                        "changes": event.changes,
                        "entity_data": event.entity_data,
                    },
                    sort_keys=True,
                )
                message = amqpstorm.Message.create(
                    channel=self.channel,
                    body=event_content,
                    properties=properties,
                )
                formatted_domain = str(event.domain).replace(".", "_")
                routing_key = f"zsnl.v2.{formatted_domain}.{event.entity_type}.{event.event_name}"

                self.logger.debug(
                    f"Publishing event {event.uuid} on {routing_key} - "
                    + str(message.method)
                    + " - "
                    + str(message.properties)
                    + " - EXCHANGE: "
                    + exchange
                )

                with timer.time():
                    message.publish(routing_key=routing_key, exchange=exchange)

                counter.increment()

    return _AMQPPublisher
