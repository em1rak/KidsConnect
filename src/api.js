const BASE_URL = 'http://localhost:8000/api';

function getAuthHeaders() {
  const token = localStorage.getItem('kc_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export default {
  // Получить список всех кружков
  async getActivities() {
    try {
      const response = await fetch(`${BASE_URL}/activities/`);
      if (!response.ok) throw new Error('Ошибка сети');
      return await response.json();
    } catch (error) {
      console.error('Ошибка при загрузке кружков:', error);
      return [];
    }
  },

  // Получить конкретный кружок по ID
  async getActivityById(id) {
    const response = await fetch(`${BASE_URL}/activities/${id}`);
    if (!response.ok) throw new Error('Кружок не найден');
    return await response.json();
  },

  // Создать новый кружок (для руководителей)
  async createActivity(activityData) {
    const response = await fetch(`${BASE_URL}/activities/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(activityData)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка при создании кружка');
    }
    return data;
  },

  // Загрузка обложки кружка на сервер
  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('kc_token');
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`${BASE_URL}/upload/`, {
      method: 'POST',
      headers,
      body: formData
    });
    const data = await response.json();
    if (!response.ok) throw new Error('Ошибка при загрузке изображения');
    return data.image_url;
  },

  // Отправить заявку на запись
  async createBooking(bookingData) {
    try {
      const response = await fetch(`${BASE_URL}/bookings/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(bookingData)
      });
      if (!response.ok) throw new Error('Ошибка при отправке');
      return await response.json();
    } catch (error) {
      console.error('Ошибка записи:', error);
      throw error;
    }
  },

  // Регистрация пользователя
  async register(userData) {
    const response = await fetch(`${BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка регистрации');
    }
    return data;
  },

  // Авторизация (вход)
  async login(loginData) {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loginData)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка авторизации');
    }
    return data;
  },

  // Получить текущего пользователя по токену
  async getMe() {
    const response = await fetch(`${BASE_URL}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) {
      throw new Error('Сессия недействительна');
    }
    return await response.json();
  },

  // Выход из системы
  async logout() {
    try {
      await fetch(`${BASE_URL}/auth/logout`, {
        method: 'POST',
        headers: getAuthHeaders()
      });
    } catch (e) {
      // Игнорируем ошибки при деавторизации на бэкенде
    }
  },

  // Получить заявки текущего родителя (История для родителей)
  async getMyBookings() {
    const response = await fetch(`${BASE_URL}/bookings/my`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Не удалось загрузить историю заявок');
    return await response.json();
  },

  // Получить заявки руководителем (для его кружков)
  async getLeaderBookings() {
    const response = await fetch(`${BASE_URL}/leader/bookings`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Не удалось загрузить заявки руководителя');
    return await response.json();
  },

  // Получить кружки текущего руководителя
  async getLeaderActivities() {
    const response = await fetch(`${BASE_URL}/leader/activities`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Не удалось загрузить кружки руководителя');
    return await response.json();
  },

  // Получить заявки на конкретный кружок
  async getActivityBookings(activityId) {
    const response = await fetch(`${BASE_URL}/activities/${activityId}/bookings`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Не удалось загрузить заявки на кружок');
    return await response.json();
  },

  // Смена статуса заявки («Ожидает», «Принято», «Отклонено»)
  async updateBookingStatus(bookingId, status) {
    const response = await fetch(`${BASE_URL}/bookings/${bookingId}/status`, {
      method: 'PATCH',
      headers: getAuthHeaders(),
      body: JSON.stringify({ status })
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Не удалось обновить статус заявки');
    }
    return data;
  },

  // Обновить кружок
  async updateActivity(id, activityData) {
    const response = await fetch(`${BASE_URL}/activities/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(activityData)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Не удалось обновить кружок');
    }
    return data;
  },

  // Удалить кружок
  async deleteActivity(id) {
    const response = await fetch(`${BASE_URL}/activities/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Не удалось удалить кружок');
    }
    return data;
  },

  // Получить отзывы к конкретному кружку
  async getReviews(activityId) {
    const response = await fetch(`${BASE_URL}/activities/${activityId}/reviews`);
    if (!response.ok) throw new Error('Не удалось загрузить отзывы');
    return await response.json();
  },

  // Оставить отзыв к кружку
  async createReview(reviewData) {
    const response = await fetch(`${BASE_URL}/reviews/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(reviewData)
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Не удалось оставить отзыв');
    }
    return data;
  },

  // Получить рекомендации по возрасту и категории
  async getRecommendations(age, category) {
    const params = new URLSearchParams();
    if (age !== undefined && age !== null && age !== '') params.append('age', age);
    if (category) params.append('category', category);

    const response = await fetch(`${BASE_URL}/recommendations/?${params.toString()}`);
    if (!response.ok) throw new Error('Не удалось загрузить рекомендации');
    return await response.json();
  },

  // Получить уведомления текущего пользователя
  async getNotifications() {
    const response = await fetch(`${BASE_URL}/notifications/`, {
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Не удалось загрузить уведомления');
    return await response.json();
  },

  // Отметить уведомление как прочитанное
  async markNotificationRead(notificationId) {
    const response = await fetch(`${BASE_URL}/notifications/${notificationId}/read`, {
      method: 'PATCH',
      headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Не удалось обновить статус уведомления');
    return await response.json();
  }
};


