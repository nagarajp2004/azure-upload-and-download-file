import streamlit as st
import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import BytesIO


# Azure Storage account details
azure_account_storage_account = "  "
azure_storage_account_key = "  "
container = "somedata"

# Function to upload a file to Azure Blob Storage
def upload_to_azure_storage(file):
    try:
        # Connect to BlobService
        blob_service_client = BlobServiceClient.from_connection_string(
            f"DefaultEndpointsProtocol=https;AccountName={azure_account_storage_account};AccountKey={azure_storage_account_key}"
        )
        # Get the blob client
        blob_client = blob_service_client.get_blob_client(container=container, blob=file.name)
        # Upload the file
        blob_client.upload_blob(file, overwrite=True)
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        raise e

# Function to list blobs in the container
def list_blob():
    try:
        # Connect to BlobService
        blob_service_client = BlobServiceClient.from_connection_string(
            f"DefaultEndpointsProtocol=https;AccountName={azure_account_storage_account};AccountKey={azure_storage_account_key}"
        )
        # Get the container client
        container_client = blob_service_client.get_container_client(container)
        # List and return blob names
        blobs = [blob.name for blob in container_client.list_blobs()]
        return blobs
    except Exception as e:
        st.error(f"Error listing blobs: {e}")
        return []

# Streamlit UI
st.title("Azure Blob Storage Manager")

# File uploader
upload = st.file_uploader("Choose a file to upload")
if upload is not None:
    try:
        upload_to_azure_storage(upload)
        st.success(f"File '{upload.name}' uploaded to Azure Blob Storage.")
    except Exception as e:
        st.error(f"Failed to upload file: {e}")

# List blobs in the container
st.subheader("Available Blobs")
blobs = list_blob()
if blobs:
    st.write("The following files are available in the container:")
    for blob_name in blobs:
        st.write(f"- {blob_name}")
else:
    st.write("No blobs found in the container.")
