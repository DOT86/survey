
    let currentQuestion = null;
    let quizId = {{ quiz_id }};
    let currentQuestionIndex = 0;
    let selectedAnswerId = null;
    let totalQuestions = 0;

    async function loadCurrentQuestion() {
        showLoading();

        try {
            const url = `/quiz/api/current-question/?quiz_id=${quizId}`;
            console.log('Fetching question from:', url);

            const response = await fetch(url, {
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
                    window.location.href = `/quiz/result/${quizId}/`;
                    return;
                } else if (errorData.error?.includes('Session not found')) {
                    const created = await createSession();
                    if (created) {
                        return loadCurrentQuestion();
                    }
                } else {
                    alert('Опрос не найден или недоступен');
                    window.location.href = '/quiz/';
                    return;
                }
            }

            if (!response.ok && response.status !== 404) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            console.log('Question data:', data);

            currentQuestion = data;
            displayQuestion(currentQuestion);
            await loadTotalQuestions();

        } catch (error) {
            console.error('Error loading question:', error);
            document.getElementById('question-container').innerHTML = `
                <div class="text-center py-8">
                    <p class="text-red-600 mb-4">Ошибка загрузки вопроса</p>
                    <p class="text-gray-500 mb-4">${error.message}</p>
                    <button onclick="location.reload()" class="bg-blue-600 text-white px-4 py-2 rounded">
                        Попробовать снова
                    </button>
                </div>
            `;
        } finally {
            hideLoading();
        }
    }

    async function createSession() {
        try {
            const response = await fetch(`/quiz/api/start-session/?quiz_id=${quizId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                console.log('Session created');
                return true;
            } else {
                const error = await response.json();
                console.error('Session creation error:', error);
                return false;
            }
        } catch (error) {
            console.error('Error creating session:', error);
            return false;
        }
    }

    async function loadTotalQuestions() {
        try {
            const response = await fetch(`/quiz/api/quizzes/${quizId}/`);

            if (response.ok) {
                const quiz = await response.json();
                totalQuestions = quiz.questions_count || quiz.questions?.length || 0;
                updateProgress();
            }
        } catch (error) {
            console.error('Error loading total questions:', error);
        }
    }

    function displayQuestion(question) {
        if (!question) {
            console.error('No question to display');
            return;
        }

        document.getElementById('question-text').textContent = question.question || 'Вопрос не загружен';
        document.getElementById('question-number').textContent =
            `Вопрос ${currentQuestionIndex + 1}${totalQuestions ? ` из ${totalQuestions}` : ''}`;

        const answersContainer = document.getElementById('answers-container');
        answersContainer.innerHTML = '';

        if (question.answers && question.answers.length > 0) {
            question.answers.forEach(answer => {
                const answerDiv = document.createElement('div');
                answerDiv.className = 'border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition';
                answerDiv.onclick = () => {
                    document.querySelectorAll('#answers-container > .border').forEach(div => {
                        div.classList.remove('bg-blue-50', 'border-blue-500');
                    });
                    answerDiv.classList.add('bg-blue-50', 'border-blue-500');
                    selectedAnswerId = answer.id;
                };

                answerDiv.innerHTML = `
                    <div class="flex items-center">
                        <input type="radio" name="answer" value="${answer.id}" id="answer-${answer.id}" class="mr-3">
                        <label for="answer-${answer.id}" class="flex-grow cursor-pointer">${escapeHtml(answer.text)}</label>
                    </div>
                `;
                answersContainer.appendChild(answerDiv);
            });

            // Кнопка для пользовательского ответа
            const customDiv = document.createElement('div');
            customDiv.className = 'border-2 border-dashed rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition text-center';
            customDiv.onclick = () => openCustomModal();
            customDiv.innerHTML = `
                <div class="text-gray-600">
                    <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                    <span>Написать свой ответ</span>
                </div>
            `;
            answersContainer.appendChild(customDiv);
        } else {
            answersContainer.innerHTML = `
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-700">Ваш ответ:</label>
                    <textarea id="text-answer" rows="4" class="w-full border rounded-lg p-3"
                              placeholder="Введите ваш ответ здесь..."></textarea>
                </div>
            `;
        }
    }

    function openCustomModal() {
        document.getElementById('custom-answer-modal').classList.remove('hidden');
        document.getElementById('custom-answer-modal').classList.add('flex');
    }

    function closeCustomModal() {
        document.getElementById('custom-answer-modal').classList.add('hidden');
        document.getElementById('custom-answer-modal').classList.remove('flex');
        document.getElementById('custom-answer-text').value = '';
    }

    async function submitCustomAnswer() {
        const customText = document.getElementById('custom-answer-text').value.trim();
        if (!customText) {
            alert('Пожалуйста, введите ваш ответ');
            return;
        }
        await submitAnswer(null, customText, 'custom');
        closeCustomModal();
    }

    async function submitAnswer(answerId, customText, answerType = 'predefined') {
        showLoading();

        const payload = {
            question_id: currentQuestion.id,
            answer_type: answerType
        };

        if (answerType === 'predefined') {
            payload.selected_answer_id = answerId;
        } else {
            payload.custom_answer_text = customText;
        }

        try {
            const response = await fetch(`/quiz/api/submit-answer/?quiz_id=${quizId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to submit answer');
            }

            const result = await response.json();
            console.log('Submit result:', result);

            if (result.is_completed) {
                window.location.href = `/quiz/result/${quizId}/`;
            } else {
                currentQuestionIndex++;
                selectedAnswerId = null;
                await loadCurrentQuestion();
                updateProgress();
            }

        } catch (error) {
            console.error('Error submitting answer:', error);
            alert(error.message || 'Ошибка при отправке ответа');
        } finally {
            hideLoading();
        }
    }

    async function nextQuestion() {
        const textAnswer = document.getElementById('text-answer');
        if (textAnswer && textAnswer.value.trim()) {
            await submitAnswer(null, textAnswer.value.trim(), 'custom');
            return;
        }

        if (!selectedAnswerId) {
            alert('Пожалуйста, выберите ответ');
            return;
        }

        await submitAnswer(selectedAnswerId, null, 'predefined');
    }

    function previousQuestion() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            loadCurrentQuestion();
        }
    }

    function updateProgress() {
        if (totalQuestions > 0) {
            const percentage = ((currentQuestionIndex) / totalQuestions) * 100;
            document.getElementById('progress-bar').style.width = `${percentage}%`;
            document.getElementById('progress-text').textContent = `${Math.round(percentage)}%`;
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Инициализация
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Page loaded, quiz ID:', quizId);
        loadCurrentQuestion();
    });