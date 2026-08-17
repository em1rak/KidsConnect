<template>
  <div class="content-wrapper">
    <!-- Шапка профиля -->
    <div class="profile-header">
      <div class="profile-avatar">
        <img :src="getImageUrl('/image/Логин1.svg')" alt="icon" class="icon" />
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ authStore.user.value?.name || 'Пользователь' }}</h1>
        <div class="profile-meta">
          <span class="profile-email">{{ authStore.user.value?.email }}</span>
          <span v-if="authStore.user.value?.phone" class="profile-phone">• {{ authStore.user.value?.phone }}</span>
          <span class="role-pill" :class="authStore.user.value?.role">
            {{ authStore.isLeader.value ? 'Руководитель' : 'Родитель' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Уведомление / Тоаст -->
    <transition name="fade">
      <div v-if="toastMessage" class="toast" :class="toastType">
        {{ toastMessage }}
      </div>
    </transition>

    <!-- СЕКЦИЯ РУКОВОДИТЕЛЯ -->
    <section v-if="authStore.isLeader.value" class="dashboard-section">
      <!-- Микро-Navbar руководителя -->
      <div class="leader-navbar">
        <button 
          class="leader-nav-tab" 
          :class="{ active: activeLeaderTab === 'bookings' }"
          @click="activeLeaderTab = 'bookings'"
        >
          Заявки
          <span class="tab-badge" v-if="bookings.length">{{ bookings.length }}</span>
        </button>

        <button 
          class="leader-nav-tab" 
          :class="{ active: activeLeaderTab === 'activities' }"
          @click="activeLeaderTab = 'activities'"
        >
          Кружки
          <span class="tab-badge" v-if="myActivities.length">{{ myActivities.length }}</span>
        </button>
      </div>

      <!-- ВКЛАДКА 1: ЗАЯВКИ -->
      <div v-if="activeLeaderTab === 'bookings'">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">Управление заявками</h2>
            <p class="section-subtitle">Поступившие записи на ваши кружки и секции</p>
          </div>
          <div class="header-actions">
            <button class="btn-refresh" @click="loadData" :disabled="loading">
              <img :src="getImageUrl('/image/Обновить.svg')" alt="icon" class="icon" />
              Обновить
            </button>
          </div>
        </div>

        <!-- Статистика -->
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-label">Всего заявок</span>
            <span class="stat-value">{{ bookings.length }}</span>
          </div>
          <div class="stat-card pending">
            <span class="stat-label">Ожидают решения</span>
            <span class="stat-value">{{ countByStatus('Ожидает') }}</span>
          </div>
          <div class="stat-card accepted">
            <span class="stat-label">Принято</span>
            <span class="stat-value">{{ countByStatus('Принято') }}</span>
          </div>
          <div class="stat-card rejected">
            <span class="stat-label">Отклонено</span>
            <span class="stat-value">{{ countByStatus('Отклонено') }}</span>
          </div>
        </div>

        <!-- Фильтры по статусам -->
        <div class="filter-tabs">
          <button 
            v-for="status in ['Все', 'Ожидает', 'Принято', 'Отклонено']" 
            :key="status"
            class="tab-btn"
            :class="{ active: leaderFilter === status }"
            @click="leaderFilter = status"
          >
            {{ status }}
          </button>
        </div>

        <!-- Список / Таблица заявок -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <span>Загрузка заявок...</span>
        </div>

        <div v-else-if="filteredLeaderBookings.length === 0" class="empty-state">
          <p>Заявок с выбранными параметрами не найдено.</p>
        </div>

        <div v-else class="bookings-list">
          <div 
            v-for="b in filteredLeaderBookings" 
            :key="b.id" 
            class="booking-card"
            :class="`status-border-${getStatusClass(b.status)}`"
          >
            <div class="booking-header">
              <div class="booking-club">
                <span class="club-title">{{ b.activity?.title || `Кружок #${b.activity_id}` }}</span>
                <span class="booking-date" v-if="b.created_at">Подано: {{ b.created_at }}</span>
              </div>
              <span class="status-badge" :class="getStatusClass(b.status)">
                {{ b.status }}
              </span>
            </div>

            <div class="booking-body">
              <div class="info-group">
                <span class="label">Ребёнок:</span>
                <span class="value font-semibold">{{ b.child_name }} ({{ b.child_age }} лет)</span>
              </div>
              <div class="info-group">
                <span class="label">Родитель:</span>
                <span class="value">{{ b.parent_name }}</span>
              </div>
              <div class="info-group">
                <span class="label">Телефон:</span>
                <a :href="`tel:${b.phone}`" class="value phone-link">{{ b.phone }}</a>
              </div>
            </div>

            <div class="booking-actions">
              <span class="action-label">Сменить статус:</span>
              <div class="btn-group">
                <button 
                  class="btn-status accept" 
                  :disabled="b.status === 'Принято' || updatingId === b.id"
                  @click="changeStatus(b.id, 'Принято')"
                >
                  <span>Принять</span>
                </button>
                <button 
                  class="btn-status reject" 
                  :disabled="b.status === 'Отклонено' || updatingId === b.id"
                  @click="changeStatus(b.id, 'Отклонено')"
                >
                  <span>Отклонить</span>
                </button>
                <button 
                  class="btn-status pending" 
                  :disabled="b.status === 'Ожидает' || updatingId === b.id"
                  @click="changeStatus(b.id, 'Ожидает')"
                >
                  <span>В ожидание</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ВКЛАДКА 2: МОИ КРУЖКИ -->
      <div v-else-if="activeLeaderTab === 'activities'">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">Закрепленные кружки</h2>
            <p class="section-subtitle">Кружки и секции, созданные вашим профилем</p>
          </div>
          <div class="header-actions">
            <router-link to="/create-activity" class="btn-primary-sm">
              Создать кружок
            </router-link>
            
            <button class="btn-refresh" @click="loadData" :disabled="loading">
              <img :src="getImageUrl('/image/Обновить.svg')" alt="icon" class="icon" />
              Обновить
            </button>
          </div>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <span>Загрузка ваших кружков...</span>
        </div>

        <div v-else-if="myActivities.length === 0" class="empty-state">
          <h3>У вас пока нет созданных кружков</h3>
          <p>Нажмите кнопку «Создать кружок», чтобы добавить вашу секцию в каталог.</p>
          <router-link to="/create-activity" class="btn-primary-sm mt-3">
            + Создать кружок
          </router-link>
        </div>

        <div v-else class="my-activities-grid">
          <div v-for="act in myActivities" :key="act.id" class="activity-card">
            <div class="activity-card-image" :style="{ backgroundImage: `url(${getImageUrl(act.image_url)})` }">
              <span class="act-badge">{{ act.category }}</span>
            </div>
            <div class="activity-card-body">
              <h3 class="act-title">{{ act.title }}</h3>
              <p class="act-address">{{ act.address }}</p>
              <div class="act-meta">
                <span class="act-meta-item">{{ act.age_group }}</span>
                <span class="act-price-badge">{{ act.is_free ? 'Бесплатно' : act.price }}</span>
              </div>
              <div class="act-footer">
                <div class="act-btn-row">
                  <router-link :to="`/detail?id=${act.id}`" class="btn-act-action view" title="Открыть карточку">
                    Просмотр
                  </router-link>
                  <router-link :to="`/create-activity?id=${act.id}`" class="btn-act-action edit" title="Редактировать">
                    Изменить
                  </router-link>
                  <button class="btn-act-action delete" @click="confirmDelete(act)" title="Удалить">
                    Удалить
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- СЕКЦИЯ РОДИТЕЛЯ: ИСТОРИЯ ЗАПИСЕЙ -->
    <section v-else class="dashboard-section">
      <div class="section-header-row">
        <div>
          <h2 class="section-title">История моих записей</h2>
          <p class="section-subtitle">Отслеживайте статус ваших заявок в кружки и секции</p>
        </div>
        <router-link to="/" class="btn-primary-sm">
          Найти новый кружок
        </router-link>
      </div>

      <!-- Фильтры по статусу -->
      <div class="filter-tabs">
        <button 
          v-for="status in ['Все', 'Ожидает', 'Принято', 'Отклонено']" 
          :key="status"
          class="tab-btn"
          :class="{ active: parentFilter === status }"
          @click="parentFilter = status"
        >
          {{ status }}
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>Загрузка истории записей...</span>
      </div>

      <div v-else-if="filteredParentBookings.length === 0" class="empty-state">
        <h3>Заявок не найдено</h3>
        <p>Вы пока не подавали заявок или нет записей с выбранным статусом.</p>
        <router-link to="/" class="btn-main mt-4">Каталог кружков</router-link>
      </div>

      <div v-else class="bookings-grid">
        <div 
          v-for="b in filteredParentBookings" 
          :key="b.id" 
          class="parent-booking-card"
        >
          <div class="card-top">
            <div class="club-info">
              <h3 class="club-title">{{ b.activity?.title || `Кружок #${b.activity_id}` }}</h3>
              <p class="club-address" v-if="b.activity?.address">{{ b.activity.address }}</p>
            </div>
            <span class="status-badge" :class="getStatusClass(b.status)">
              {{ b.status }}
            </span>
          </div>

          <div class="card-details">
            <div class="detail-item">
              <span class="detail-label">Ребенок</span>
              <span class="detail-val">{{ b.child_name }}, {{ b.child_age }} лет</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Контактный телефон</span>
              <span class="detail-val">{{ b.phone }}</span>
            </div>
            <div class="detail-item" v-if="b.created_at">
              <span class="detail-label">Дата подачи</span>
              <span class="detail-val">{{ b.created_at }}</span>
            </div>
          </div>

          <div class="status-hint" :class="getStatusClass(b.status)">
            <span v-if="b.status === 'Ожидает'">Ваша заявка находится на рассмотрении руководителем.</span>
            <span v-else-if="b.status === 'Принято'">Поздравляем! Заявка одобрена. С вами свяжутся по указанному номеру.</span>
            <span v-else-if="b.status === 'Отклонено'">К сожалению, запись была отклонена. Вы можете выбрать другой кружок.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Модальное окно подтверждения удаления кружка -->
    <transition name="fade">
      <div v-if="deletingAct" class="modal-backdrop" @click.self="deletingAct = null">
        <div class="modal-card modal-card-sm">
          <div class="modal-header">
            <h3 class="modal-title">Удаление кружка</h3>
            <button class="btn-close" @click="deletingAct = null" aria-label="Закрыть">
              ×
            </button>
          </div>
          <div class="modal-body">
            <p>Вы действительно хотите удалить кружок <strong>«{{ deletingAct.title }}»</strong>?</p>
            <p class="warning-text">Это действие также удалит все поступившие на этот кружок заявки. Данное действие нельзя отменить.</p>
          </div>
          <div class="modal-actions mt-4">
            <button type="button" class="btn-cancel" @click="deletingAct = null">Отмена</button>
            <button type="button" class="btn-danger" :disabled="isDeleting" @click="executeDelete">
              {{ isDeleting ? 'Удаление...' : 'Да, удалить' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { authStore } from '../authStore'
import api from '../api'

const bookings = ref([])
const myActivities = ref([])
const loading = ref(true)
const updatingId = ref(null)

const deletingAct = ref(null)
const isDeleting = ref(false)

const activeLeaderTab = ref('bookings') // 'bookings' | 'activities'
const leaderFilter = ref('Все')
const parentFilter = ref('Все')

const toastMessage = ref('')
const toastType = ref('success')

function confirmDelete(act) {
  deletingAct.value = act
}

async function executeDelete() {
  if (!deletingAct.value) return
  isDeleting.value = true
  try {
    await api.deleteActivity(deletingAct.value.id)
    showToast(`Кружок «${deletingAct.value.title}» успешно удален`, 'success')
    deletingAct.value = null
    await loadData()
  } catch (err) {
    showToast(err.message || 'Не удалось удалить кружок', 'error')
  } finally {
    isDeleting.value = false
  }
}

function showToast(msg, type = 'success') {
  toastMessage.value = msg
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 4000)
}

function getImageUrl(path) {
  if (!path) return import.meta.env.BASE_URL + 'image/Group330.svg'
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  if (path.startsWith('/uploads/') || path.startsWith('/media/') || path.startsWith('uploads/')) {
    return 'http://127.0.0.1:8000/' + path.replace(/^\//, '')
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

function getStatusClass(status) {
  switch (status) {
    case 'Принято': return 'accepted'
    case 'Отклонено': return 'rejected'
    case 'Ожидает':
    default: return 'pending'
  }
}

function countByStatus(status) {
  return bookings.value.filter(b => b.status === status).length
}

const filteredLeaderBookings = computed(() => {
  if (leaderFilter.value === 'Все') return bookings.value
  return bookings.value.filter(b => b.status === leaderFilter.value)
})

const filteredParentBookings = computed(() => {
  if (parentFilter.value === 'Все') return bookings.value
  return bookings.value.filter(b => b.status === parentFilter.value)
})

async function loadData() {
  loading.value = true
  try {
    if (authStore.isLeader.value) {
      const [bRes, aRes] = await Promise.all([
        api.getLeaderBookings(),
        api.getLeaderActivities()
      ])
      bookings.value = bRes
      myActivities.value = aRes
    } else {
      bookings.value = await api.getMyBookings()
    }
  } catch (err) {
    showToast(err.message || 'Ошибка загрузки данных', 'error')
  } finally {
    loading.value = false
  }
}

async function changeStatus(bookingId, newStatus) {
  updatingId.value = bookingId
  try {
    const updated = await api.updateBookingStatus(bookingId, newStatus)
    const idx = bookings.value.findIndex(b => b.id === bookingId)
    if (idx !== -1) {
      bookings.value[idx] = updated
    }
    showToast(`Статус заявки #${bookingId} изменен на "${newStatus}"`, 'success')
  } catch (err) {
    showToast(err.message || 'Ошибка смены статуса', 'error')
  } finally {
    updatingId.value = null
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.content-wrapper {
  width: 100%;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  padding: 20px 25px;
  border-radius: 5px;
  box-shadow: none;
  margin-bottom: 20px;
}

.profile-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
}

.profile-name {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 6px 0;
}

.profile-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 14px;
  opacity: 0.9;
}

.role-pill {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 5px;
  background-color: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.role-pill.leader {
  background-color: #ffd54f;
  color: #3e2723;
}

/* Toast */
.toast {
  padding: 12px 20px;
  border-radius: 5px;
  margin-bottom: 20px;
  font-weight: 600;
  font-size: 14px;
  box-shadow: none;
}

.toast.success {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.toast.error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

/* Leader Sub-Navbar */
.leader-navbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 14px;
}

.leader-nav-tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-main, #333333);
  background: #ffffff;
  border: 1px solid #d1d5db;
  cursor: pointer;
  transition: all 0.2s ease;
}

.leader-nav-tab:hover {
  background: #e0e0e0;
}

.leader-nav-tab.active {
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  border-color: var(--primary-dark, #70232f);
  box-shadow: none;
}

.tab-badge {
  font-size: 12px;
  font-weight: 600;

  padding: 2px 8px;
  border-radius: 5px;
}

.leader-nav-tab.active .tab-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

/* My Activities Grid */
.my-activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.activity-card {
  background: var(--bg-color, #ffffff);
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: none;
  transition: transform 0.2s ease;
}


.activity-card-image {
  height: 150px;
  background-size: cover;
  background-position: center;
  position: relative;
  padding: 12px;
}

.act-badge {
  background: rgba(112, 35, 47, 0.9);
  color: #ffffff;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 5px;
}

.activity-card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: space-between;
  gap: 10px;
}

.act-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-main, #333333);
  margin: 0;
  line-height: 1.3;
}

.act-address {
  font-size: 13px;
  color: var(--text-light, #666666);
  margin: 0;
}

.act-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  margin-top: 4px;
}

.act-meta-item {
  color: #4b5563;
  font-weight: 500;
}

.act-price-badge {
  font-weight: 600;
  color: var(--primary-dark, #70232f);
  background: #fce8eb;
  padding: 3px 8px;
  border-radius: 5px;
}

.act-footer {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #f3f4f6;
}

.act-btn-row {
  display: flex;
  gap: 6px;
}

.btn-act-action {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 6px;
  border-radius: 5px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: var(--text-main, #333333);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-act-action.view:hover {
  background: #f3f4f6;
}

.btn-act-action.edit {
  color: var(--primary-dark, #70232f);
  border-color: #fce8eb;
  background: #fff5f7;
}

.btn-act-action.edit:hover {
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  border-color: var(--primary-dark, #70232f);
}

.btn-act-action.delete {
  color: #dc2626;
  border-color: #fee2e2;
  background: #fef2f2;
}

.btn-act-action.delete:hover {
  background: #dc2626;
  color: #ffffff;
  border-color: #dc2626;
}

.modal-card-sm {
  max-width: 440px;
}

.warning-text {
  font-size: 13px;
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 12px;
  border-radius: 5px;
  margin-top: 12px;
  line-height: 1.4;
}

.btn-danger {
  background: #dc2626;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-danger:hover:not(:disabled) {
  background: #b91c1c;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2F050F;
  margin: 0;
}

.section-subtitle {
  font-size: 14px;
  color: var(--text-light, #666666);
  margin: 4px 0 0 0;
}

.btn-refresh {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #ffffff;
  border: 1px solid #d1d5db;
  padding: 8px 14px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main, #333333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-refresh:hover {
  background: #e0e0e0;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  background: var(--bg-color, #ffffff);
  padding: 16px 20px;
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  display: flex;
  flex-direction: column;
  box-shadow: none;
}

.stat-label {
  font-size: 13px;
  color: var(--text-light, #666666);
  font-weight: 500;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-main, #333333);
  margin-top: 4px;
}

.stat-card.pending .stat-value { color: #d97706; }
.stat-card.accepted .stat-value { color: #059669; }
.stat-card.rejected .stat-value { color: #dc2626; }

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-light, #666666);
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: var(--text-main, #333333);
  background-color: #f3f4f6;
}

.tab-btn.active {
  color: var(--primary-dark, #70232f);
  background-color: #fce8eb;
}

/* Loading & Empty */
.loading-state, .empty-state {
  text-align: center;
  padding: 40px;
  background: #ffffff;
  border-radius: 5px;
  border: 1px dashed #d1d5db;
  color: var(--text-light, #666666);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #f3f4f6;
  border-top-color: var(--primary-dark, #70232f);
  border-radius: 50%;
  animation: spin 1s infinite linear;
  margin: 0 auto 12px auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 8px;
}

/* Booking Card (Leader) */
.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.booking-card {
  background: var(--bg-color, #ffffff);
  border-radius: 5px;
  border: 1px solid #d1d5db;
  padding: 20px;
  box-shadow: none;
  transition: transform 0.2s ease;
}

.booking-card.status-border-pending { border-left: 4px solid #f59e0b; }
.booking-card.status-border-accepted { border-left: 4px solid #10b981; }
.booking-card.status-border-rejected { border-left: 4px solid #ef4444; }

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}

.club-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-main, #333333);
}

.booking-date {
  display: block;
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

.status-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 5px;
}

.status-badge.pending { background: #fef3c7; color: #92400e; }
.status-badge.accepted { background: #d1fae5; color: #065f46; }
.status-badge.rejected { background: #fee2e2; color: #991b1b; }

.booking-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  background: var(--bg-wrapper, #efefef);
  padding: 14px;
  border-radius: 5px;
  margin-bottom: 16px;
}

.info-group {
  display: flex;
  flex-direction: column;
}

.info-group .label {
  font-size: 12px;
  color: var(--text-light, #666666);
}

.info-group .value {
  font-size: 14px;
  color: var(--text-main, #333333);
}

.phone-link {
  color: var(--primary-dark, #70232f);
  text-decoration: none;
  font-weight: 600;
}

.booking-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.action-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main, #333333);
}

.btn-group {
  display: flex;
  gap: 8px;
}

.btn-status {
  padding: 7px 14px;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.btn-status:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-status.accept { background-color: #10b981; color: #ffffff; }
.btn-status.accept:hover:not(:disabled) { background-color: #059669; }

.btn-status.reject { background-color: #ef4444; color: #ffffff; }
.btn-status.reject:hover:not(:disabled) { background-color: #dc2626; }

.btn-status.pending { background-color: #f59e0b; color: #ffffff; }
.btn-status.pending:hover:not(:disabled) { background-color: #d97706; }

/* Parent Grid */
.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.parent-booking-card {
  background: var(--bg-color, #ffffff);
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  padding: 20px;
  box-shadow: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.club-address {
  font-size: 12px;
  color: var(--text-light, #666666);
  margin-top: 2px;
}

.card-details {
  background: var(--bg-wrapper, #efefef);
  padding: 12px 14px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.detail-label { color: var(--text-light, #666666); }
.detail-val { font-weight: 600; color: var(--text-main, #333333); }

.status-hint {
  font-size: 12px;
  padding: 10px 12px;
  border-radius: 5px;
}

.status-hint.pending { background: #fffbe8; color: #78350f; }
.status-hint.accepted { background: #ecfdf5; color: #047857; }
.status-hint.rejected { background: #fef2f2; color: #b91c1c; }

.btn-primary-sm {
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
}

.btn-main {
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  text-decoration: none;
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 5px;
  font-weight: 500;
  display: inline-block;
}

/* Header Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-actions .btn-primary-sm {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  border: none;
}

/* Modal Overlay & Base Styling */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  box-sizing: border-box;
}

.modal-card {
  background: #ffffff;
  width: 100%;
  max-width: 520px;
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  padding: 24px 28px;
  box-shadow: none;
  box-sizing: border-box;
  position: relative;
}

.modal-card-lg {
  max-width: 720px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-dark, #70232f);
  text-transform: uppercase;
  margin: 0;
}

.btn-close {
  background: #f3f4f6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: #fee2e2;
  color: #70232f;
}

.scrollable-form {
  overflow-y: auto;
  padding-right: 8px;
  max-height: calc(90vh - 110px);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main, #333333);
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 14px;
  color: var(--text-main, #333333);
  background-color: #ffffff;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-dark, #70232f);
}

.form-textarea {
  min-height: 90px;
  resize: vertical;
  font-family: inherit;
  line-height: 1.5;
  box-sizing: border-box;
}

.form-section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--primary-dark, #70232f);
  text-transform: uppercase;
  margin-top: 20px;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e5e7eb;
  grid-column: 1 / -1;
}

.checkbox-row {
  display: flex;
  align-items: center;
  margin-top: 6px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  cursor: pointer;
  font-weight: 500;
  color: var(--text-main, #333333);
}

.form-input-file {
  font-size: 13px;
  color: #6b7280;
  padding: 6px 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
  grid-column: 1 / -1;
}

.btn-cancel {
  background: var(--bg-color, #ffffff);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main, #333333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-submit {
  background: var(--primary-dark, #70232f);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: none;
}

.btn-submit:hover:not(:disabled) {
  background: #581b25;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.mt-1 { margin-top: 4px; }
.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
