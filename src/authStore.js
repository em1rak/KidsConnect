import { reactive, computed } from 'vue'
import api from './api.js'

const savedUser = JSON.parse(localStorage.getItem('kc_user') || 'null')
const savedToken = localStorage.getItem('kc_token') || null

const state = reactive({
  user: savedUser,
  token: savedToken,
  isLoading: false,
  error: null
})

export const authStore = {
  state,
  user: computed(() => state.user),
  token: computed(() => state.token),
  isAuthenticated: computed(() => !!state.user && !!state.token),
  isLeader: computed(() => state.user?.role === 'leader'),
  isParent: computed(() => state.user?.role === 'parent' || !state.user?.role),
  isLoading: computed(() => state.isLoading),


  async login(loginData) {
    state.isLoading = true
    state.error = null
    try {
      const res = await api.login(loginData)
      this.setAuth(res.user, res.access_token)
      return res
    } catch (err) {
      state.error = err.message
      throw err
    } finally {
      state.isLoading = false
    }
  },

  async register(registerData) {
    state.isLoading = true
    state.error = null
    try {
      const res = await api.register(registerData)
      this.setAuth(res.user, res.access_token)
      return res
    } catch (err) {
      state.error = err.message
      throw err
    } finally {
      state.isLoading = false
    }
  },

  setAuth(user, token) {
    state.user = user
    state.token = token
    if (user) {
      localStorage.setItem('kc_user', JSON.stringify(user))
    } else {
      localStorage.removeItem('kc_user')
    }
    if (token) {
      localStorage.setItem('kc_token', token)
    } else {
      localStorage.removeItem('kc_token')
    }
  },

  async logout() {
    state.isLoading = true
    try {
      await api.logout()
    } catch (e) {
      // Игнорируем ошибки деавторизации на сервере
    } finally {
      this.setAuth(null, null)
      state.isLoading = false
    }
  },

  async checkAuth() {
    if (!state.token) return
    try {
      const user = await api.getMe()
      state.user = user
      localStorage.setItem('kc_user', JSON.stringify(user))
    } catch (e) {
      this.setAuth(null, null)
    }
  }
}
