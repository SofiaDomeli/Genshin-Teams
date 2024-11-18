# Importações
## pandas para leitura do DataFrame
import pandas as pd
## Outras classes criadas por nós
### Classe de personagem
from model.characters import Character
### Métodos de reação elemental e ressonância elemental
from model.df_creation import elemental_reaction, elemental_ressonance
## Counter
from collections import Counter
## Bibliotecas do algoritmo de genética
from deap import base, creator, tools, algorithms
## Random, utilizado para a entropia do modelo
import random

# Classe do modelo
class TeamFinder:
    # Método construtoe, recebe a lista de nomes dos personagens escolhidos para o time
    def __init__(self, input_characters:iter = []) -> None:
        # Leitura dos DataFrames de personagens e times
        self.df_characters = pd.read_excel('C:\\Users\\guilhermelanzoni-ieg\\OneDrive - Instituto J&F\\Documents\\Tech Dados 2° ano\\Estatística\\genshin\\Genshin-Teams\\model\\characters.xlsx')
        self.df_teams = pd.read_excel('C:\\Users\\guilhermelanzoni-ieg\\OneDrive - Instituto J&F\\Documents\\Tech Dados 2° ano\\Estatística\\genshin\\Genshin-Teams\\model\\teams.xlsx')
        
        # Definindo os personagens que o algoritmo pode adicionar ao time (os que não foram escolhidos pelo usuário)
        self.available_characters = list(set(self.df_characters['Name']) - set(input_characters))
        # Transformando os times existentes em sets
        self.existing_teams = pd.DataFrame({'team': self.df_teams[['character_1', 'character_2', 'character_3', 'character_4']].apply(lambda x: set(x), axis=1).tolist(), 'rate': self.df_teams['use_rate'].tolist()})
        
        # Parâmetros do algoritmo de genética
        ## Número de gerações (quantas vezes será evoluído)
        self.NUM_GENERATIONS = 100
        ## Tamanho da população
        self.POPULATION_SIZE = 200
        ## Número de indivíduos que competem no torneio de seleção
        self.TOURNAMENT_SIZE = 5
        ## Probabilidade de mutação
        self.MUTATION_PROB = 0.2
        ## Probabilidade de recombinação
        self.CROSSOVER_PROB = 0.8
        
        # Define o objetivo (maximizar o retorno da função de fitness)
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # Salvando os personagens selecionados em um atributo
        self.input_characters = input_characters
        
        # Iniciação do gerenciador do algoritmo (toolbox)
        self.toolbox = base.Toolbox()
        
        # Atributos dos indivíduos (personagem aleatório dos possíveis)
        self.toolbox.register("attr_character", random.choice, self.available_characters)
        # Indivíduos (4 atributos diferentes)
        self.toolbox.register("individual", tools.initIterate, creator.Individual,
                        lambda: input_characters + random.sample(self.available_characters, 4 - len(input_characters)))
        # A população é composta por indivíduos (times)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        
        self.toolbox.register("evaluate", self.fitness)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
        self.toolbox.register("select", tools.selTournament, tournsize=self.TOURNAMENT_SIZE)
        
    # Função de transformação de personagens em
    def to_character(self, name: str):
        df_line = self.df_characters.loc[self.df_characters['Name'] == name].iloc[0].tolist()
        print(df_line)
        return Character(*df_line)
    
    # Função principal de recompensa
    def calculate_compatibility(self, input_characters, complement_characters):
        # Juntando os personagens escolhidos com os gerados pelo modelo (caso já não estejam)
        team_characters = set(input_characters + complement_characters)
        
        # Transformando os personagens em objetos da classe Character
        team_objects = [self.to_character(name) for name in team_characters]
        
        # Encontrando a reação elemental principal do time
        reaction = elemental_reaction(*team_objects)
        
        # Encontrando a principal ressonância elemental do time
        resonance = elemental_ressonance(*team_objects)
        
        # Compatibility Score será a variável de recompensa
        compatibility_score = 0
        
        # Aqui, são adicionados pesos para cada possível ressonância, já que, algumas agregam mais ao time do que outras, além disso, também tem uma tentativa de melhorar o double geo (general damage), já que isso não pode aparecer nos scales dos persoangens
        resonance_weights = {
            'HP': 1.5, 'ATK': 1.5, 'Elemental Mastery': 1.8, 
            'General Damage': 2.0, 'Energy Recharge': 1.0, 
            'CRIT Rate': 1.0, 'Speed': 0.5, 'Resistance': 0.3
        }
        
        compatibility_score += resonance_weights[resonance]

        # Aqui, também são adicionados pesos para as reações elementais, já que algumas delas são melhores que outras (em relção ao DPS [Dano por segundo] do time)
        reaction_weights = {
            'Crystal': 1.0, 'HyperBloom': 3.0, 'AggraSpread': 1.0,
            'Bloom': 1.0, 'Burn': 1.0, 'Fruit Salad': 0.8,
            'National': 1.2, 'Taser': 1.0, 'Vape': 1.2, 
            'Freeze': 1.0, 'Melt': 1.2, 'Burgeon': 1.0, None: 1.0, 'Superconduct': 0.7
        }
        reaction_score = reaction_weights[reaction]

        # Verificação se a reação elemental do time é a mesma dos personagens escolhidos
        if len(set(input_characters)) > 1:
            input_characters = [self.to_character(name) for name in input_characters]
            actual_reaction = elemental_reaction(*list(input_characters+input_characters)[0:4])
            if actual_reaction != None:
                if actual_reaction == reaction:
                    reaction_score *= 1.5
                else:
                    reaction_score /= 2 
        
        # Somando o score das reações à recompensa final
        compatibility_score += reaction_score
        
        # Penalizando caso tenha um personagem Cryo (gelo) esteja no time e a reação principal não seja uma relacionada a cryo
        ## Elementos que não fazem muitas reações elementais (Geo, Anemo) tem muitos buffers, então agregam ao time, porém cryo, não tem tantos, o que faz com que geralmente não sejam interessantes no time 
        if 'Cryo' in [char.element for char in team_objects] and reaction not in ['Freeze', 'Melt', 'Superconduct']:
            return -float('inf')
        
        # Penalizando times com uma reação elemental e 3 personagens do mesmo elemento 
        elements = Counter([char.element for char in team_objects])
        if any(elements[element] > 2 for element in elements) and reaction != None and reaction != 'Overload':
            compatibility_score /= 2
        else:
            compatibility_score *= 1.5
        
        # Se o scale dos personagens for o mesmo, a recompensa é maior
        scales = [char.scale for char in team_objects]
        scale_count = Counter(scales)
        compatibility_score += sum(count for count in scale_count.values() if count > 1)  # Bonus for shared scales
        
        # Penalizando caso o time tenha mais de um Main DPS, já que eles não podem bater ao mesmo tempo
        roles = Counter([char.role for char in team_objects])
        if roles['DPS'] > 1:
            compatibility_score /= 2
        
        # Aumentando a recompensa caso a quantidade de elementos do time seja 2
        if len(set([char.element for char in team_objects])) == 2:
            compatibility_score+=10
        
        # Recompensa para personagens específicos (fazendo isso somente para os personagens mais relevantes)
        ## Chevreuse para times de overload
        if 'Chevreuse' in team_characters:
            if reaction == 'Overload':
                compatibility_score *= 10
            else:
                return -float('inf')
        
        ## Bennett para qualquer time que precise de Ataque
        if 'Bennett' in team_characters:
            if Counter([char.scale for char in team_objects])['ATK'] > 1:
                compatibility_score += 10
            else:
                return -float('inf')
        
        ## Sara para os times com personagens Electro
        if 'Sara' in team_characters:
            if Counter([char.element for char in team_objects])['Electro'] > 1:
                compatibility_score += 10
            else:
                return -float('inf')
            
        ## Shenhe para os times com personagens Electro
        if 'Shenhe' in team_characters:
            if Counter([char.element for char in team_objects])['Cryo'] > 1:
                compatibility_score += 10
            else:
                return -float('inf')
            
        return compatibility_score

    # Função de recompensa (chama a anterior)
    def fitness(self, team):
        # Se os personagens escolhidos não estiverem no time, é penalizado
        if not set(self.input_characters).issubset(set(team)):
            return -float('inf'),
        
        # Se o teme não tiver 4 personagens é penalizado
        if len(set(team)) != 4:
            return -float('inf'),
        
        # Em outros casos, a função anterior é chamada
        return self.calculate_compatibility(self.input_characters, team),
    
    # Função do modelo
    def evolve_teams(self):
        # Encontra caso exista algum time no DataFrame de melhores times com os personagens escolhidos
        matching_teams = self.existing_teams[self.existing_teams['team'].apply(lambda team: set(self.input_characters).issubset(team))]
        ## Caso exista, é retornado o time com maior use rate
        if not matching_teams.empty:
            return [list(team) for team in matching_teams.sort_values(by='rate', ascending=False).head(min(len(matching_teams), 3))['team'].tolist()]
        ## Senão, é aí que o modelo aparece
        else:
            # Aqui é criada a população inicial, com base no que foi definido anteriormente (equipes com 4 integrantes)
            population = self.toolbox.population(n=self.POPULATION_SIZE)
            
            # Loop Evolutivo
            ## Executa algus passos para cada geração do algoritmo
            for gen in range(self.NUM_GENERATIONS):
                # Avaliação de aptidão
                ## Aplica a função de recompensa para todos os indivíduos (equipes) da população
                fitnesses = list(map(self.toolbox.evaluate, population))
                for ind, fit in zip(population, fitnesses): # Zip associa o valor ao indivíduo
                    ind.fitness.values = fit
                
                # Seleção (assim como a seleção natural), como definido anteriormente (Torneio)
                offspring = self.toolbox.select(population, len(population))
                offspring = list(map(self.toolbox.clone, offspring))
                
                # Cruzamento (também funciona como animais em um ciclo evolutivo)
                ## Faz o curuzamento entre pares de indivíduos (2 personagens de um time e 2 de outro)
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() < self.CROSSOVER_PROB:
                        self.toolbox.mate(child1, child2)
                        # Remove o valor que foi definido anteriormente
                        del child1.fitness.values
                        del child2.fitness.values
                
                # Mutação
                ## Aplica uma mutação genética aos indivíduos da nova geração com base em uma probabilidade
                for mutant in offspring:
                    if random.random() < self.MUTATION_PROB:
                        self.toolbox.mutate(mutant)
                        del mutant.fitness.values
                
                # Substitui a geração antiga da população pela nova
                population[:] = offspring
            
            # Quando o ciclo evolutivo acabar, ele seleciona o time que se saiu melhor, baseado na função de recompensa
            return list(tools.selBest(population, k=1))
