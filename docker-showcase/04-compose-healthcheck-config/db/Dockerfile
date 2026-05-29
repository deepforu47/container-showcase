FROM postgres:15-alpine

# In this setup, we do not hardcode default credentials in the image metadata.
# This makes the image reusable across environment layers (dev, staging, prod),
# shifting configuration values entirely to Compose dynamic inputs (.env).

EXPOSE 5432
