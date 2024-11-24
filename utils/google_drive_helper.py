from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import streamlit as st
import os
import io
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Google Drive 認證"""
    creds = None
    
    # 檢查是否已有已保存的憑證
    if 'google_creds' in st.session_state:
        creds = st.session_state.google_creds
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 保存憑證到 session state
        st.session_state.google_creds = creds
    
    return creds

def upload_to_drive(file_content, filename, mime_type, folder_id=None):
    """上傳檔案到 Google Drive"""
    try:
        creds = authenticate_google_drive()
        service = build('drive', 'v3', credentials=creds)
        
        # 準備檔案元數據
        file_metadata = {'name': filename}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # 創建媒體上傳物件
        fh = io.BytesIO(file_content.encode('utf-8') if isinstance(file_content, str) else file_content)
        media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=True)
        
        # 執行上傳
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        return file.get('webViewLink')
        
    except Exception as e:
        st.error(f"上傳到 Google Drive 時發生錯誤: {str(e)}")
        return None 