import asyncio
from pathlib import Path
from typing import Any

import aiofiles
import aiohttp

import os 
import dwani

import tempfile
dwani.api_key = os.getenv("DWANI_API_KEY")

dwani.api_base = os.getenv("DWANI_API_BASE_URL")


API_URL = "https://api.ai-coustics.com/v1"


api_key = os.getenv("SOUND_API_KEY")

async def upload_and_enhance(
    url: str,
    file_path: Path,
    arguments: dict[str, Any],
) -> str:
    form_data = aiohttp.FormData()
    for field_name, field_value in arguments.items():
        form_data.add_field(field_name, str(field_value))

    async with aiofiles.open(file_path, "rb") as file:
        form_data.add_field(
            "file",
            file,
            content_type="application/octet-stream",
            filename=file_path.name,
        )

        async with aiohttp.ClientSession(
            headers={"X-API-Key": api_key}
        ) as session:
            async with session.post(url, data=form_data) as response:
                if response.status != 201:
                    response_text = await response.text()
                    print(f"Error occured: {response_text}")
                    return None

                response_json = await response.json()
                generated_name = response_json["generated_name"]
                print(f"Uploaded file's generated name: {generated_name}")
                return generated_name


def main(file_path: Path, arguments: dict[str, Any]) -> None:
    url = f"{API_URL}/media/enhance"

    asyncio.run(
        upload_and_enhance(
            url,
            file_path,
            arguments,
        )
    )


if __name__ == "__main__":


    response = dwani.Audio.speech(input = "what is your name? I am sachin from Bonn", response_format="mp3", language="english")
    file_path = Path("sound-input.mp3")
    with open(file_path, "wb") as f:
        f.write(response)

    file_path = Path("sound-input.mp3")
    arguments = {
        "loudness_target_level": -14,
        "loudness_peak_limit": -1,
        "enhancement_level": 1.0,
        "transcode_kind": "MP3",
    }
    main(file_path, arguments)