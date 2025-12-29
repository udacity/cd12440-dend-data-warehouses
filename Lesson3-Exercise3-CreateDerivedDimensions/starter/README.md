# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to build a derived fare class dimension that categorizes continuous fare values into analytical buckets. You'll define classification rules, apply them to trip data, and create a reusable dimension table for the warehouse.

- [ ] Define fare bucket thresholds (Budget: $0-$3, Standard: $3-$4.50, Premium: $4.50-$6.50, Luxury: $6.50+) and discount band thresholds (Full Price: 0%, Light: 1-19%, Moderate: 20-34%, Heavy: 35%+)

- [ ] Implement `classify_fare()` and `classify_discount()` helper functions that categorize continuous values into buckets, handling NaN values by returning 'Unknown'

- [ ] Extract fare data from PostgreSQL and apply the classification functions to create `fare_bucket` and `discount_band` columns, then analyze the distribution with value counts and cross-tabulation

- [ ] Build the dimension table by finding unique fare bucket/discount band combinations, adding a composite `fare_class_code` (e.g., 'STA_FULL'), descriptive labels, fare range descriptions, and warehouse metadata (`fare_class_sk`, `created_at`, `is_current`)

- [ ] Validate that all trips can be classified (zero unclassified fares/discounts), then output the dimension to CSV and generate documentation