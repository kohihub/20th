from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import os
import aiohttp

async def create_profile_image(avatar_url, user_name, user_level, current_xp, xp_to_next_level, user_badges: list):
    avatar_img = None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    avatar_img = Image.open(BytesIO(image_data)).convert("RGBA")
                else:
                    print(f"[❌] Erro ao baixar o avatar: Status {response.status}")
        except Exception as e:
            print(f"[❌] Erro na requisição do avatar: {e}")

    if avatar_img is None:
        avatar_img = Image.new('RGBA', (180, 180), (80, 80, 80))
    assets_folder = os.path.join(os.path.dirname(__file__), "assets")
    
    try:
        background_path = os.path.join(assets_folder, "background.png")
        background = Image.open(background_path).convert("RGBA").resize((700, 250))
    except FileNotFoundError:
        print("[⚠️] Imagem 'background.png' não encontrada. Usando cor sólida como fundo.")
        background = Image.new('RGBA', (700, 250), (40, 42, 54))
    
    script_dir = os.path.dirname(__file__)
    font_path = os.path.join(script_dir, "font.otf")
    
    try:
        font_large = ImageFont.truetype(font_path, 24)
        font_medium = ImageFont.truetype(font_path, 20)
        font_small = ImageFont.truetype(font_path, 18)
    except IOError:
        print("[⚠️] Arquivo de fonte não encontrado! Usando fontes padrão.")
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    avatar_img = avatar_img.resize((180, 180))
    
    background.paste(avatar_img, (35, 35), avatar_img)

    draw = ImageDraw.Draw(background)
    draw.text((250, 50), user_name, fill=(0, 0, 0), font=font_large)
    level_text = f"Level: {user_level}"
    draw.text((250, 130), level_text, fill=(0, 0, 0), font=font_medium)
    
    xp_percentage = current_xp / xp_to_next_level
    progress_width = int(400 * xp_percentage)
    if progress_width > 0:
        draw.rectangle((252, 182, 250 + progress_width, 198), fill=(0, 0, 130))

    xp_text = f"XP: {current_xp} / {xp_to_next_level}"
    text_bbox = draw.textbbox((0, 0), xp_text, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]
    text_pos_x = 250
    draw.text((text_pos_x, 160), xp_text, fill=(0, 0, 0), font=font_small)
    
    badge_size = (32, 32)
    badge_padding = 10
    start_x = 255
    start_y = 80 

    badge_folder = os.path.join(os.path.dirname(__file__), "assets", "badges")

    for badge_id in user_badges:
        try:
            badge_path = os.path.join(badge_folder, f"{badge_id}.png")
            badge_img = Image.open(badge_path).convert("RGBA")
            badge_img = badge_img.resize(badge_size)

            background.paste(badge_img, (start_x, start_y), badge_img)

            start_x += badge_size[0] + badge_padding
        except FileNotFoundError:
            print(f"[⚠️] Imagem da badge '{badge_id}.png' não encontrada.")
            continue 
    

    image_buffer = BytesIO()
    background.save(image_buffer,    format='PNG')
    image_buffer.seek(0)
    
    return image_buffer
