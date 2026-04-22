let quizId = {{ quiz.id }};
let isRedirecting = false;

function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function startQuiz() {
    const btn = document.getElementById('start-btn');

    if (btn.disabled || isRedirecting) return;

    btn.disabled = true;
    btn.textContent = 'Загрузка...';
    showLoading();

    await new Promise(resolve => setTimeout(resolve, 50));

    try {
        if (isRedirecting) return;

        const response = await fetch(`/quiz/api/current-question/?quiz_id=${quizId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            credentials: 'include'
        });

        if (response.status === 404) {
            const errorData = await response.json();

            if (errorData.error && errorData.error.includes('Session not found')) {
                const sessionResponse = await fetch(`/quiz/api/start-session/?quiz_id=${quizId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                    credentials: 'include'
                });

                if (sessionResponse.ok) {
                    isRedirecting = true;
                    window.location.href = `/quiz/take/${quizId}/`;
                    return;
                } else {
                    throw new Error('Не удалось создать сессию');
                }
            } else if (errorData.error && errorData.error.includes('No more questions')) {
                isRedirecting = true;
                alert('Вы уже прошли этот опрос!');
                window.location.href = `/quiz/result/${quizId}/`;
                return;
            } else {
                throw new Error(errorData.error || 'Ошибка при начале опроса');
            }
        }

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        isRedirecting = true;
        window.location.href = `/quiz/take/${quizId}/`;

    } catch (error) {
        console.error('Error starting quiz:', error);
        alert('Ошибка при начале опроса: ' + error.message);
        btn.disabled = false;
        btn.textContent = 'Начать опрос →';
        hideLoading();
        isRedirecting = false;
    }
}

function showLoading() {
    const overlay = document.getElementById('overlay');
    const loading = document.getElementById('loading');
    if (overlay) overlay.classList.add('active');
    if (loading) loading.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('overlay');
    const loading = document.getElementById('loading');
    if (overlay) overlay.classList.remove('active');
    if (loading) loading.classList.remove('active');
}