import { createApp } from 'vue'

createApp({
    delimiters: ['[[', ']]'],
    data() {
      return {
        count: 0
      }
    }
  }).mount('#profile-photo-wrapper')