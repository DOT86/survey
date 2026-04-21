
    let quizId = {{ quiz.id }};

    async function startQuiz() {
        const btn = document.getElementById('start-btn');
        btn.disabled = true;
        btn.textContent = 'Загрузка...';
        showLoading();

        try {
            // Пытаемся получить первый вопрос
            const response = await fetch(`/quiz/api/current-question/?quiz_id=${quizId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 404) {
                const errorData = await response.json();

                if (errorData.error && errorData.error.includes('Session not found')) {
                    // Создаем новую сессию
                    const sessionResponse = await fetch(`/quiz/api/start-session/?quiz_id=${quizId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (sessionResponse.ok) {
                        // Переходим к прохождению опроса
                        window.location.href = `/quiz/take/${quizId}/`;
                        return;
                    } else {
                        throw new Error('Не удалось создать сессию');
                    }
                } else if (errorData.error && errorData.error.includes('No more questions')) {
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

            // Если всё успешно, переходим к прохождению
            window.location.href = `/quiz/take/${quizId}/`;

        } catch (error) {
            console.error('Error starting quiz:', error);
            alert('Ошибка при начале опроса: ' + error.message);
            btn.disabled = false;
            btn.textContent = 'Начать опрос →';
        } finally {
            hideLoading();
        }
    }