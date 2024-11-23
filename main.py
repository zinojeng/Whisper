import streamlit as st
from pydub import AudioSegment
from utils.text_processor import process_text, translate_text, summarize_text
from utils.openai_client import init_openai, create_transcription
from tempfile import NamedTemporaryFile
import time
from utils.subtitle_generator import create_bilingual_srt

def process_audio_with_progress(client, chunks, system_prompt):
    """處理音頻並顯示進度"""
    progress_bar = st.progress(0)
    transcript = ""
    
    for i, chunk in enumerate(chunks):
        with st.spinner(f'處理音頻片段 {i+1}/{len(chunks)}...'):
            with NamedTemporaryFile(suffix=".wav", delete=True) as f:
                chunk.export(f.name, format="wav")
                with open(f.name, "rb") as audio_file:
                    transcript += create_transcription(client, audio_file)
        progress = (i + 1) / len(chunks)
        progress_bar.progress(progress)
    
    return transcript

def format_transcript(text: str) -> str:
    """將原始文本分段，使其更易閱讀"""
    # 按句號分割，但保留句號
    sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
    # 每4句組成一個段落
    paragraphs = [' '.join(sentences[i:i+4]) for i in range(0, len(sentences), 4)]
    return '\n\n'.join(paragraphs)

def translate_in_chunks(client, text: str, system_prompt: str, chunk_size: int = 1500) -> str:
    """分塊翻譯長文本"""
    # 按句號分割文本
    sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        if current_length + len(sentence) > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = len(sentence)
        else:
            current_chunk.append(sentence)
            current_length += len(sentence)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    # 翻譯每個塊
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        with st.spinner(f'翻譯進度: {i+1}/{len(chunks)}'):
            translated = translate_text(client, chunk, system_prompt)
            translated_chunks.append(translated)
    
    return '\n\n'.join(translated_chunks)

def create_download_link(text: str, filename: str) -> str:
    """創建下載連結"""
    import base64
    b64 = base64.b64encode(text.encode('utf-8')).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">下載 {filename}</a>'

def create_bilingual_srt(english_text: str, chinese_text: str) -> str:
    """創建雙語字幕文件"""
    # 分割文本為句子
    english_sentences = [s.strip() for s in english_text.split('.') if s.strip()]
    chinese_sentences = [s.strip() for s in chinese_text.split('。') if s.strip()]
    
    # 確保兩個列表長度相同
    min_len = min(len(chinese_sentences), len(english_sentences))
    chinese_sentences = chinese_sentences[:min_len]
    english_sentences = english_sentences[:min_len]
    
    srt_content = []
    for i, (en, ch) in enumerate(zip(english_sentences, chinese_sentences), 1):
        # 每個字幕顯示3秒
        start_time = (i - 1) * 3
        end_time = start_time + 3
        
        # 格式化時間戳
        start_stamp = f"{int(start_time//3600):02d}:{int((start_time%3600)//60):02d}:{int(start_time%60):02d},000"
        end_stamp = f"{int(end_time//3600):02d}:{int((end_time%3600)//60):02d}:{int(end_time%60):02d},000"
        
        # 添加句號（如果沒有的話）
        en = en if en.endswith('.') else en + '.'
        ch = ch if ch.endswith('。') else ch + '。'
        
        # 構建字幕塊
        srt_content.append(f"{i}\n{start_stamp} --> {end_stamp}\n{en}\n{ch}\n\n")
    
    return ''.join(srt_content)

def show_instructions():
    st.markdown("""
    ### 使用說明
    1. **設定 API Key**
        - 在側欄輸入您的 OpenAI API Key
        - 選擇要使用的 GPT 模型
    
    2. **上傳音檔**
        - 支援的格式：MP3, WAV, M4A
        - 檔案大小限制：25MB
    
    3. **處理過程**
        - 系統會自動將音檔轉換為文字
        - 產生中英文逐字稿
        - 生成重點摘要
        - 建立雙語字幕檔
    
    4. **下載選項**
        - 完整報告（TXT格式）
        - 雙語字幕（SRT格式）
        
    ### 注意事項
    - 處理時間依音檔長度而定
    - 請確保網路連線穩定
    - API Key 請妥善保管，勿外流
    """)

def main():
    # 設置頁面配置
    st.set_page_config(
        page_title="Audio to Summary",
        page_icon="🎯",
        layout="wide"
    )
    
    # 側欄設置
    with st.sidebar:
        st.markdown("### 設定")
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="在 https://platform.openai.com/account/api-keys 取得"
        )
        
        model = st.selectbox(
            "選擇模型",
            ["gpt-4o", "gpt-4o-mini"],
            help="gpt-4o: 穩定但較慢，token 耗用較多\ngpt-4o-mini: 便宜但速度較快"
        )
        
        st.markdown("---")
        if st.button("顯示使用說明"):
            show_instructions()
            
        st.markdown("---")
        st.markdown("""
        ### 關於
        Created by Doctor Tseng  
        Tungs' Metroharbor Hospital Taichung
        
        版本：1.0.0  
        最後更新：2024/01
        """)

    # 主要內容
    st.markdown("<h1 style='text-align: center; color: blue;'>Audio to Summarization</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Convert audio to text summary with GPT-4</p>", unsafe_allow_html=True)

    if not api_key:
        st.warning("請在側欄輸入您的 OpenAI API Key")
        return

    try:
        client = init_openai(api_key)
        
        # 系統提示輸入
        system_prompt = st.text_input(
            '輸入系統角色設定:',
            help="例如：You specialize in endocrinology and diabetes..."
        )
        
        # 檔案上傳
        audio_file = st.file_uploader("上傳音檔", type=["mp3", "wav", "m4a"])
        
        if audio_file is not None:
            if 'processed_results' not in st.session_state:
                with st.spinner('處理音檔中...'):
                    # 讀取音頻
                    audio_data = AudioSegment.from_file(audio_file)
                    
                    # 分割音頻
                    chunk_length = 100 * 1000  # 100 seconds
                    chunks = [
                        audio_data[i:i + chunk_length]
                        for i in range(0, len(audio_data), chunk_length)
                    ]
                    
                    # 處理音頻並顯示進度
                    transcript = process_audio_with_progress(client, chunks, system_prompt)
                    
                    # 更新模型選擇
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": transcript}
                    ]
                    
                    # 使用選擇的模型
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages
                    )
                    
                    # 處理文本
                    with st.spinner('生成摘要中...'):
                        processed_transcript = process_text(client, transcript, system_prompt)
                        processed_transcript_ch = translate_text(client, transcript, system_prompt)
                        processed_summary = summarize_text(client, processed_transcript, system_prompt)
                        processed_summary_str = "\n".join(processed_summary)
                        
                        # 保存結果
                        st.session_state.processed_results = {
                            'transcript': transcript,
                            'processed_transcript_ch': processed_transcript_ch,
                            'processed_transcript': processed_transcript,
                            'processed_summary_str': processed_summary_str
                        }
                
            # 顯示結果
            if st.session_state.processed_results:
                results = st.session_state.processed_results
                
                # 原始長文（分段）
                with st.expander("原始長文", expanded=False):
                    formatted_transcript = format_transcript(results['transcript'])
                    st.markdown(f"<div style='font-size: 14px;'>{formatted_transcript}</div>", 
                              unsafe_allow_html=True)
                    st.markdown(create_download_link(formatted_transcript, "original_transcript.txt"), 
                              unsafe_allow_html=True)

                # 中文逐字稿（分塊翻譯）
                with st.expander("中文逐字稿", expanded=True):
                    if '分塊翻譯' not in st.session_state:
                        with st.spinner('正在翻譯長文本...'):
                            translated_text = translate_in_chunks(client, results['transcript'], system_prompt)
                            st.session_state.分塊翻譯 = translated_text
                    
                    st.markdown(f"<div style='font-size: 14px;'>{st.session_state.分塊翻譯}</div>", 
                              unsafe_allow_html=True)
                    st.markdown(create_download_link(st.session_state.分塊翻譯, "chinese_translation.txt"), 
                              unsafe_allow_html=True)

                # 英文摘要
                with st.expander("英文摘要", expanded=False):
                    st.markdown(f"<div style='font-size: 14px;'>{results['processed_transcript']}</div>", 
                              unsafe_allow_html=True)
                    st.markdown(create_download_link(results['processed_transcript'], "english_summary.txt"), 
                              unsafe_allow_html=True)

                # 重點整理
                with st.expander("重點整理", expanded=True):
                    st.markdown(f"<div style='font-size: 14px;'>{results['processed_summary_str']}</div>", 
                              unsafe_allow_html=True)
                    st.markdown(create_download_link(results['processed_summary_str'], "key_points.txt"), 
                              unsafe_allow_html=True)
                
                # 下載所有內容
                all_content = f"""原始長文：
{formatted_transcript}

中文逐字稿：
{st.session_state.get('分塊翻譯', '翻譯處理中...')}

英文摘要：
{results['processed_transcript']}

重點整理：
{results['processed_summary_str']}
"""
                st.markdown("---")
                st.markdown("### 下載選項")
                col1, col2, col3 = st.columns(3)
                
                # 生成雙語字幕
                if '分塊翻譯' in st.session_state:
                    try:
                        srt_content = create_bilingual_srt(
                            results['transcript'],
                            st.session_state.分塊翻譯
                        )
                        
                        with col1:
                            st.markdown(create_download_link(all_content, "complete_summary.txt"), 
                                      unsafe_allow_html=True)
                        with col2:
                            st.markdown(create_download_link(srt_content, "bilingual_subtitles.srt"), 
                                      unsafe_allow_html=True)
                            st.caption("雙語字幕檔 (SRT格式)")
                        
                        # 可選：顯示字幕預覽
                        if st.checkbox("預覽字幕"):
                            st.text_area("字幕預覽", srt_content, height=200)
                            
                    except Exception as e:
                        st.error(f"生成字幕時發生錯誤：{str(e)}")
                
                # 添加重置按鈕
                if st.button('處理新的音頻'):
                    st.session_state.processed_results = None
                    if '分塊翻譯' in st.session_state:
                        del st.session_state.分塊翻譯
                    st.experimental_rerun()
                    
    except Exception as e:
        st.error(f"發生錯誤：{str(e)}")

if __name__ == "__main__":
    main() 