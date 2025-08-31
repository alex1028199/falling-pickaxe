import subprocess
import pygame
from config import config
from constants import INTERNAL_WIDTH, INTERNAL_HEIGHT, FRAMERATE

class Streamer:
    def __init__(self):
        # In a real-world scenario, you would get this from the config.
        # For now, we'll set a default for testing.
        self.stream_url = config.get("STREAM_URL", "output.mp4")

        command = [
            'ffmpeg',
            '-y',  # Overwrite output file if it exists
            # Video input
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'rgb24',
            '-s', f'{INTERNAL_WIDTH}x{INTERNAL_HEIGHT}',
            '-r', str(FRAMERATE),
            '-i', '-',  # Video input from stdin
            # Audio input
            '-f', 's16le', # Raw audio format
            '-ar', '44100', # Sample rate
            '-ac', '2', # Stereo channels
            '-i', 'sdlaudio.raw', # Audio input file
            # Sync options
            '-async', '1',
            '-vsync', 'cfr',
            # Output options
            '-c:v', 'libx264',
            '-c:a', 'aac', # Audio codec
            '-shortest', # Finish encoding when the shortest input stream ends
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'mp4' if self.stream_url.endswith(".mp4") else "flv",
            self.stream_url
        ]

        # The Popen command should be structured to handle stdin, stdout, and stderr.
        # We only need stdin for this use case.
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def write_frame(self, surface):
        """Writes a single frame to the ffmpeg process."""
        if not self.process:
            return

        try:
            # Get the raw pixel data from the pygame surface
            frame_data = pygame.image.tostring(surface, 'RGB')
            self.process.stdin.write(frame_data)
        except (BrokenPipeError, IOError):
            # This can happen if ffmpeg closes the pipe
            print("ffmpeg process has closed the pipe. This may be expected on exit.")
            self.close()

    def close(self):
        """Closes the ffmpeg process gracefully."""
        if self.process:
            # Closing stdin will signal ffmpeg to finalize the video
            if self.process.stdin:
                self.process.stdin.close()

            # Wait for the process to terminate
            self.process.wait()
            self.process = None
            print("ffmpeg process closed.")
