import datetime
import os
import socket
import zipfile

async def zip_and_backup_palworld():
    folder_path = "C:\\Users\\Plex\\Desktop\\Palworld\\steamapps\\common\\PalServer\\Pal\\Saved"
    zip_destination_path = "\\NAS01\Austausch\\backups\Palworld"
    port = 8211

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:  # Check port connectivity
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
            zip_file_path = os.path.join(zip_destination_path, f"Lunas_Palworld_{current_datetime}.zip")

            if os.path.exists(zip_file_path):
                return

            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, folders, files in os.walk(folder_path):
                    for file in files:
                        zipf.write(os.path.join(root, file))
