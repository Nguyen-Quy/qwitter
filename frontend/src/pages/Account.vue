<template>
  <q-page class="q-pa-lg">
    <h4 class="q-mt-none q-mb-md text-weight-bold">
      Change Account Information
    </h4>
    <div class="q-py-sm" style="max-width: 400px">
      <h5 class="q-mt-none q-mb-sm text-weight-bold">
        Change your email & name
      </h5>
      <q-form @submit="submitNameChange" class="q-gutter-md">
        <q-input
          hide-bottom-space
          v-model="email"
          type="email"
          label="Email"
          :error="this.v$.email.$error"
          :error-message="this.v$.email.$errors[0] ? v$.email.$errors[0].$message : ''">
          <template v-slot:prepend>
            <q-icon color="primary" name="email" />
          </template>
        </q-input>
        <q-input
          v-model="fullname"
          label="Full name">
          <template v-slot:prepend>
            <q-icon color="primary" name="person" />
          </template>
        </q-input>
        <div class="q-py-md">
          <q-btn rounded label="Submit" type="submit" color="primary" class="glossy" />
          <q-btn @click="fillname" label="fillform" class="q-ml-md" color="black" />
        </div>
      </q-form>
    </div>

    <div class="q-py-md" style="max-width: 400px">
      <h5 class="q-mt-none q-mb-sm text-weight-bold">
        Change your password
      </h5>
      <q-form @submit="submitPassChange" class="q-gutter-md">
        <q-input
          hide-bottom-space
          v-model="current_pass"
          type="password"
          label="Current password"
          :error="this.v$.current_pass.$error"
          :error-message="this.v$.current_pass.$errors[0] ? v$.current_pass.$errors[0].$message : ''">
          <template v-slot:prepend>
            <q-icon color="primary" name="password" />
          </template>
        </q-input>
        <q-input
          hide-bottom-space
          v-model="new_pass"
          type="password"
          label="New password"
          :error="this.v$.new_pass.$error"
          :error-message="this.v$.new_pass.$errors[0] ? v$.new_pass.$errors[0].$message : ''">
          <template v-slot:prepend>
            <q-icon color="primary" name="vpn_key" />
          </template>
        </q-input>
        <q-input
          hide-bottom-space
          v-model="confirm_pass"
          type="password"
          label="Confirm password"
          :error="this.v$.confirm_pass.$error"
          :error-message="this.v$.confirm_pass.$errors[0] ? v$.confirm_pass.$errors[0].$message : ''">
          <template v-slot:prepend>
            <q-icon color="primary" name="vpn_key" />
          </template>
        </q-input>

        <div class="q-py-md">
          <q-btn rounded label="Submit" type="submit" color="primary" class="glossy" />
          <q-btn @click="fillpass" label="fillform" class="q-ml-md" color="black" />
        </div>
      </q-form>

    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useVuelidate } from "@vuelidate/core"
import { required, email, helpers, sameAs, minLength } from "@vuelidate/validators"
import { api } from "src/boot/axios"
import { useAuthStore } from "../stores/auth";

export default defineComponent({
  name: 'Account',
  setup() {
    const store = useAuthStore()
    const token = store.getAccessToken()

    return {
      store,
      token,
      v$: useVuelidate({ $lazy: true })
    }
  },
  data() {
    return {
      email: undefined,
      fullname: undefined,
      current_pass: undefined,
      new_pass: undefined,
      confirm_pass: undefined,
    }
  },
  validations() {
    return {
      email: {
        email: helpers.withMessage('Please type a valid email address', email)
      },
      current_pass: {
        // required: helpers.withMessage('Please type in password', required),
        minLengthValue: helpers.withMessage('Password should be at least 8 characters', minLength(8))
      },
      new_pass: {
        minLengthValue: helpers.withMessage('Password should be at least 8 characters', minLength(8))
      },
      confirm_pass: {
        minLengthValue: helpers.withMessage('Password should be at least 8 characters', minLength(8)),
        sameAsNewPass: helpers.withMessage('Confirm password must be the same as password', sameAs(this.new_pass))
      }
    }
  },
  methods: {
    fillname() {
      this.email = 'quy1@gmail.com'
      this.fullname = 'Nguyen Duc Quy'
    },
    fillpass() {
      this.current_pass = 'quy12345'
      this.new_pass = 'quy123456'
      this.confirm_pass = 'quy123456'
    },
    async submitUpdate(data) {
      const isFormCorrect = await this.v$.$validate()

      if (!isFormCorrect) {
        return
      } else {
        const response = await api.patch(`users/update`, data, {
          headers: { "Authorization": `Bearer ${this.token}` }
        }).then(res => {
          this.$q.notify({
            color: 'green-4',
            textColor: 'white',
            icon: 'update',
            position: 'top',
            message: 'Successfully updated user'
          })
        }).catch(err => {
          console.log(err)
          this.$q.notify({
            type: 'negative',
            position: 'top',
            message: err.response.data.detail
          })
        })
      }
    },
    async submitNameChange() {
      let nameData = {
        email: this.email,
        fullname: this.fullname,
      }
      this.submitUpdate(nameData)
    },
    async submitPassChange() {
      let passData = {
        current_pass: this.current_pass,
        new_pass: this.new_pass,
        confirm_pass: this.confirm_pass,
      }
      this.submitUpdate(passData)
    }
  },
})
</script>
<style lang="sass">
.test
  transform: rotate(45deg)
</style>
