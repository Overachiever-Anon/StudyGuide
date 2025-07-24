import os

def inspect_artifacts():
    """
    Initializes the Flask app, enters its context, and then queries the database.
    This order is crucial to prevent SQLAlchemy from registering models twice.
    """
    # Import create_app here to avoid premature loading
    from .app import create_app
    app = create_app()

    with app.app_context():
        # Import models only after the app context is available
        from .models import Artifact
        
        print("--- Querying Artifacts Table ---")
        try:
            artifacts = Artifact.query.all()
            if not artifacts:
                print("No artifacts found in the database.")
                return

            for artifact in artifacts:
                print(f"\n--- Artifact ID: {artifact.id} ---")
                print(f"Title: {artifact.title}")
                print(f"Type: {artifact.artifact_type}")
                code_length = len(artifact.react_code) if artifact.react_code else 0
                print(f"React Code Length: {code_length}")
                if code_length > 0:
                    print(f"React Code Snippet: {artifact.react_code[:500]}...")
                else:
                    print("React Code: IS EMPTY OR NULL")
                print("---------------------------------")

        except Exception as e:
            print(f"An error occurred while querying the database: {e}")

if __name__ == '__main__':
    inspect_artifacts()
