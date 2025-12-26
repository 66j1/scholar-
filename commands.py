"""
أوامر البوت
Bot Commands
"""

from discord.ext import commands
import discord
from api_handler import search_hadith, format_hadith_results
from utils import create_hadith_embed, create_error_embed, create_help_embed
from config import MAX_RESULTS


class BotCommands(commands.Cog):
    """فئة الأوامر للبوت"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='بحث')
    async def search_command(self, ctx, *, topic):
        """أمر للبحث عن موضوع في الموسوعة الحديثية"""
        await self.handle_search(ctx.message, topic)
    
    @commands.command(name='مساعدة', aliases=['help', 'مساعده'])
    async def help_command(self, ctx):
        """عرض رسالة المساعدة"""
        embed = create_help_embed()
        await ctx.send(embed=embed)
    
    async def handle_search(self, message, topic):
        """معالجة طلب البحث"""
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
            print(f"خطأ في handle_search: {e}")
            error_embed = create_error_embed(f"حدث خطأ أثناء البحث: {str(e)}")
            await message.channel.send(embed=error_embed)


async def setup(bot):
    """إعداد الأوامر"""
    await bot.add_cog(BotCommands(bot))

