import os
import logging
from PIL import Image
from celery import shared_task
from django.core.files import File
from django.conf import settings
from process_images.models import ProcessedImage

logger = logging.getLogger(__name__)

# Folder inside MEDIA_ROOT
OUTPUT_FOLDER = os.path.join(settings.MEDIA_ROOT, "processed_images")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def run_ml_model(image_path):
    logger.info(f"Running ML inference for: {image_path}")
    return "dummy_result"


@shared_task(bind=True)
def process_image(self, batch):

    worker = self.request.hostname

    logger.info(f"[Worker {worker}] ===== Batch started | size={len(batch)} =====")

    successful = 0
    failed = 0

    for path, filename in batch:

        logger.info(f"[Worker {worker}] Processing image: {filename}")

        try:
            # Step 1: Open image
            img = Image.open(path)
            logger.info(f"[Worker {worker}] Image opened: {path}")

            # Step 2: Resize
            img = img.resize((256, 256))
            logger.info(f"[Worker {worker}] Image resized: {filename}")

            # Step 3: Save image locally
            save_path = os.path.join(OUTPUT_FOLDER, filename)
            img.save(save_path)
            logger.info(f"[Worker {worker}] Saved image: {save_path}")

            # Step 4: ML inference
            result = run_ml_model(save_path)
            logger.info(f"[Worker {worker}] ML result for {filename}: {result}")

            # Step 5: Save to PostgreSQL
            try:
                processed, created = ProcessedImage.objects.get_or_create(
                    filename=filename
                )

                with open(save_path, "rb") as f:
                    processed.image_file.save(filename, File(f), save=True)

                logger.info(
                    f"[Worker {worker}] DB SAVE SUCCESS | filename={filename} | created={created}"
                )

            except Exception as db_error:
                logger.error(
                    f"[Worker {worker}] DB SAVE FAILED | filename={filename} | error={db_error}"
                )
                raise db_error

            successful += 1

        except Exception as e:

            failed += 1

            logger.error(
                f"[Worker {worker}] FAILED | filename={filename} | path={path} | error={str(e)}"
            )

    logger.info(
        f"[Worker {worker}] ===== Batch completed | success={successful} | failed={failed} ====="
    )