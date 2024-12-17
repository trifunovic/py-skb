import os
import subprocess

# Install en_core_web_sm model
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])