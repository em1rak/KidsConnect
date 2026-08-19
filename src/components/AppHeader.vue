<template>
  <header class="header">
    <router-link to="/" class="logo">
      <img :src="getImageUrl('/image/LeavesPlay1.svg')" alt="Logo" class="logo-icon" />
      <span>KidsConnect</span>
    </router-link>

    <div v-if="authStore.isAuthenticated.value" class="user-menu">
      <!-- Иконка колокольчика уведомлений -->
      <div class="notifications-wrapper" ref="notifRef">
        <button 
          class="notif-btn" 
          @click="toggleNotifDropdown" 
          title="Уведомления"
          :aria-expanded="isNotifOpen"
        >
          <img :src="getImageUrl('/image/Уведомление.svg')" alt="Уведомления" class="notif-icon" />
          <span v-if="unreadCount > 0" class="notif-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
        </button>

        <!-- Выпадающее меню уведомлений -->
        <div v-if="isNotifOpen" class="notif-dropdown">
          <div class="notif-header">
            <span class="notif-title">Уведомления</span>
            <button v-if="unreadCount > 0" class="btn-read-all" @click="markAllAsRead">Прочитать все</button>
          </div>

          <div class="notif-list">
            <div v-if="loadingNotifs" class="notif-empty">
              Загрузка...
            </div>
            <div v-else-if="notifications.length === 0" class="notif-empty">
              У вас пока нет уведомлений
            </div>
            <div 
              v-else 
              v-for="notif in notifications" 
              :key="notif.id" 
              class="notif-item" 
              :class="{ unread: !notif.is_read }"
              @click="markOneAsRead(notif)"
            >
              <div class="notif-text">{{ notif.text }}</div>
              <div class="notif-time">{{ notif.created_at || '' }}</div>
            </div>
          </div>
        </div>
      </div>

      <router-link to="/profile" class="user-info" title="Перейти в личный кабинет">
        <img :src="getImageUrl('/image/Логин1.svg')" alt="icon" class="icon" />
        <span class="user-name">{{ authStore.user.value?.name }}</span>
        <span class="role-badge" :class="authStore.user.value?.role">
          {{ authStore.isLeader.value ? 'Руководитель' : 'Родитель' }}
        </span>
      </router-link>
      
      <router-link to="/profile" class="btn-profile">Профиль</router-link>
      <button class="btn-logout" @click="handleLogout">Выйти</button>
    </div>
      
    <router-link v-else to="/auth" class="auth-btn">
      <img :src="getImageUrl('/image/Логин.svg')" alt="icon" class="icon" />
      <span>Войти / Регистрация</span>
    </router-link>
  </header>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { authStore } from '../authStore'
import api from '../api'

const notifRef = ref(null)
const isNotifOpen = ref(false)
const notifications = ref([])
const loadingNotifs = ref(false)

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

// Загрузка списка уведомлений
async function fetchNotifications() {
  if (!authStore.isAuthenticated.value) return
  loadingNotifs.value = true
  try {
    const list = await api.getNotifications()
    notifications.value = list || []
  } catch (err) {
    console.warn('Не удалось загрузить уведомления:', err)
  } finally {
    loadingNotifs.value = false
  }
}

function toggleNotifDropdown() {
  isNotifOpen.value = !isNotifOpen.value
  if (isNotifOpen.value) {
    fetchNotifications()
  }
}

// Отметка одного уведомления как прочитанного
async function markOneAsRead(notif) {
  if (notif.is_read) return
  try {
    await api.markNotificationRead(notif.id)
    notif.is_read = true
  } catch (err) {
    console.warn('Не удалось обновить статус уведомления:', err)
  }
}

// Отметка всех уведомлений прочитанными
async function markAllAsRead() {
  const unreadItems = notifications.value.filter(n => !n.is_read)
  for (const item of unreadItems) {
    await markOneAsRead(item)
  }
}

// Закрытие при клике снаружи
function handleClickOutside(event) {
  if (notifRef.value && !notifRef.value.contains(event.target)) {
    isNotifOpen.value = false
  }
}

watch(() => authStore.isAuthenticated.value, (isAuth) => {
  if (isAuth) {
    fetchNotifications()
  } else {
    notifications.value = []
  }
}, { immediate: true })

onMounted(() => {
  authStore.checkAuth()
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})

function handleLogout() {
  authStore.logout()
}
</script>


<style scoped>
.logo {
  text-decoration: none;
  color: #ffffff !important;
}

.logo span {
  color: #ffffff !important;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.user-info {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.25);
}

.user-name {
  color: #ffffff;
  font-weight: 600;
}

.role-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  margin-left: 4px;
}

.role-badge.leader {
  background-color: #ffd54f;
  color: #3e2723;
}

.btn-profile {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-profile:hover {
  background: rgba(255, 255, 255, 0.35);
  border-color: #ffffff;
}

.btn-logout {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ffffff;
}

.auth-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: var(--bg-color, #ffffff);
  color: var(--primary-dark, #70232f);
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-left: auto;
}

.auth-btn:hover {
  background-color: #f8f8f8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.auth-icon {
  flex-shrink: 0;
}

/* Стили компонента уведомлений */
.notifications-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.notif-btn {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s ease;
}

.notif-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.notif-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.notif-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background-color: #ef4444;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  box-sizing: border-box;
  border: 2px solid var(--primary-dark, #70232f);
}

.notif-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 320px;
  max-height: 400px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border: 1px solid #e5e7eb;
  z-index: 1000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.notif-header {
  padding: 14px 16px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notif-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-main, #333333);
}

.btn-read-all {
  background: none;
  border: none;
  color: var(--primary-dark, #70232f);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}

.btn-read-all:hover {
  text-decoration: underline;
}

.notif-list {
  overflow-y: auto;
  max-height: 330px;
}

.notif-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: background-color 0.15s ease;
  text-align: left;
}

.notif-item:hover {
  background-color: #f9fafb;
}

.notif-item.unread {
  background-color: #fff8f8;
  border-left: 3px solid var(--primary-dark, #70232f);
}

.notif-text {
  font-size: 13px;
  color: #374151;
  line-height: 1.4;
  word-break: break-word;
}

.notif-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
}

.notif-empty {
  padding: 24px 16px;
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
}
</style>


