# 音訊轉摘要系統

一個基於 AI 的應用程式，可將音訊檔轉換為全面的文字摘要，並支援雙語輸出。

## 功能特點
- 🎯 音訊轉文字（支援多種格式）
- 📝 自動生成中英文摘要
- 💡 產生雙語字幕檔（SRT 格式）
- 🤖 支援 GPT-4 和 GPT-4-turbo-preview 模型
- ⚙️ 可自訂系統提示詞
- 📊 進度追蹤和錯誤處理

## 系統需求
- Python 3.8+
- FFmpeg
- OpenAI API 金鑰
- 網路連線

## 安裝步驟
1. 複製專案

git clone https://github.com/zinojeng/Whisper.git
cd Whisper

2. 安裝相依套件

pip install -r requirements.txt

3. 安裝 FFmpeg
- macOS: `brew install ffmpeg`
- Windows: `choco install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`

## 使用方式
1. 啟動應用程式

streamlit run main.py

2. 在側邊欄：
   - 輸入您的 OpenAI API 金鑰
   - 選擇 GPT 模型
   - 設定系統提示詞（選擇性）

3. 上傳音訊檔案
4. 等待處理完成
5. 下載生成的檔案：
   - 完整摘要（TXT）
   - 雙語字幕（SRT）
   - 原始轉錄文字

## 支援的音訊格式
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)

## 檔案大小限制
- 最大檔案大小：25MB
- 較大檔案請考慮分割或壓縮

## 使用建議
1. 使用清晰的音訊錄音
2. 避免背景噪音
3. 選擇適當的系統提示詞
4. 複雜內容建議使用 GPT-4

## 常見問題解決
- 確保網路連線穩定
- 驗證 API 金鑰有效性
- 檢查音訊檔案格式和大小
- 監控系統資源使用

## 作者
Doctor Tseng Yao Hsien
Tungs Taichung Metroharbor Hospital

## 版本資訊
- 目前版本：1.0.0 (2024/11)
- 最後更新：2024/11/23

## 授權條款
本專案採用 MIT 授權條款 - 詳見 LICENSE 檔案。

## 致謝
- OpenAI 提供 Whisper 和 GPT-4
- Streamlit 提供網頁框架
- FFmpeg 提供音訊處理

## 聯絡方式
如有問題或建議，請在 GitHub 專案中建立 Issue。

---
© 2024 曾醫師。保留所有權利。
