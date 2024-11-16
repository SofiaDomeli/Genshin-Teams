from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para exibir mensagens flash

# Lista de personagens de Genshin Impact
personagens = [
    'Aether', 'Lumine', 'Amber', 'Barbara', 'Beidou', 'Bennett', 'Chongyun', 'Diluc',
    'Fischl', 'Ganyu', 'Hu Tao', 'Jean', 'Kazuha', 'Keqing', 'Klee', 'Mona', 'Ningguang',
    'Qiqi', 'Razor', 'Rosaria', 'Sucrose', 'Tartaglia', 'Venti', 'Xiangling', 'Xiao',
    'Xin Yan', 'Yae Miko', 'Zhongli'
]

# Função para gerar a URL da imagem
def gerar_url_imagem(nome_personagem):
    nome_personagem_modificado = nome_personagem.replace(" ", "_").lower()
    return f"https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/{nome_personagem_modificado}/image.png?strip=all&quality=100&w=160"

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_personagens = {}

    if request.method == 'POST':
        # Receber as seleções do formulário
        dps = request.form.get('dps')
        subdps1 = request.form.get('subdps1')
        subdps2 = request.form.get('subdps2')
        support = request.form.get('support')

        # Verificar se todos os campos foram preenchidos
        if not all([dps, subdps1, subdps2, support]):
            flash('Por favor, preencha todos os campos para montar seu time.')
            return redirect(url_for('index'))

        # Garantir que os personagens selecionados sejam únicos
        selected_personagens = {
            'DPS': dps,
            'Sub DPS 1': subdps1,
            'Sub DPS 2': subdps2,
            'Support': support
        }
        if len(set(selected_personagens.values())) < 4:
            flash('Cada personagem no time deve ser único. Escolha diferentes personagens.')
            return redirect(url_for('index'))

    # Gerando as URLs para as imagens dos personagens
    personagens_imagens = {personagem: gerar_url_imagem(personagem) for personagem in personagens}

    return render_template('index.html', personagens=personagens, selected_personagens=selected_personagens, personagens_imagens=personagens_imagens)

if __name__ == '__main__':
    app.run(debug=True)
