# ============================================================
# AWS Configuration
# ============================================================
# Update these values ONCE here, and all notebooks will use them.
# Get your credentials from the Cloud Resources panel in Udacity.
# ============================================================

import os

# ========= AWS CREDENTIALS =========
# Copy these from your Cloud Resources panel
os.environ['AWS_ACCESS_KEY_ID'] = 'ASIA54I5TRBEW7K2OYDQ'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'zLg/sSvswNcZg+FEGT9/jcUmcD0wbecywYKMMcio'
os.environ['AWS_SESSION_TOKEN'] = 'IQoJb3JpZ2luX2VjEOv//////////wEaCXVzLXdlc3QtMiJIMEYCIQCyuQ65x8njPJD8qtA7lTfuV6Sg1neADElJySg2CG2rowIhAIT5F4gDeCGsaMpcBURhAAl569QEcL4LkAjJpeBTOBOhKq0CCLT//////////wEQAxoMOTU0MDgxNzA4MTA1IgxVj4awZUdurMemIZ8qgQKtfyuux5ZvMcnpEa/HyEEyJBSF0LeXI+sGyaNVxScLr6raglldGeRMFA69JDrUGWFFyzBKn8F0KYtwtE1CRf3dVU/F6ETWcHOqggc/8Dwrx8M3mKiEMQA8JpuOdF7QVPYN7XbQxMLGvuQd6y39YDaEOZHMoTiyc4W9HTWMTsnQeiHvhLEv6bdE7p38172EZ0D/2ye0h537X2Q90bPKglYII9Y5fJxacmWEoy06SAe3GwoWBXCjQ5bsFi90telXyKINjhMUVkP6emusAkeX5Pl+9GjgU4h+D+AiFwRnLV3iM7zGN9yR7itscTH3Hb7WXbEM5drgCruV/IvPy6XJP1UlBjC5u5bKBjqcAZqJkwzJ1Ys8H8TZ7AkAJCi/b5+FYNF6Bgj9Jz2Y8RwL+0esc/y5pLbI/nu3JZ00AfW2iCoiUOX4o5GwxlIwIcPk92BMEzzQUC8YoZIBH4L+X4TuglNFGcbZnbF7KNBAvwdFTOuFyqNJvUCPaudLx8LKj3p7RVD1eYdyq49N31g/EiBWN8y7kwJi4N9EsX1KkrS2+ymazqw7sHyRYw=='

# Database information
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['REDSHIFT_DATABASE'] = 'dev'
os.environ['REDSHIFT_WORKGROUP'] = 'udacity-dwh-wg'
