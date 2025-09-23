from app_factory import create_app
from setup.config import settings

auth_app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        auth_app, host=settings.run.host, port=settings.run.port, reload=False
    )
