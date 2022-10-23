import requests, json, os
from datetime import datetime as da
from time import localtime, strftime
from itertools import product
from PIL import Image
import win32api, win32con, win32gui

BING_URL_BASE = "http://www.bing.com"
BING_WALLPAPER_PATH = "/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-KO"
resp = requests.get(BING_URL_BASE + BING_WALLPAPER_PATH)
if resp.status_code == 200:
    json_response = json.loads(resp.content)
    wallpaper_path = json_response['images'][0]['url']
    filename = json_response['images'][0]['urlbase'].split('.')[-1].split('_')[0]
    wallpaper_uri = BING_URL_BASE + wallpaper_path
    response = requests.get(wallpaper_uri)
    if resp.status_code == 200:
        with open(f'{os.getcwd()}\\assat\\{filename}_1920x1080.jpg', 'wb') as f:
            f.write(response.content)
    else:
        raise ValueError("[ERROR] non-200 response from Bing server for '{}'".format(wallpaper_uri))
else:
    raise ValueError("[ERROR] non-200 response from Bing server for '{}'".format(BING_URL_BASE + BING_WALLPAPER_PATH))

t_date= strftime("%y%m%d", localtime())
file_dir=os.getcwd()+"\\assat\\"
ext=r'.jpg'
files=[_ for _ in os.listdir(file_dir) if _.endswith(ext)]
for i, j in product(range(len(files)), repeat=2):
    if da.fromtimestamp(os.path.getmtime(file_dir+files[i])) > da.fromtimestamp(os.path.getmtime(file_dir+files[j])):
        (files[i], files[j]) = (files[j], files[i])
print(files)
img1, img2 = file_dir+files[0] ,file_dir+files[1]
images = [Image.open(x) for x in [img1, img2]]
widths, heights = zip(*(i.size for i in images))
total_width = sum(widths)
max_height = max(heights)
new_im = Image.new('RGB', (total_width, max_height))
x_offset = 0
for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]
new_im.save('final.jpg', quality=100, subsampling=0)
key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "1")
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, f'{os.getcwd()}\\final.jpg', 1 + 2)