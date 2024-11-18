from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from model.model import TeamFinder

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para exibir mensagens flash

characters = {
    'Albedo': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/albedo/image.png?strip=all&quality=100&w=160',
    'Alhaitham': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/alhaitham/image.png?strip=all&quality=100&w=160',
    'Amber': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/amber/image.png?strip=all&quality=100&w=160',
    'Arlecchino': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/arlecchino/image.png?strip=all&quality=100&w=160',
    'Ayaka': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kamisato_ayaka/image.png?strip=all&quality=100&w=160',
    'Ayato': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kamisato_ayato/image.png?strip=all&quality=100&w=160',
    'Baizhu': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/baizhu/image.png?strip=all&quality=100&w=160',
    'Barbara': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/barbara/image.png?strip=all&quality=100&w=160',
    'Beidou': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/beidou/image.png?strip=all&quality=100&w=160',
    'Bennett': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/bennett/image.png?strip=all&quality=100&w=160',
    'Candace': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/candace/image.png?strip=all&quality=100&w=160',
    'Charlotte': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/charlotte/image.png?strip=all&quality=100&w=160',
    'Chevreuse': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/chevreuse/image.png?strip=all&quality=100&w=160',
    'Chiori': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/chiori/image.png?strip=all&quality=100&w=160',
    'Chongyun': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/chongyun/image.png?strip=all&quality=100&w=160',
    'Clorinde': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/clorinde/image.png?strip=all&quality=100&w=160',
    'Collei': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/collei/image.png?strip=all&quality=100&w=160',
    'Cyno': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/cyno/image.png?strip=all&quality=100&w=160',
    'Dehya': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/dehya/image.png?strip=all&quality=100&w=160',
    'Diluc': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/diluc/image.png?strip=all&quality=100&w=160',
    'Diona': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/diona/image.png?strip=all&quality=100&w=160',
    'Dori': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/dori/image.png?strip=all&quality=100&w=160',
    'Emilie': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/emilie/image.png?strip=all&quality=100&w=160',
    'Eula': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/eula/image.png?strip=all&quality=100&w=160',
    'Faruzan': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/faruzan/image.png?strip=all&quality=100&w=160',
    'Fischl': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/fischl/image.png?strip=all&quality=100&w=160',
    'Freminet': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/freminet/image.png?strip=all&quality=100&w=160',
    'Furina': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/furina/image.png?strip=all&quality=100&w=160',
    'Gaming': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/gaming/image.png?strip=all&quality=100&w=160',
    'Ganyu': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/ganyu/image.png?strip=all&quality=100&w=160',
    'Gorou': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/gorou/image.png?strip=all&quality=100&w=160',
    'Heizou': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/heizou/image.png?strip=all&quality=100&w=160',
    'Hu Tao': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/hu_tao/image.png?strip=all&quality=100&w=160',
    'Itto': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/arataki_itto/image.png?strip=all&quality=100&w=160',
    'Jean': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/jean/image.png?strip=all&quality=100&w=160',
    'Kachina': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kachina/image.png?strip=all&quality=100&w=160',
    'Kaeya': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kaeya/image.png?strip=all&quality=100&w=160',
    'Kaveh': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kaveh/image.png?strip=all&quality=100&w=160',
    'Kazuha': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kaedehara_kazuha/image.png?strip=all&quality=100&w=160',
    'Keqing': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/keqing/image.png?strip=all&quality=100&w=160',
    'Kinich': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kinich/image.png?strip=all&quality=100&w=160',
    'Kirara': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kirara/image.png?strip=all&quality=100&w=160',
    'Klee': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/klee/image.png?strip=all&quality=100&w=160',
    'Kokomi': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/sangonomiya_kokomi/image.png?strip=all&quality=100&w=160',
    'Layla': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/layla/image.png?strip=all&quality=100&w=160',
    'Lisa': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/lisa/image.png?strip=all&quality=100&w=160',
    'Lynette': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/lynette/image.png?strip=all&quality=100&w=160',
    'Lyney': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/lyney/image.png?strip=all&quality=100&w=160',
    'Mika': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/mika/image.png?strip=all&quality=100&w=160',
    'Mona': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/mona/image.png?strip=all&quality=100&w=160',
    'Mualani': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/mualani/image.png?strip=all&quality=100&w=160',
    'Nahida': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/nahida/image.png?strip=all&quality=100&w=160',
    'Navia': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/navia/image.png?strip=all&quality=100&w=160',
    'Neuvillette': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/neuvillette/image.png?strip=all&quality=100&w=160',
    'Nilou': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/nilou/image.png?strip=all&quality=100&w=160',
    'Ningguang': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/ningguang/image.png?strip=all&quality=100&w=160',
    'Noelle': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/noelle/image.png?strip=all&quality=100&w=160',
    'Qiqi': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/qiqi/image.png?strip=all&quality=100&w=160',
    'Raiden': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/raiden_shogun/image.png?strip=all&quality=100&w=160',
    'Razor': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/razor/image.png?strip=all&quality=100&w=160',
    'Rosaria': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/rosaria/image.png?strip=all&quality=100&w=160',
    'Sara': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kujou_sara/image.png?strip=all&quality=100&w=160',
    'Sayu': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/sayu/image.png?strip=all&quality=100&w=160',
    'Sethos': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/sethos/image.png?strip=all&quality=100&w=160',
    'Shenhe': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/shenhe/image.png?strip=all&quality=100&w=160',
    'Shinobu': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/kuki_shinobu/image.png?strip=all&quality=100&w=160',
    'Sigewinne': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/sigewinne/image.png?strip=all&quality=100&w=160',
    'Sucrose': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/sucrose/image.png?strip=all&quality=100&w=160',
    'Tartaglia': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/tartaglia/image.png?strip=all&quality=100&w=160',
    'Thoma': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/thoma/image.png?strip=all&quality=100&w=160',
    'Tighnari': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/tighnari/image.png?strip=all&quality=100&w=160',
    'Venti': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/venti/image.png?strip=all&quality=100&w=160',
    'Wanderer': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/wanderer/image.png?strip=all&quality=100&w=160',
    'Wriothesley': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/wriothesley/image.png?strip=all&quality=100&w=160',
    'Xiangling': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/xiangling/image.png?strip=all&quality=100&w=160',
    'Xianyun': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/xianyun/image.png?strip=all&quality=100&w=160',
    'Xiao': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/xiao/image.png?strip=all&quality=100&w=160',
    'Xilonen': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/xilonen/image.png?strip=all&quality=100&w=160',
    'Xingqiu': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/xingqiu/image.png?strip=all&quality=100&w=160',
    'Xinyan': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/xinyan/image.png?strip=all&quality=100&w=160',
    'Yae Miko': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/yae_miko/image.png?strip=all&quality=100&w=160',
    'Yanfei': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/yanfei/image.png?strip=all&quality=100&w=160',
    'Yaoyao': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/yaoyao/image.png?strip=all&quality=100&w=160',
    'Yelan': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/yelan/image.png?strip=all&quality=100&w=160',
    'Yoimiya': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/yoimiya/image.png?strip=all&quality=100&w=160',
    'Yun Jin': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/yun_jin/image.png?strip=all&quality=100&w=160',
    'Zhongli': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/zhongli/image.png?strip=all&quality=100&w=160',
    'Anemo Traveler': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/traveler_anemo/image.png?strip=all&quality=100&w=160',
    'Geo Traveler': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/traveler_geo/image.png?strip=all&quality=100&w=160',
    'Electro Traveler': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/traveler_electro/image.png?strip=all&quality=100&w=160',
    'Dendro Traveler': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/traveler_dendro/image.png?strip=all&quality=100&w=160',
    'Hydro Traveler': 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/traveler_hydro/image.png?strip=all&quality=100&w=160'
}

selected_characters = []
@app.route('/')
def home():
    return render_template('index.html', characters=characters, selected_characters=selected_characters)

@app.route('/submit-form', methods=['POST'])
def index():
    returned_characters = list(request.get_json())
    
    for character in returned_characters:
        if character != '' and character not in selected_characters and character is not None:
            selected_characters.append(character)

@app.route('/get_teams', methods=['GET', 'POST'])
def get_teams():
    teams = TeamFinder(selected_characters).evolve_teams()
    return jsonify(teams)

@app.route('/get_characters', methods=['GET'])
def get_characters():
    return jsonify(characters)

if __name__ == '__main__':
    app.run(debug=True)