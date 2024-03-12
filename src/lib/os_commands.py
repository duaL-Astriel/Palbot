import os

async def shutdown_application(application_name: str):
    # Stop the service
    os.system(f"net stop {application_name}")

    # Optional: Check the exit code for success
    if os.system(f"net query {application_name}") == 0:
        print(f"Service {application_name} stopped successfully.")
    else:
        print(f"Error stopping service {application_name}.")
