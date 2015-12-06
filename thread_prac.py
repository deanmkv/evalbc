import threading
import time

def work(*args, **kwargs):
	print(args, kwargs)
	diag(threading.current_thread())
	time.sleep(10)


def diag(thing):
	print("~~~~~~~~~~~~~~")
	print(thing.ident)
	print(threading.get_ident())
	print(thing.name)
	print(thing.daemon)
	print("~~~~~~~~~~~~~~")

thing = threading.Thread(target=work, args=(10,), daemon=True)

diag(thing)
print("Started thread")
thing.start()
# diag(thing)

print(threading.enumerate())

thing.join()
print("done joining")