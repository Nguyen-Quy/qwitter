<template>
  <q-page class="relative-position">
    <q-scroll-area class="absolute fullscreen">
      <div class="q-py-lg q-px-md row items-end q-col-gutter-md">
        <div class="col">
          <q-input
            v-model="newQweetContent"
            placeholder="What's happening?"
            maxlength="200"
            bottom-slots
            counter
            autogrow
            class="new-qweet">
            <template v-slot:before>
              <q-avatar size="xl">
                <img src="~/src/assets/quy.jpg" style="object-fit:cover;">
              </q-avatar>
            </template>
          </q-input>
        </div>
        <div class="col col-shrink">
          <q-btn
            @click="addNewQweet"
            class="glossy q-mb-lg"
            rounded
            no-caps
            :disable="!newQweetContent"
            color="primary"
            label="Qweet" />
        </div>
      </div>
      <q-separator size="10px" color="grey-2" class="divider" />

      <q-list separator>
        <transition-group
          appear
          enter-active-class="animated fadeIn slow"
          leave-active-class="animated fadeOut slower">

          <q-item v-for="(qweet, index) in this.qweets.slice().reverse()" :key="qweet.created_at" class="qweet q-py-md">

            <q-item-section avatar top>
              <q-avatar size="xl">
                <img src="~/src/assets/quy.jpg" style="object-fit:cover;">
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label class="text-subtitle1">
                <strong>{{ this.username }}</strong> <br class="lt-md">
                <span class="text-grey-7"> {{ this.email }} <br class="lt-md"> &bull; {{ relativeDate(qweet.created_at) }}
                </span>
              </q-item-label>
              <q-item-label class="qweet-content text-body1">
                {{ qweet.content }}
              </q-item-label>
              <div class="row qweet-icons justify-between q-mt-sm">
                <div>
                  <q-btn flat round color="grey" size="sm" icon="far fa-comment" @click="commentQweet(qweet)" />
                  {{ qweet.commentCount || 0 }}
                </div>
                <div>
                  <q-btn flat round color="grey" size="sm" icon="fas fa-retweet" @click="reQweet(qweet)" />
                  {{ qweet.share || 0 }}
                </div>
                <div>
                  <q-btn flat round color="grey" size="sm" icon="far fa-heart" @click="likeQweet(qweet)" />
                  {{ qweet.like || 0 }}
                </div>
                <div>
                  <q-btn flat round color="grey" size="sm" icon="fas fa-trash" @click="deleteQweet(qweet)" />
                </div>
              </div>
              <q-item-label v-for="(cmt, index) in qweet.comments" :key="index" class="text-body2">
                {{ cmt.comment }}
              </q-item-label>
            </q-item-section>

            <q-separator inset="item" />
          </q-item>

        </transition-group>


      </q-list>
    </q-scroll-area>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { api } from 'src/boot/axios'
import { useAuthStore } from "../stores/auth";
import { formatDistance } from 'date-fns'

export default defineComponent({
  name: 'PageHome',
  setup() {
    const store = useAuthStore()
    const token = store.getAccessToken()

    return { store, token }
  },
  data() {
    return {
      newQweetContent: '',
      qweets: [],
      username: '',
      email: '',
      like: 0,
      share: 0, //reQweet
      commentCount: 0,
      comments: []
    }
  },
  mounted() {
    this.getMe()
    this.getAllQweets()
  },
  methods: {
    relativeDate(value) {
      let now = new Date()
      let val = new Date(value)
      return formatDistance(val, now, { includeSeconds: true, addSuffix: true })
    },
    async getMe() {
      const me = await api.get(`/users/me`, {
        headers: { "Authorization": `Bearer ${this.token}` }
      }).then(res => {
        this.username = res.data.fullname || res.data.username
        this.email = res.data.email
      }).catch(err => {
        if (err.response.status == 401) {
          // remove old accessToken
          this.store.removeAccessToken()

          //use refreshToken to get new set of token
          // let refreshToken = this.store.getRefreshToken()
          // const refresh = api.post(`/users/refresh`, {}, {
          //   headers: { "Authorization": `Bearer ${refreshToken}` }
          // }).then(res => {
          //   this.store.setToken(res.data.access_token, res.data.refresh_token)
          // }).catch(err => {
          //   console.log('refresh err', err);
          // })

          //logout user on token expire
          this.$q.dialog({
            title: 'Timeout',
            message: 'Your session ended, please login again',
          }).onOk(async () => {
            this.$router.push('/login')
          })
        }
        console.log('err', err);
      })
    },
    async getAllQweets() {
      const response = await api.get(`/qweet`, {
        headers: { "Authorization": `Bearer ${this.token}` }
      }).then(res => {
        this.qweets = res.data.data
      }).catch(err => {
        console.log('err', err);
      })
    },
    async addNewQweet() {
      let newQweet = {
        content: this.newQweetContent
      }
      try {
        const response = await api.post(`/qweet`, newQweet, {
          headers: { "Authorization": `Bearer ${this.token}` }
        })
        newQweet.created_at = response.data.data.created_at
        this.qweets.unshift(newQweet)
        this.$q.notify('Qweet added!')
        this.newQweetContent = ''
        this.getAllQweets()

      } catch (err) {
        console.log(err);
      }
    },
    async commentQweet(qweet) {
      try {
        const data = await this.$q.dialog({
          title: 'Comment',
          message: 'Please type your comment',
          prompt: {
            model: '',
            type: 'text'
          },
          cancel: true
        }).onOk(async data => {
          let commentId = qweet.qweet_id
          let commentData = {
            comment: data
          }
          const response = await api.patch(`/qweet/comment/${commentId}`, commentData).then(res => {
            console.log('res', res);
            this.getAllQweets()
          }).catch(err => {
            console.log('err', err);
          })
        })

      } catch (err) {
        console.log(err);
      }
    },
    reQweet(qweet) {
      this.share++
    },
    likeQweet(qweet) {
      this.like++
    },

    deleteQweet(qweet) {
      try {
        this.$q.dialog({
          title: 'Confirm',
          message: 'Would you like to delete this Qweet?',
          cancel: true
        }).onOk(async () => {
          let idToDelete = qweet.qweet_id
          await api.delete(`/qweet/${idToDelete}`)
          this.qweets.splice(qweet, 1)
          this.$q.notify('Qweet deleted!')

          // console.log(idToDelete);
        })
      } catch (err) {
        console.log(err);
      }
    },
    logout() {
      this.$q.dialog({
        title: 'Confirm',
        message: 'Are you sure you want to logout?',
      }).onOk(() => {
        this.store.removeAccessToken()
        this.store.removeRefreshToken()
        this.$router.push('/logout')
      })
    }
  },
})
</script>

<style lang="sass">
.new-qweet
  textarea
    font-size: 19px
    line-height: 1.4 !important
.divider
  border-top: 1px solid
  border-bottom: 1px solid
  border-color: $grey-4
.qweet-content
  white-space: pre-line
.qweet-icons
  margin-left: -5px
.qweet:not(:first-child)
  border-top: 1px solid rgba(0,0,0,0.12)
</style>
