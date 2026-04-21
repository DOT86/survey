
        function showLoading() {
            document.getElementById('overlay').classList.add('active');
            document.getElementById('loading').classList.add('active');
        }

        function hideLoading() {
            document.getElementById('overlay').classList.remove('active');
            document.getElementById('loading').classList.remove('active');
        }

        function getCSRFToken() {
            return document.querySelector('[name=csrf-token]').content;
        }

        function getAccessToken() {
            return localStorage.getItem('access_token');
        }

        // Проверка авторизации при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            const token = getAccessToken();
            if (!token) {
                // Если нет токена, перенаправляем на страницу входа
                // window.location.href = '/login/';
                console.log('No token found');
            }
        });