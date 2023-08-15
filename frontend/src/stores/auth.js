import { defineStore } from 'pinia';
import { LocalStorage } from "quasar";

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    refreshToken: null
  }),

  actions: {
    setToken(accessToken, refreshToken) {
      LocalStorage.set('accessToken', accessToken)
      LocalStorage.set('refreshToken', refreshToken)
      this.accessToken = accessToken
      this.refreshToken = refreshToken
    },
    getAccessToken() {
      return LocalStorage.getItem('accessToken')
    },
    getRefreshToken() {
      return LocalStorage.getItem('refreshToken')
    },
    removeAccessToken() {
      LocalStorage.remove('accessToken')
      this.accessToken = null
    },
    removeRefreshToken() {
      LocalStorage.remove('refreshToken')
      this.refreshToken = null
    },
  }
})
