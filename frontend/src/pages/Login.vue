<template>
  <q-page class="window-height window-width row justify-center items-center">
    <div class="column q-pa-lg dark">
      <div class="row">
        <q-card square class="transparent" style="width:400px;height:600px;">
          <q-card-section class="bg-indigo q-mb-md">
            <h4 class="text-h5 text-white q-my-md"><q-icon name="login" /> Login</h4>
            <div class="absolute-bottom-right q-pr-md" style="transform: translateY(50%);">
              <q-btn fab icon="add" color="indigo-4" />
            </div>
          </q-card-section>

          <q-card-section class="q-mb-lg">
            <q-form class="q-px-sm q-py-lg">
              <q-input
                dark
                hide-bottom-space
                v-model="username"
                type="username"
                label="Username"
                :error="this.v$.username.$error"
                :error-message="this.v$.username.$errors[0] ? v$.username.$errors[0].$message : ''">
                <template v-slot:prepend>
                  <q-icon name="person" />
                </template>
              </q-input>
              <q-input
                dark
                hide-bottom-space
                v-model="password"
                type="password"
                label="Password"
                :error="this.v$.password.$error"
                :error-message="this.v$.password.$errors[0] ? v$.password.$errors[0].$message : ''">
                <template v-slot:prepend>
                  <q-icon name="vpn_key" />
                </template>
              </q-input>
            </q-form>
          </q-card-section>

          <q-card-actions class="q-px-lg">
            <q-btn color="white" textColor="blue" @click="fillform" label="fillform" />
            <q-btn
              unelevated
              size="lg"
              color="indigo"
              class="full-width text-white"
              @click="login"
              label="Sign In" />
          </q-card-actions>
          <q-card-section>
            <div class="text-center q-pa-md q-gutter-md">
              <q-btn round color="indigo-7">
                <q-icon name="fab fa-facebook-f" size="1.2rem" />
              </q-btn>
              <q-btn round color="red-8">
                <q-icon name="fab fa-google-plus-g" size="1.2rem" />
              </q-btn>
              <q-btn round color="light-blue-5">
                <q-icon name="fab fa-twitter" size="1.2rem" />
              </q-btn>
            </div>
          </q-card-section>

          <q-card-section class="text-center q-pa-sm">
            <p class="text-grey-4">Forgot your password?</p>
          </q-card-section>
        </q-card>
      </div>
    </div>

  </q-page>
</template>


<script>
import { defineComponent } from "vue"
import { api } from "src/boot/axios";
import { useAuthStore } from "../stores/auth";
import { useVuelidate } from '@vuelidate/core'
import { required, helpers } from "@vuelidate/validators"

export default defineComponent({
  name: 'LoginPage',
  setup() {
    const store = useAuthStore()

    return {
      v$: useVuelidate({ $lazy: true }),
      store
    }
  },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  validations() {
    return {
      username: {
        required: helpers.withMessage('Username cannot be blank', required)
      },
      password: {
        required: helpers.withMessage('Password cannot be blank', required)
      },
    }
  },
  methods: {
    async login() {
      const isFormCorrect = await this.v$.$validate()
      const formData = new FormData()
      formData.append('username', this.username)
      formData.append('password', this.password)

      if (!isFormCorrect) {
        return

      } else {
        const response = await api.post(`users/login`, formData)
          .then(res => {
            this.store.setToken(res.data.access_token, res.data.refresh_token)

            this.$q.notify({
              color: 'green-4',
              textColor: 'white',
              icon: 'check_circle',
              position: 'top',
              message: 'Logged in successfully',
              timeout: 3000,
            })
            this.$router.push('/')
          })
          .catch(err => {
            console.log('error', err)
            if (err.response.status == 400 || err.response.status == 404) {
              this.$q.notify({
                type: 'negative',
                position: 'top',
                message: err.response.data.detail,
                timeout: 3000,
              })
            }
          })
      }
    },
    fillform() {
      this.username = 'quy1'
      this.password = 'quy12345'
    }
  },
})
</script>
<style lang="sass">
.dark
  background: #1817309a
</style>
