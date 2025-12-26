"""
أدوات مساعدة
Utility Functions
"""

import discord
from config import MAX_RESULTS


def create_hadith_embed(result: dict) -> discord.Embed:
    """
    إنشاء رسالة منسقة للحديث
    
    Args:
        result: بيانات الحديث المنسقة
        
    Returns:
        discord.Embed: رسالة منسقة
    """
    embed = discord.Embed(
        title=f"نتيجة {result['index']} - البحث عن: {result['topic']}",
        color=discord.Color.green()
    )
    
    # إضافة نص الحديث
    if result['text']:
        text_content = result['text']
        # تقليل النص إذا كان طويلاً جداً (حد Discord: 2000 حرف)
        if len(text_content) > 2000:
            text_content = text_content[:1997] + "..."
        embed.add_field(name="الحديث", value=text_content, inline=False)
    
    # إضافة المصدر
    if result['source']:
        embed.add_field(name="المصدر", value=result['source'], inline=True)
    
    # إضافة الدرجة
    if result['grade']:
        embed.add_field(name="الدرجة", value=result['grade'], inline=True)
    
    # إضافة الرابط
    if result['link']:
        embed.add_field(name="الرابط", value=result['link'], inline=False)
    
    # إضافة عدد النتائج في آخر رسالة
    if result['is_last']:
        embed.set_footer(
            text=f"تم العثور على {result['total_results']} نتيجة. عرض {result['shown_results']} نتيجة."
        )
    
    return embed


def create_error_embed(error_message: str) -> discord.Embed:
    """
    إنشاء رسالة خطأ منسقة
    
    Args:
        error_message: رسالة الخطأ
        
    Returns:
        discord.Embed: رسالة خطأ منسقة
    """
    embed = discord.Embed(
        title="❌ خطأ",
        description=error_message,
        color=discord.Color.red()
    )
    return embed


def create_help_embed() -> discord.Embed:
    """
    إنشاء رسالة المساعدة
    
    Returns:
        discord.Embed: رسالة المساعدة
    """
    embed = discord.Embed(
        title="مساعدة البوت",
        description="هذا البوت يبحث في الموسوعة الحديثية من موقع الدرر السنية",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="طريقة الاستخدام",
        value="اكتب الموضوع الذي تريد البحث عنه مباشرة في الرسالة، أو استخدم الأمر:\n`!بحث [الموضوع]`",
        inline=False
    )
    embed.add_field(
        name="مثال",
        value="`!بحث الصلاة`\nأو ببساطة اكتب: `الصلاة`",
        inline=False
    )
    embed.add_field(
        name="الأوامر المتاحة",
        value="`!بحث [الموضوع]` - البحث عن موضوع\n`!مساعدة` - عرض هذه الرسالة",
        inline=False
    )
    return embed

