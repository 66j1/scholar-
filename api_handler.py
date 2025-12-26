"""
معالج API للموسوعة الحديثية
API Handler for Hadith Encyclopedia
"""

import aiohttp
import json
import urllib.parse
from config import API_BASE_URL


def clean_jsonp_response(text: str) -> str:
    """تنظيف النتيجة من JSONP callback"""
    if text.startswith('?('):
        text = text[2:]
    if text.endswith(');'):
        text = text[:-2]
    if text.startswith('callback('):
        text = text[9:]
    if text.endswith(');'):
        text = text[:-2]
    return text.strip()


async def search_hadith(topic: str) -> dict:
    """
    البحث عن موضوع في الموسوعة الحديثية
    
    Args:
        topic: الموضوع المراد البحث عنه
        
    Returns:
        dict: البيانات المستلمة من API أو None في حالة الخطأ
    """
    try:
        # ترميز الموضوع للبحث
        encoded_topic = urllib.parse.quote(topic)
        
        # بناء رابط API
        api_url = f"{API_BASE_URL}?skey={encoded_topic}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    # قراءة النتيجة
                    text = await response.text()
                    
                    # تنظيف النتيجة من JSONP callback
                    text = clean_jsonp_response(text)
                    
                    # تحويل JSON
                    try:
                        data = json.loads(text)
                        return data
                    except json.JSONDecodeError as e:
                        print(f"خطأ في تحليل JSON: {e}")
                        print(f"النص المستلم: {text[:500]}")
                        return None
                else:
                    print(f"خطأ في الاتصال بالخادم. الرمز: {response.status}")
                    return None
    
    except aiohttp.ClientError as e:
        print(f"خطأ في الاتصال: {e}")
        return None
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        return None


def format_hadith_results(data: dict, topic: str, max_results: int = 5) -> list:
    """
    تنسيق نتائج البحث للعرض
    
    Args:
        data: البيانات المستلمة من API
        topic: الموضوع المبحوث عنه
        max_results: عدد النتائج القصوى
        
    Returns:
        list: قائمة بالنتائج المنسقة
    """
    if not data or 'ahadith' not in data or len(data['ahadith']) == 0:
        return []
    
    results = data['ahadith'][:max_results]
    total_results = len(data['ahadith'])
    
    formatted_results = []
    for idx, hadith in enumerate(results, 1):
        result = {
            'index': idx,
            'topic': topic,
            'text': hadith.get('th', ''),
            'source': hadith.get('m', ''),
            'grade': hadith.get('g', ''),
            'link': hadith.get('l', ''),
            'is_last': idx == len(results),
            'total_results': total_results,
            'shown_results': len(results)
        }
        formatted_results.append(result)
    
    return formatted_results

