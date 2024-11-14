import os
import random
import config


async def get_random_gif() -> None or str:
    media_folder_files = os.listdir(config.MEDIA_FOLDER)
    media_files = [f for f in media_folder_files if
                   f.lower().endswith('.gif') and os.path.isfile(os.path.join(config.MEDIA_FOLDER, f))]

    if not media_files:
        return None
    else:
        random_file = random.choice(media_files)
        random_file_path = os.path.join(config.MEDIA_FOLDER, random_file)
        return random_file_path
