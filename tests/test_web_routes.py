import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_web_pages(client):
    assert client.get('/').status_code == 200
    assert client.get('/college').status_code == 200
    assert client.get('/ai-lab').status_code == 200
    assert client.get('/dashboard').status_code == 200
    assert client.get('/about').status_code == 200
    
    res_health = client.get('/health')
    assert res_health.status_code == 200
    assert res_health.get_json()['status'] == 'ok'

def test_chat_api(client):
    res = client.post('/api/chat', json={'message': 'What courses are offered?'})
    assert res.status_code == 200
    data = res.get_json()
    assert 'response' in data
    assert 'sources' in data
    assert data['intent'] in ['courses', 'programs']

def test_search_api(client):
    res = client.post('/api/ai-lab/search', json={'algorithm': 'astar', 'start': 'A', 'goal': 'Goal'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['found'] is True
    assert data['path_cost'] == 13

def test_game_api(client):
    board = ['X', '', '', '', 'O', '', '', '', '']
    res = client.post('/api/ai-lab/game', json={'algorithm': 'alphabeta', 'board': board})
    assert res.status_code == 200
    data = res.get_json()
    assert 'best_move' in data

def test_water_jug_api(client):
    res = client.post('/api/ai-lab/water-jug', json={'jug_a': 4, 'jug_b': 3, 'target': 2})
    assert res.status_code == 200
    data = res.get_json()
    assert data['solvable'] is True
    assert data['solution_steps_count'] == 4

def test_missionaries_api(client):
    res = client.post('/api/ai-lab/missionaries-cannibals', json={'missionaries': 3, 'cannibals': 3, 'boat_capacity': 2})
    assert res.status_code == 200
    data = res.get_json()
    assert data['solvable'] is True

def test_dashboard_api(client):
    res = client.get('/api/dashboard/data')
    assert res.status_code == 200
    data = res.get_json()
    assert 'summary' in data
    assert 'chart_base64' in data

def test_voice_chat_elements(client):
    res = client.get('/')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'voiceAutoSpeakBtn' in html
    assert 'micBtn' in html
    assert 'voiceStatusBanner' in html
    assert 'btn-speak' in html
