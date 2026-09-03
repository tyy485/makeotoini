# Error Code Reference

When the program encounters an error, it will output an error code. Use the table below to find the corresponding error and solution.

## E001
Description: Folder not found.
Solution: Check the path and confirm the folder exists.

## E002
Description: No read permission.
Solution: Check folder permissions and ensure the program has read access.

## E003
Description: No audio files in the folder.
Solution: Confirm the folder contains wav, mp3, flac, or other audio files.

## E101
Description: WAV file is corrupted or has an unsupported format.
Solution: Re-convert the file using FFmpeg, or re-record the audio.

## E102
Description: Failed to read WAV file.
Solution: Check if the file is in use or incomplete.

## E103
Description: Unsupported audio format.
Solution: Convert to standard WAV format and try again.

## E201
Description: FFmpeg not installed.
Solution: Install FFmpeg from ffmpeg.org.

## E202
Description: FFmpeg conversion failed.
Solution: Check if the source file is intact, or convert manually.

## E203
Description: FFmpeg conversion timeout.
Solution: Try splitting large audio files, or check system performance.

## E301
Description: Encoding write failed.
Solution: Switch to UTF-8 encoding and retry.

## E302
Description: oto.ini write failed.
Solution: Check disk space and write permissions.

## E401
Description: User cancelled the operation.
Solution: Run the program again.

## E402
Description: Program was interrupted.
Solution: Run the program again.

## E501
Description: Invalid config file format.
Solution: Delete the config file and regenerate it.

## E502
Description: Config file version mismatch.
Solution: Re-export the config using the current version of the tool.

## E???
Description: Unknown error.
Solution: Contact the developer at tyy485@outlook.com and provide the error log.

If you encounter an unknown error, please contact me:
Email: tyy485@outlook.com
GitHub: https://github.com/tyy485