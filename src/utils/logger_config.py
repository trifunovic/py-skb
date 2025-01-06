import logging
import platform
import psutil  # Make sure `psutil` is installed for system info

class AppLogger:
    def __init__(self, log_level=logging.DEBUG):
        self.logger = logging.getLogger("fastapi_app")
        self.logger.setLevel(log_level)

        # Console handler with custom format
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(console_handler)

    def log_system_info(self):
        """
        Logs system information such as OS, memory, and CPU usage.
        """
        try:
            self.logger.debug("\n=== System Information ===")
            self.logger.debug(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
            self.logger.debug(f"Architecture: {platform.architecture()[0]}")
            self.logger.debug(f"Processor: {platform.processor()}")
            self.logger.debug(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
            self.logger.debug(f"Memory: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB total")
            self.logger.debug(f"Free Memory: {round(psutil.virtual_memory().available / (1024 ** 3), 2)} GB")
            self.logger.debug(f"Disk Usage: {psutil.disk_usage('/').percent}% used of {round(psutil.disk_usage('/').total / (1024 ** 3), 2)} GB")
            self.logger.debug("==========================")
        except ImportError:
            self.logger.warning("System info utilities not available in this environment.")
        except Exception as e:
            self.logger.error(f"Error printing system info: {e}")
