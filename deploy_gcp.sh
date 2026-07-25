#!/bin/bash
# GCP Cloud Run deployment script for AIMap Platform
# Cost Optimization: Min instances = 0 ensures $0 cost when idle.

set -e

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")

if [ -z "$PROJECT_ID" ]; then
  echo "Error: No active GCP project set. Run 'gcloud config set project YOUR_PROJECT_ID' first."
  exit 1
fi

SERVICE_NAME="aimap-interview-platform"
REGION="us-central1"

echo "=========================================="
echo "Deploying AIMap Platform to GCP Cloud Run"
echo "GCP Project ID: $PROJECT_ID"
echo "Region:         $REGION"
echo "Service Name:   $SERVICE_NAME"
echo "=========================================="

# Build container image using Cloud Build
gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME:latest" .

# Deploy to Cloud Run with low-cost settings
gcloud run deploy "$SERVICE_NAME" \
  --image "gcr.io/$PROJECT_ID/$SERVICE_NAME:latest" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 3 \
  --memory 512Mi \
  --cpu 1 \
  --port 8501

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
