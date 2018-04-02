<template>
  <div class="animated fadeIn">
    <b-card-group deck>
        <b-card bg-variant="danger"
                text-variant="white"
                header-text-variant="white"
                header-slot="header"
                class="text-center bg-transparent">
            <h1 slot="header" class="mb-0 font-weight-bold display-2">0</h1>
            <p class="card-text font-weight-bold text-dark">VULNERABILITY</p>
        </b-card>
        <b-card bg-variant="warning"
                text-variant="white"
                header-text-variant="white"
                header-slot="header"
                class="text-center bg-transparent">
            <h1 slot="header" class="mb-0 font-weight-bold display-2">0</h1>
            <p class="card-text font-weight-bold text-dark">Warnings</p>
        </b-card>
        <b-card bg-variant="info"
                text-variant="white"
                header-text-variant="white"
                header-slot="header"
                class="text-center bg-transparent">
            <h1 slot="header" class="mb-0 font-weight-bold display-2">0</h1>
            <p class="card-text font-weight-bold text-dark">Informational</p>
        </b-card>
        <b-card bg-variant="primary"
                text-variant="white"
                header-text-variant="white"
                header-slot="header"
                class="text-center bg-transparent">
            <h1 slot="header" class="mb-0 font-weight-bold display-2">0</h1>
            <p class="card-text font-weight-bold text-dark">Debug</p>
        </b-card>
    </b-card-group>
  </div>
</template>

<script>
  import jsonObject from '../report'
  export default {
    name: 'report',
    data () {
      return {
        json: jsonObject
      }
    }
}
</script>
