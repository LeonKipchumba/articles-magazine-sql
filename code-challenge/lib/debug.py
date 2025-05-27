import code

if __name__ == "__main__":
    print("Interactive debug session. Models and DB are available.")
    vars = globals().copy()
    try:
        from lib.models.author import Author
        from lib.models.magazine import Magazine
        from lib.models.article import Article
        vars.update({"Author": Author, "Magazine": Magazine, "Article": Article})
    except Exception as e:
        print(f"Warning: Could not import models: {e}")
    code.interact(local=vars)
