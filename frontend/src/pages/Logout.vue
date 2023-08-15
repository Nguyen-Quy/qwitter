<template>
  <q-page class="window-height window-width row justify-center items-center">
    <div class="column justify-between items-end q-pa-lg dark" style="max-width: 500px;height: 90vh;">
      <div class="text-center q-mb-md">
        <h2>Qwitter</h2>
        <h4>Wilkomme zu der Welt der Qwitter</h4>
      </div>

      <div class="q-pa-none">
        <h5>There are no limits, you are only limited by however far you want to be limited</h5>
        <h6 class="justify-end">-Chuck Schuldiner-</h6>

        <div class="row justify-center q-mt-lg">
          <div class="text-center items-end q-pa-md q-gutter-md">
            <q-btn
              unelevated
              size="lg"
              color="indigo"
              class=" text-white"
              label="Sign In"
              to="/login" />
            <q-btn
              unelevated
              size="lg"
              color="indigo"
              class=" text-white"
              label="Register"
              to="/register" />
          </div>
        </div>
      </div>
    </div>

  </q-page>
</template>

<script>
export default {
  // name: 'PageName',
}
</script>

<style lang="sass">
@import url('https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap')

h2,h3,h4,h5,h6
  font-family: 'Gloria Hallelujah', cursive
  color: #fff
  top: 20%
  // word-wrap: break-word
  hyphens: auto
  margin: 0

h2
  margin-bottom: 20px

.dark
  background: #1817309a
</style>
