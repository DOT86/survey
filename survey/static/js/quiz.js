
    function showLoading() {
        document.getElementById('loadingOverlay').style.display = 'block';
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) spinner.style.display = 'block';
    }

    function hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) spinner.style.display = 'none';
    }

    async function startQuiz(quizId) {
        showLoading();

        try {
            // Получаем текущий вопрос для проверки существования сессии
            const response = await fetch(`/quiz/api/current-question/?quiz_id=${quizId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            console.log('Response status:', response.status);

            if (response.status === 404) {
                const errorData = await response.json();
                console.log('404 Error:', errorData);

                if (errorData.Error === 'No more questions' || errorData.error?.includes('No more questions')) {
                    alert('Вы уже прошли этот опрос!');
                    window.location.href = `/quiz/result/${quizId}/`;
                    return;
                } else if (errorData.error?.includes('Session not found')) {
                    // Создаем новую сессию
                    const sessionResponse = await fetch(`/quiz/api/start-session/?quiz_id=${quizId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (!sessionResponse.ok) {
                        throw new Error('Не удалось создать сессию');
                    }

                    console.log('Session created successfully');
                } else {
                    alert('Опрос не найден или недоступен');
                    window.location.href = '/quiz/';
                    return;
                }
            }

            if (response.status === 403 || response.status === 401) {
                // Пробуем создать сессию
                const sessionResponse = await fetch(`/quiz/api/start-session/?quiz_id=${quizId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!sessionResponse.ok) {
                    throw new Error('Не удалось создать сессию');
                }
            }

            if (!response.ok && response.status !== 404) {
                throw new Error(`HTTP ${response.status}`);
            }

            // Переходим на страницу опроса
            window.location.href = `/quiz/take/${quizId}/`;

        } catch (error) {
            console.error('Error starting quiz:', error);

            let errorMessage = 'Ошибка при начале опроса. ';
            if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
                errorMessage += 'Проверьте подключение к интернету.';
            } else {
                errorMessage += error.message;
            }

            alert(errorMessage);
        } finally {
            hideLoading();
        }
    }