import os
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        base_dir = self.location  # Absolute media root
        full_path = os.path.join(base_dir, name)
        dir_name, base_filename = os.path.split(full_path)
        basename, _ = os.path.splitext(base_filename)

        # Delete any files in the same directory with the same basename but any extension
        if os.path.exists(dir_name):
            for f in os.listdir(dir_name):
                f_base, f_ext = os.path.splitext(f)
                if f_base == basename:
                    try:
                        os.remove(os.path.join(dir_name, f))
                    except Exception:
                        pass  # Optionally log this

        return name

    