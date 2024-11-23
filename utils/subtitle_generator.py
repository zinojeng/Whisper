from typing import List, Tuple
import datetime

def create_subtitle_timestamps(text: str, words_per_line: int = 10) -> List[Tuple[float, float, str]]:
    """
    創建字幕時間戳
    每個字幕顯示預計3秒
    """
    words = text.split()
    lines = []
    for i in range(0, len(words), words_per_line):
        line = ' '.join(words[i:i + words_per_line])
        start_time = i / words_per_line * 3
        end_time = start_time + 3
        lines.append((start_time, end_time, line))
    return lines

def format_time(seconds: float) -> str:
    """將秒數轉換為 SRT 時間格式"""
    time = datetime.timedelta(seconds=seconds)
    hours = int(time.total_seconds() // 3600)
    minutes = int((time.total_seconds() % 3600) // 60)
    seconds = int(time.total_seconds() % 60)
    milliseconds = int((time.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def split_sentence(sentence: str, max_length: int = 75) -> List[str]:
    """將長句子分割成較短的片段"""
    if len(sentence) <= max_length:
        return [sentence]
    
    words = sentence.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_bilingual_srt(english_text: str, chinese_text: str, max_length: int = 75) -> str:
    """創建雙語字幕文件，限制每行長度"""
    # 分割文本為句子
    english_sentences = [s.strip() for s in english_text.split('.') if s.strip()]
    chinese_sentences = [s.strip() for s in chinese_text.split('。') if s.strip()]
    
    # 確保兩個列表長度相同
    min_len = min(len(chinese_sentences), len(english_sentences))
    chinese_sentences = chinese_sentences[:min_len]
    english_sentences = english_sentences[:min_len]
    
    srt_content = []
    subtitle_index = 1
    
    for en, ch in zip(english_sentences, chinese_sentences):
        # 分割長句子
        en_parts = split_sentence(en, max_length)
        ch_parts = split_sentence(ch, max_length)
        
        # 確保兩種語言的部分數量相同
        max_parts = max(len(en_parts), len(ch_parts))
        en_parts.extend([''] * (max_parts - len(en_parts)))
        ch_parts.extend([''] * (max_parts - len(ch_parts)))
        
        # 為每個部分創建字幕
        for en_part, ch_part in zip(en_parts, ch_parts):
            if not en_part and not ch_part:
                continue
                
            start_time = (subtitle_index - 1) * 3
            end_time = start_time + 3
            
            start_stamp = f"{int(start_time//3600):02d}:{int((start_time%3600)//60):02d}:{int(start_time%60):02d},000"
            end_stamp = f"{int(end_time//3600):02d}:{int((end_time%3600)//60):02d}:{int(end_time%60):02d},000"
            
            # 添加適當的標點
            en_part = en_part.strip()
            ch_part = ch_part.strip()
            
            if en_part and not en_part.endswith(('.', '!', '?')):
                en_part += '.'
            if ch_part and not ch_part.endswith('。'):
                ch_part += '。'
            
            srt_content.append(f"{subtitle_index}\n{start_stamp} --> {end_stamp}\n{en_part}\n{ch_part}\n\n")
            subtitle_index += 1
    
    return ''.join(srt_content) 