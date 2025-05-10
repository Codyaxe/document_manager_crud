from document import Slideshow, Document
import pickle
import os

def test_slideshow_save_and_structure():
    # Cleanup previous save if exists
    if os.path.exists("files/docs"):
        os.remove("files/docs")

    # Garbage Collector
    Document.saved_documents.clear()

    # Create a SlideShow
    ss = Slideshow("My Presentation", "Codyaxe", "Some content", 3)

    ss.slides = ["Hello", "BOI", None]

    ss.print()

    # Check size and slides
    assert ss._size == 3
    assert len(ss._slides) == 3

    # Call save and verify file creation
    os.makedirs("files", exist_ok=True)
    ss.save()
    assert os.path.exists("files/docs")

    # Load and verify contents
    with open("files/docs", "rb") as f:
        loaded_docs = pickle.load(f)
        print(loaded_docs)
        assert ss in loaded_docs
        assert isinstance(loaded_docs[-1], SlideShow)

    print("SlideShow test passed.")

test_slideshow_save_and_structure()