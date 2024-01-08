import requests
import folium
import json

def obter_dados_api():
    url_api = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    parametros = {}
    
    try:
        # Solicitação GET para a URL da API
        response = requests.get(url_api, params=parametros)
        
        # Verifica se a solicitação foi bem-sucedida (código 200)
        response.raise_for_status()

        # Tenta converter para JSON
        dados_json = response.json()

        return dados_json

    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação: {e}")
        return None
    except ValueError as ve:
        print(f"Erro ao converter para JSON: {ve}")
        return None

# Chama a função para obter dados da API
dados_da_api = obter_dados_api()

# Exibe os dados obtidos
if dados_da_api:

    def processar_dados(dados_da_api):
        incidentes = dados_da_api.get('CVE_Items', [])
        dados_processados = []

        for incidente in incidentes:
            cve = incidente.get('cve', {})
            descricao_data = cve.get('description', {}).get('description_data', [{}])[0]
            tipo = descricao_data.get('value', 'Desconhecido')

            # valores fictícios
            latitude = 0
            longitude = 0

            dados_processados.append({"tipo": tipo, "latitude": latitude, "longitude": longitude})

        return dados_processados

    # Chama a função para processar os dados apenas se houver dados válidos
    dados_processados = processar_dados(dados_da_api)

    if dados_processados:
        # Cria um mapa com base nos dados processados
        def criar_mapa(incidentes):
            mapa = folium.Map(location=[0, 0], zoom_start=2)

            for incidente in incidentes:
                folium.Marker([incidente['latitude'], incidente['longitude']], popup=f'Tipo: {incidente["tipo"]}').add_to(mapa)

            mapa.save('mapa_de_incidentes.html')

        criar_mapa(dados_processados)

        # Salva dados processados em um arquivo JSON
        with open('dados_processados.json', 'w') as json_file:
            json.dump(dados_processados, json_file)

    

