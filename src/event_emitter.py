import logging
import asyncio
from typing import Callable, Dict, List, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EventEmitter:
    def __init__(self):
        self.events: Dict[str, List[Tuple[int, Callable[[Any], None]]] ] = {}  # Event name -> list of (priority, listener)

    def on(self, event: str, listener: Callable[[Any], None], priority: int = 0) -> None:
        """Register a listener for a specific event with an optional priority."""
        if event not in self.events:
            self.events[event] = []
        self.events[event].append((priority, listener))
        self.events[event].sort(key=lambda x: x[0], reverse=True)  # Higher priority first
        logging.info(f"Listener registered for event: {event} with priority: {priority}")

    async def _emit_listener(self, listener: Callable[[Any], None], data: Any) -> None:
        """Execute a listener asynchronously."""
        try:
            if asyncio.iscoroutinefunction(listener):
                await listener(data)
            else:
                listener(data)
        except Exception as e:
            logging.error(f"Error while executing listener: {listener.__name__} for event: {data}: {e}")

    async def emit(self, event: str, data: Any) -> None:
        """Emit an event, calling all registered listeners asynchronously."""
        if event in self.events:
            logging.info(f"Emitting event: {event} with data: {data}")
            await asyncio.gather(*(self._emit_listener(listener, data) for _, listener in self.events[event]))
        else:
            logging.warning(f"No listeners registered for event: {event}")

    def remove_listener(self, event: str, listener: Callable[[Any], None]) -> None:
        """Remove a specific listener for an event."""
        if event in self.events:
            self.events[event] = [(priority, l) for priority, l in self.events[event] if l != listener]
            logging.info(f"Listener removed for event: {event}")

    def clear_event(self, event: str) -> None:
        """Clear all listeners for a specific event."""
        if event in self.events:
            del self.events[event]
            logging.info(f"All listeners cleared for event: {event}")

# Example usage of the EventEmitter class
async def main():
    emitter = EventEmitter()

    # Define a sample listener
    async def on_stake(data: Any) -> None:
        logging.info(f"Stake event received with data: {data}")

    # Register the listener for the 'stake' event with priority 1
    emitter.on('stake', on_stake, priority=1)

    # Emit a 'stake' event
    await emitter.emit('stake', {'user': 'user1', 'amount': 100.0})

    # Emit an event with no listeners
    await emitter.emit('unknown_event', {'info': 'This should not trigger any listener.'})

    # Remove the listener
    emitter.remove_listener('stake', on_stake)

    # Emit the 'stake' event again to confirm listener removal
    await emitter.emit('stake', {'user': 'user1', 'amount': 100.0})

    # Clear all listeners for the 'stake' event
    emitter.clear_event('stake')

if __name__ == "__main__":
    asyncio.run(main())
