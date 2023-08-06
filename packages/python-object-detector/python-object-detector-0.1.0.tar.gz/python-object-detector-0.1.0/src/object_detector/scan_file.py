from src.object_detector import scan_buffer


def scan_file(path):
    """Scans image file with object detector.

    :param path: Path to image file.
    :return: Detection result.
    """
    with open(path, "rb") as file_in:
        buffer = file_in.read()

    with open(path + ".out", "w") as file_out:
        out = scan_buffer(buffer)
        file_out.write(out)
