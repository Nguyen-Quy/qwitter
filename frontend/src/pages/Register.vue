<template>
  <q-page class="window-height window-width row justify-center items-center">
    <div class="column q-pa-lg dark">
      <div class="row">
        <q-card square class="transparent" style="width:400px;height:600px;">
          <q-card-section class="bg-indigo q-mb-md">
            <h4 class="text-h5 text-white q-my-md"><q-icon name="app_registration" /> Registration</h4>
            <div class="absolute-bottom-right q-pr-md" style="transform: translateY(50%);">
              <q-btn fab icon="close" color="indigo-4" />
            </div>
          </q-card-section>
          <q-card-section class="q-mb-lg">
            <q-form dense class="q-px-sm q-pt-lg">
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
                v-model="email"
                type="email"
                label="Email"
                :error="this.v$.email.$error"
                :error-message="this.v$.email.$errors[0] ? v$.email.$errors[0].$message : ''">
                <template v-slot:prepend>
                  <q-icon name="email" />
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

              <q-input
                dark
                hide-bottom-space
                v-model="confirm"
                type="password"
                label="Confirm password"
                :error="this.v$.confirm.$error"
                :error-message="this.v$.confirm.$errors[0] ? v$.confirm.$errors[0].$message : ''">
                <template v-slot:prepend>
                  <q-icon name="vpn_key" />
                </template>
              </q-input>
            </q-form>
          </q-card-section>

          <q-card-section class="text-center q-pa-sm">
            <q-card-actions class="q-px-lg q-mb-md">
              <q-btn color="white" textColor="blue" @click="fillform" label="fillform" />
              <q-btn
                unelevated
                size="lg"
                color="indigo"
                class="full-width text-white"
                @click="submitForm"
                label="Get Started" />
            </q-card-actions>
            <q-btn to="/login" flat color="grey-4" label="Return to login" />
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength, sameAs, helpers } from '@vuelidate/validators'
import { defineComponent } from 'vue'
import { api } from "src/boot/axios";

export default defineComponent({
  name: 'RegisterPage',
  setup() {
    return { v$: useVuelidate({ $lazy: true }) }
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirm: '',
    }
  },
  validations() {
    return {
      username: {
        required: helpers.withMessage('Username cannot be blank', required)
      },
      email: {
        required: helpers.withMessage('Email cannot be blank', required),
        email: helpers.withMessage('Please type a valid email address', email)
      },
      password: {
        required: helpers.withMessage('Password cannot be blank', required),
        minLengthValue: helpers.withMessage('Password should be at least 8 characters', minLength(8))
      },
      confirm: {
        required: helpers.withMessage('Please confirm password', required),
        sameAsPassword: helpers.withMessage('Confirm password must be the same as password', sameAs(this.password))
      }

    }
  },
  methods: {
    fillform() {
      this.username = 'quy1'
      this.email = 'quy@gmail.com'
      this.password = 'quy12345'
      this.confirm = 'quy12345'
    },
    async submitForm() {
      const isFormCorrect = await this.v$.$validate()
      let userData = {
        username: this.username,
        email: this.email,
        password: this.password,
        confirm: this.confirm
      }
      if (!isFormCorrect) {
        return

      } else {
        const response = await api.post(`users/signup`, userData)
          .then(res => {
            this.$q.notify({
              color: 'green-4',
              textColor: 'white',
              icon: 'check_circle',
              position: 'top',
              message: 'Successfully registered'
            })
            this.$router.push('/login')
          })
          .catch(err => {
            console.log(err)
            this.$q.notify({
              type: 'negative',
              position: 'top',
              message: err.response.data.detail
            })
          })
      }
    },
  },
})
</script>
<style lang="sass">
.dark
  background: #1817309a
</style>
