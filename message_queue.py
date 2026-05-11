"""
Message Queue - Complete Implementation

Message queue with:
- Pub/Sub
- Task queues
- Message types
- Retry logic
- Dead letter queue

Reference:
- RabbitMQ: https://www.rabbitmq.com/
- Redis: https://redis.io/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import uuid


# =============================================================================
# TYPES
# =============================================================================

class MessagePriority(Enum):
    LOW = 1
    NORMAL = 5
    HIGH = 10


class MessageStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"
    DEAD = "dead"


# =============================================================================
# MESSAGE
# =============================================================================

@dataclass
class Message:
    """Message"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    topic: str = ""
    payload: Any = None
    
    priority: MessagePriority = MessagePriority.NORMAL
    
    status: MessageStatus = MessageStatus.PENDING
    
    # Retry
    retry_count: int = 0
    max_retries: int = 3
    
    # Timing
    created_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Headers
    headers: Dict[str, Any] = field(default_factory=dict)
    
    # Error
    error: Optional[str] = None
    
    # Correlation
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    
    def ack(self):
        """Acknowledge message"""
        self.status = MessageStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def nack(self, error: str = None):
        """Negative acknowledge"""
        if error:
            self.error = error
        
        if self.retry_count < self.max_retries:
            self.status = MessageStatus.RETRY
            self.retry_count += 1
        else:
            self.status = MessageStatus.DEAD
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "topic": self.topic,
            "payload": self.payload,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat()
        }


# =============================================================================
# QUEUE
# =============================================================================

class MessageQueue:
    """Message queue"""
    
    def __init__(self, name: str):
        self.name = name
        
        self.messages: List[Message] = []
        
        self.dead_letter: List[Message] = []
        
        self.handlers: Dict[str, Callable] = {}
        
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def publish(self, topic: str, payload: Any, priority: MessagePriority = MessagePriority.NORMAL):
        """Publish message"""
        message = Message(topic=topic, payload=payload, priority=priority)
        self.messages.append(message)
        
        # Notify subscribers
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)
        
        return message
    
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to topic"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
    
    def consume(self) -> Optional[Message]:
        """Get next message"""
        if not self.messages:
            return None
        
        # Sort by priority
        self.messages.sort(key=lambda m: m.priority.value, reverse=True)
        
        # Get highest priority
        message = self.messages.pop(0)
        message.status = MessageStatus.PROCESSING
        
        return message
    
    def process(self, handler: Callable) -> bool:
        """Process message with handler"""
        message = self.consume()
        
        if not message:
            return False
        
        try:
            handler(message)
            message.ack()
            return True
        except Exception as e:
            message.nack(str(e))
            
            if message.status == MessageStatus.DEAD:
                self.dead_letter.append(message)
            
            return False
    
    def size(self) -> int:
        return len(self.messages)
    
    def dead_size(self) -> int:
        return len(self.dead_letter)


# =============================================================================
# TOPIC
# =============================================================================

class Topic:
    """Pub/Sub topic"""
    
    def __init__(self, name: str):
        self.name = name
        self.subscribers: List[Callable] = []
        self.message_count: int = 0
    
    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable):
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def publish(self, message: Message):
        self.message_count += 1
        for callback in self.subscribers:
            callback(message)


# =============================================================================
# WORKER
# =============================================================================

class Worker:
    """Queue worker"""
    
    def __init__(self, name: str, queue: MessageQueue):
        self.name = name
        self.queue = queue
        self.running: bool = False
    
    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False
    
    def process(self, handler: Callable):
        """Process messages"""
        while self.running:
            message = self.queue.consume()
            
            if message:
                try:
                    handler(message)
                    message.ack()
                except Exception as e:
                    message.nack(str(e))
            else:
                # No messages, wait
                import time
                time.sleep(0.1)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Example"""
    
    print("=" * 50)
    print("Message Queue")
    print("=" * 50)
    
    # Create queue
    queue = MessageQueue("tasks")
    
    # Publish messages
    queue.publish("notifications", {"type": "email", "to": "user@example.com"})
    queue.publish("tasks", {"action": "process_data"})
    
    print(f"Queue size: {queue.size()}")
    
    # Subscribe
    def handler(msg: Message):
        print(f"Received: {msg.topic}")
    
    queue.subscribe("notifications", handler)
    
    # Consume
    msg = queue.consume()
    if msg:
        print(f"Processing: {msg.topic}")
        msg.ack()
        print(f"Status: {msg.status.value}")


if __name__ == "__main__":
    main()


"""
Message Queue Usage

    # Create queue
    queue = MessageQueue("tasks")
    
    # Publish
    queue.publish("notifications", {"type": "email", "to": "user@example.com"})
    
    # Subscribe
    queue.subscribe("notifications", lambda m: print(m.payload))
    
    # Consume
    msg = queue.consume()
    if msg:
        print(msg.payload)
        msg.ack()
    
    # Dead letter
    queue.dead_letter  # Failed messages
"""