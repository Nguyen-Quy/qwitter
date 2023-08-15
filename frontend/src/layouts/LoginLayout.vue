<template>
  <!-- <q-layout view="lhr lpR lfr"> -->
  <q-layout view="lHh Lpr lFf" class="img-background">
    <q-page-container class="container-fluid">
      <router-view />
    </q-page-container>

  </q-layout>
</template>
<style lang="sass">
::-webkit-scrollbar
  display: none
.img-background
  background: #fff url(~src/assets/background-image.jpg)
  height: 100%
  background-position: center
  background-repeat: no-repeat
  background-size: cover
  border: 1px solid #000
</style>
