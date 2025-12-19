# ============================================================
# AWS Configuration
# ============================================================
# Update these values ONCE here, and all notebooks will use them.
# Get your credentials from the Cloud Resources panel in Udacity.
# ============================================================

import os

# ========= AWS CREDENTIALS =========
# Copy these from your Cloud Resources panel (set them as environment variables before running)
os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID', '')
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY', '')
os.environ['AWS_SESSION_TOKEN'] = os.getenv('AWS_SESSION_TOKEN', '')

# Database information
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['REDSHIFT_DATABASE'] = 'dev'
os.environ['REDSHIFT_WORKGROUP'] = 'udacity-dwh-wg'
