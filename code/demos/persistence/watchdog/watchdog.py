#!/usr/bin/env python3

import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class PrettyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"👀 Event detected:\n  Type:   {event.event_type}\n  Path:   {event.src_path}\n"
              f"  Is Dir: {event.is_directory}")
        if hasattr(event, "dest_path") and event.dest_path:
            print(f"  Dest:   {event.dest_path}")


def main():
    event_handler = PrettyEventHandler()
    observer = Observer()
    watch_path = "."
    print(f"🔍 Watching for file system events in: {watch_path} (recursive)")
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping observer...")
    finally:
        observer.stop()
        observer.join()
        print("✅ Observer stopped.")


if __name__ == "__main__":
    main()
