const BASE_URL = 'http://localhost:8000/api';

/**
 * Базовый метод отправки HTTP-запросов с автоматической подстановкой токена и обработкой ошибок
 */
async function request(endpoint, options = {}) {
  const token = localStorage.getItem('kc_token');
  const headers = { ...options.headers };

  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (options.body && !(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (response.status === 204) {
    return null;
  }

  let data;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const errorMsg = data?.detail || `Ошибка сервера (${response.status})`;
    throw new Error(errorMsg);
  }

  return data;
}

export default {
  // Кружки
  async getActivities() {
    try {
      return await request('/activities/');
    } catch (error) {
      console.error('Ошибка при загрузке кружков:', error);
      return [];
    }
  },

  async getActivityById(id) {
    return await request(`/activities/${id}`);
  },

  async createActivity(activityData) {
    return await request('/activities/', {
      method: 'POST',
      body: JSON.stringify(activityData)
    });
  },

  async updateActivity(id, activityData) {
    return await request(`/activities/${id}`, {
      method: 'PUT',
      body: JSON.stringify(activityData)
    });
  },

  async deleteActivity(id) {
    return await request(`/activities/${id}`, {
      method: 'DELETE'
    });
  },

  // Загрузка медиафайлов
  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    const data = await request('/upload/', {
      method: 'POST',
      body: formData
    });
    return data.image_url;
  },

  // Заявки и бронирования
  async createBooking(bookingData) {
    return await request('/bookings/', {
      method: 'POST',
      body: JSON.stringify(bookingData)
    });
  },

  async getMyBookings() {
    return await request('/bookings/my');
  },

  async getLeaderBookings() {
    return await request('/leader/bookings');
  },

  async getLeaderActivities() {
    return await request('/leader/activities');
  },

  async getActivityBookings(activityId) {
    return await request(`/activities/${activityId}/bookings`);
  },

  async updateBookingStatus(bookingId, status) {
    return await request(`/bookings/${bookingId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    });
  },

  // Авторизация
  async register(userData) {
    return await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  },

  async login(loginData) {
    return await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(loginData)
    });
  },

  async getMe() {
    return await request('/auth/me');
  },

  async logout() {
    try {
      await request('/auth/logout', { method: 'POST' });
    } catch {
      // Игнорируем ошибки при деавторизации на бэкенде
    }
  },

  // Отзывы
  async getReviews(activityId) {
    return await request(`/activities/${activityId}/reviews`);
  },

  async createReview(reviewData) {
    return await request('/reviews/', {
      method: 'POST',
      body: JSON.stringify(reviewData)
    });
  },

  // Рекомендации
  async getRecommendations(age, category) {
    const params = new URLSearchParams();
    if (age !== undefined && age !== null && age !== '') params.append('age', age);
    if (category) params.append('category', category);
    return await request(`/recommendations/?${params.toString()}`);
  },

  // Уведомления
  async getNotifications() {
    return await request('/notifications/');
  },

  async markNotificationRead(notificationId) {
    return await request(`/notifications/${notificationId}/read`, {
      method: 'PATCH'
    });
  }
};