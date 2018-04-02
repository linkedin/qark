<template>
  <div class="animated fadeIn">
    <b-card>
      <div slot="header">
                Manifest File Issues
        <b-badge variant="success" class="float-right">Success</b-badge>
      </div>
      <div v-for="data in json">
        <div v-if="data.category == 'Manifest'||data.category == 'manifest'" class="card-divider">
          <p class="vulnerability" v-if="data.severity == 'VULNERABILITY'">{{data.severity}}</p>
          <p class="warning" v-if="data.severity == 'WARNING'">{{data.severity}}</p>
          <p class="info" v-if="data.severity == 'INFO'">{{data.severity}}</p>
          <h5><b>Name:</b> {{data.name}}</h5>
          <p><b>Description:</b> {{data.description}}</p>
          <p><b>Filepath:</b> {{data.file_object}}</p>
          <br>
        </div>
      </div>
     </b-card>
  </div>
</template>

<script>
  import jsonObject from '../report'
  export default {
    name: 'card.vue',
    data () {
      return {
        json: jsonObject
      }
    }
  }
</script>
