# This cleans the data and creates a new dataframe with the data from 2016, 2018 and 2020.
# Author: Eduardo Adame

import pandas as pd
import numpy as np
import unidecode

translation_dict = {
    'Região \nAdministrativa': 'administrativeRegion',
    'Mortalidade na infância': 'infantMortality',
    'Baixo peso ao nascer': 'lowBirthWeight',
    'Mortalidade materna': 'maternalMortality',
    'Internações infantis por crise respiratória aguda': 'infantHospitalizationsRespiratoryCrisis',
    'Acesso à água canalizada': 'pipedWaterAccess',
    'Acesso a esgotamento sanitário': 'sanitationAccess',
    'Acesso a banheiro': 'toiletAccess',
    'População vivendo em\nFavelas não-urbanizadas': 'populationLivingInNonUrbanizedSlums',
    'Acesso à energia elétrica': 'electricityAccess',
    'Adensamento habitacional\nexcessivo': 'excessiveHousingDensity',
    'Taxa de homicídios': 'homicideRate',
    'Roubos de rua': 'streetRobberies',
    'Alfabetização': 'literacyRate',
    'Qualidade do Ensino Fundamental, anos iniciais': 'qualityOfElementaryEducationEarlyYears',
    'Qualidade do Ensino Fundamental, anos finais': 'qualityOfElementaryEducationLateYears',
    'Abandono escolar no Ensino Médio': 'highSchoolDropoutRate',
    'Acesso à telefone celular ou fixo': 'mobileOrFixedTelephoneAccess',
    'Acesso a internet': 'internetAccess',
    'Mortalidade por doenças crônicas\n': 'chronicDiseaseMortality',
    'Incidência de dengue': 'dengueIncidence',
    'Mortalidade por tuberculose e HIV': 'tuberculosisAndHIVMortality',
    'Coleta seletiva de lixo': 'wasteSelectiveCollection',
    'Degradação de áreas verdes': 'degradationOfGreenAreas',
    'Mobilidade urbana': 'urbanMobility',
    'Homicídios por ação policial': 'policeActionHomicides',
    'Tempo médio de deslocamento': 'averageTravelTime',
    'Participação política': 'politicalParticipation',
    'Gravidez na adolescência': 'teenagePregnancy',
    'Trabalho infantil': 'childLabor',
    'Índice de acesso à cultura': 'culturalAccessIndex',
    'Violência contra a mulher': 'violenceAgainstWomen',
    'Homicídios de jovens negros': 'homicidesOfBlackYouth',
    'Vulnerabilidade familiar': 'familyVulnerability',
    'Pessoas com Ensino Superior': 'populationWithHigherEducation',
    'Negros e indígenas com Ensino Superior': 'blacksAndIndigenousWithHigherEducation',
    'Frequência ao Ensino Superior': 'attendanceToHigherEducation'
}

df = pd.DataFrame()

for year in ['2016', '2018', '2020']:
    year_data = pd.read_excel('data/raw.xlsx', sheet_name=f'Indicadores - {year}')
    year_data = year_data.dropna()
    year_data = year_data.rename(columns = year_data.iloc[0])
    year_data = year_data.drop(year_data.index[[0, 1]])

    year_data = year_data.reset_index(drop=True)
    
    year_data = year_data.rename(columns=translation_dict)
    
    year_data['year'] = int(year)

    df = pd.concat([df, year_data])

normalized = df.iloc[:, 1:-1]  / df.iloc[:, 1:-1].max()
variance = np.std(normalized, axis=0)

selected = df[variance.nlargest(22).index[1:]]

padronized = (selected - selected.mean())/ selected.std()

padronized = padronized.drop(columns=['homicideRate'])
dataset = pd.concat([df[['homicideRate', 'administrativeRegion', 'year']], padronized], axis=1)
dataset['administrativeRegion'] = dataset['administrativeRegion'].apply(lambda x: unidecode.unidecode(x.partition(' ')[2].upper()))

dataset = dataset.reset_index(drop=True)
dataset.to_csv('data/dataset.csv', index=False)
