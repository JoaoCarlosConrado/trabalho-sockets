import threading

import sensors.temperature as t
import sensors.humidity as h
import sensors.co2 as c

# Create the threads
temperature_thread = threading.Thread(target=t.execute)
humidity_thread = threading.Thread(target=h.execute)
co2_thread = threading.Thread(target=c.execute)

# Start the threads
temperature_thread.start()
humidity_thread.start()
co2_thread.start()

# Wait for all threads to finish
temperature_thread.join()
humidity_thread.join()
co2_thread.join()