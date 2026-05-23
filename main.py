from fastapi import FastAPI
import logging
import logging.config
from api.chat import router as chat_router

# Настройка логгера
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "standard"
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
})

logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Service")

@app.on_event("startup")
async def startup_event():
    logger.info("Приложение запущено")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Приложение остановлено")

app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)