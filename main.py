"""
الملف الرئيسي للبوت
Main Bot File
"""

import discord
from discord.ext import commands
from config import TOKEN, CLIENT_ID, COMMAND_PREFIX
from api_handler import search_hadith, format_hadith_results
from utils import create_hadith_embed, create_error_embed
from config import MAX_RESULTS


# إنشاء البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    """حدث عند جاهزية البوت"""
    print("=" * 50)
    print(f'✅ البوت {bot.user} جاهز للعمل!')
    print(f'📋 معرف البوت: {bot.user.id}')
    print(f'🆔 Client ID: {CLIENT_ID}')
    print(f'🔗 تم الاتصال بـ {len(bot.guilds)} سيرفر')
    print("=" * 50)


@bot.event
async def on_message(message):
    """حدث عند استلام رسالة"""
    # تجاهل رسائل البوت نفسه
    if message.author == bot.user:
        return
    
    # معالجة الأوامر أولاً
    if message.content.startswith(COMMAND_PREFIX):
        await bot.process_commands(message)
        return
    
    # البحث التلقائي عند كتابة أي موضوع
    if message.content.strip():
        topic = message.content.strip()
        await handle_auto_search(message, topic)


async def handle_auto_search(message, topic):
    """معالجة البحث التلقائي"""
    try:
        # إظهار رسالة "جاري البحث..."
        loading_msg = await message.channel.send("🔍 جاري البحث...")
        
        # البحث في API
        data = await search_hadith(topic)
        
        # حذف رسالة "جاري البحث..."
        try:
            await loading_msg.delete()
        except:
            pass
        
        if data:
            # تنسيق النتائج
            results = format_hadith_results(data, topic, MAX_RESULTS)
            
            if results:
                # إرسال النتائج
                for result in results:
                    embed = create_hadith_embed(result)
                    await message.channel.send(embed=embed)
            else:
                error_embed = create_error_embed(f"لم يتم العثور على نتائج للموضوع: **{topic}**")
                await message.channel.send(embed=error_embed)
        else:
            error_embed = create_error_embed("حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.")
            await message.channel.send(embed=error_embed)
    
    except Exception as e:
        print(f"خطأ في handle_auto_search: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        error_embed = create_error_embed(f"حدث خطأ أثناء البحث: {str(e)}")
        await message.channel.send(embed=error_embed)


@bot.command(name='بحث')
async def search_command(ctx, *, topic):
    """أمر للبحث عن موضوع في الموسوعة الحديثية"""
    await handle_auto_search(ctx.message, topic)


@bot.command(name='مساعدة', aliases=['help', 'مساعده'])
async def help_command(ctx):
    """عرض رسالة المساعدة"""
    from utils import create_help_embed
    embed = create_help_embed()
    await ctx.send(embed=embed)


# تشغيل البوت
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ خطأ: Token غير صحيح!")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

