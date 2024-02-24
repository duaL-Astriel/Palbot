import socket, psutil

def udp_ping(ip, port):
  """
  Sends a UDP ping to the specified IP and port and returns True if a 
  response is received within the timeout, False otherwise.
  """
  # Create a new socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  # Set a timeout so the socket doesn't block indefinitely
  sock.settimeout(1)

  try:
    # Send a message to the server
    message = b'PING'
    sock.sendto(message, (ip, port))

    # Receive a response with timeout handling
    try:
      sock.recvfrom(1024)
      return True  # Return True on successful response
    except socket.timeout:
      print("Timeout")
      return False  # Return False on timeout

  except Exception as e:
    print(f"An error occurred: {e}")
    return False  # Return False on any other exceptions

  finally:
    sock.close()


def is_application_running(name):
  """
  Checks if an application is running by name.

  Args:
      name: The name of the application (e.g., "notepad.exe").

  Returns:
      True if the application is running, False otherwise.
  """
  # Iterate through all processes
  for process in psutil.process_iter():
    # Check if process name matches the provided name
    if process.name() == name:
      return True
  return False