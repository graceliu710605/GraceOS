from pathlib import Path


def analyze(folder, top_n=10):

    files = []

    root = Path(folder)

    try:

        for file in root.rglob("*"):

            if file.is_file():

                try:

                    size = file.stat().st_size

                    files.append(
                        {
                            "name": file.name,
                            "path": str(file),
                            "size_mb": round(size / 1024 / 1024, 2)
                        }
                    )

                except:
                    pass

    except:
        return []

    files.sort(
        key=lambda x: x["size_mb"],
        reverse=True
    )

    return files[:top_n]