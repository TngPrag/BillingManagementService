from fs.fs import fs_open

def get_db():
    db = fs_open()
    try:
        yield db
    finally:
        db.close()